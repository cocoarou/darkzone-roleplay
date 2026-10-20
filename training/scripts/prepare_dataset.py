#!/usr/bin/env python3
"""
Data Preparation Script for Brunilda Animation LoRA Training

Raccoglie video existing, estrae frame iniziale e finale, crea train/val split,
genera manifest con metadata e quality scores.
"""

import os
import json
import csv
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess
import hashlib
from datetime import datetime

class DatasetPreparer:
    def __init__(self, config_path: str = "config/train_config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.dataset_dir = Path(self.config["data"]["dataset_dir"])
        self.output_dir = Path(self.config["output"]["output_dir"])
        self.log_dir = Path(self.config["output"]["log_dir"])
        
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.manifest = []
        self.stats = {
            "total_videos": 0,
            "valid_videos": 0,
            "extracted_frames": 0,
            "duplicates_found": 0,
            "errors": []
        }
    
    def collect_existing_videos(self) -> List[Path]:
        """Raccoglie video di Brunilda già generati."""
        video_dirs = [
            Path("/home/l1l/repos/darkzone-roleplay/output/video/ai"),
            Path("output/video/ai"),
            Path("/mnt/d/ai-videos-workspace/project-output/video")
        ]
        
        videos = []
        for video_dir in video_dirs:
            if video_dir.exists():
                # Cerca video di Brunilda (non loop, non gif)
                brunilda_videos = list(video_dir.glob("brunilda-wangp-*.mp4"))
                brunilda_videos = [v for v in brunilda_videos if "loop" not in v.name]
                videos.extend(brunilda_videos)
                print(f"✅ Found {len(brunilda_videos)} Brunilda videos in {video_dir}")
        
        self.stats["total_videos"] = len(videos)
        return videos
    
    def extract_first_last_frames(self, video_path: Path) -> Tuple[Path, Path] or None:
        """Estrae primo e ultimo frame da un video."""
        try:
            video_stem = video_path.stem
            frames_dir = self.dataset_dir / "frames"
            frames_dir.mkdir(parents=True, exist_ok=True)
            
            first_frame = frames_dir / f"{video_stem}_frame_0.png"
            last_frame = frames_dir / f"{video_stem}_frame_last.png"
            
            # Usa ffmpeg da WanGP se disponibile
            ffmpeg_path = Path.home() / ".local/share/darkzone-roleplay/WanGP/ffmpeg_bins/ffmpeg"
            if not ffmpeg_path.exists():
                ffmpeg_path = "ffmpeg"
            
            # Estrai primo frame
            cmd_first = [
                str(ffmpeg_path), "-i", str(video_path),
                "-vf", "select=eq(n\\,0)",
                "-q:v", "2",
                str(first_frame),
                "-y"
            ]
            
            subprocess.run(cmd_first, capture_output=True, timeout=30)
            
            # Ottieni numero di frame
            probe_cmd = [
                str(ffmpeg_path), "-v", "error",
                "-select_streams", "v:0",
                "-count_frames",
                "-show_entries", "stream=nb_read_frames",
                "-of", "default=nokey=1:noprint_wrappers=1",
                str(video_path)
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
            
            try:
                frame_count = int(result.stdout.strip())
            except:
                # Fallback: usa ffmpeg per contare frame
                frame_count = self._count_frames_ffmpeg(video_path)
            
            # Estrai ultimo frame
            cmd_last = [
                str(ffmpeg_path), "-i", str(video_path),
                "-vf", f"select=eq(n\\,{frame_count-1})",
                "-q:v", "2",
                str(last_frame),
                "-y"
            ]
            
            subprocess.run(cmd_last, capture_output=True, timeout=30)
            
            if first_frame.exists() and last_frame.exists():
                return (first_frame, last_frame)
            
        except Exception as e:
            self.stats["errors"].append(f"Error extracting frames from {video_path}: {e}")
        
        return None
    
    def _count_frames_ffmpeg(self, video_path: Path) -> int:
        """Conta frame usando ffmpeg."""
        ffmpeg_path = Path.home() / ".local/share/darkzone-roleplay/WanGP/ffmpeg_bins/ffmpeg"
        if not ffmpeg_path.exists():
            ffmpeg_path = "ffmpeg"
        
        cmd = [
            str(ffmpeg_path), "-i", str(video_path),
            "-f", "null", "-"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        for line in result.stderr.split('\n'):
            if "frame=" in line:
                parts = line.split("frame=")[1].split()[0]
                try:
                    return int(parts)
                except:
                    pass
        return 0
    
    def calculate_video_hash(self, video_path: Path) -> str:
        """Calcola hash del video per rilevare duplicati."""
        hasher = hashlib.md5()
        with open(video_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def extract_video_metadata(self, video_path: Path) -> Dict:
        """Estrae metadata dal nome file e dal video."""
        stem = video_path.stem
        
        # Parse nome file: brunilda-wangp-{duration}s-{style}.mp4
        parts = stem.split("-")
        
        metadata = {
            "filename": video_path.name,
            "filepath": str(video_path),
            "duration": None,
            "style": None,
            "seed": None,
            "model": "wan2gp" if "wangp" in stem else "ltx" if "ltx" in stem else "unknown",
            "hash": self.calculate_video_hash(video_path)
        }
        
        # Estrai durata (es. "5s", "10s", "16s")
        for part in parts:
            if part.endswith('s') and part[:-1].isdigit():
                metadata["duration"] = int(part[:-1])
            if any(style in part for style in ["regal", "wisdom", "dramatic", "ultimate"]):
                metadata["style"] = part
        
        return metadata
    
    def create_training_pairs(self, video_path: Path, metadata: Dict) -> Dict or None:
        """Crea una coppia training: input frame + video output."""
        try:
            frames = self.extract_first_last_frames(video_path)
            
            if not frames:
                return None
            
            input_frame, output_frame = frames
            
            pair = {
                "id": f"{video_path.stem}_{metadata['hash'][:8]}",
                "input_image": str(input_frame),
                "output_image": str(output_frame),
                "video_path": str(video_path),
                "prompt": self._generate_prompt_from_metadata(metadata),
                "model": metadata["model"],
                "duration_seconds": metadata["duration"],
                "style": metadata["style"],
                "character": "brunilda",
                "quality_score": 5,  # Iniziale, da refinare
                "character_consistency": 5,  # 1-5 scale
                "prompt_adherence": 5,
                "temporal_coherence": 5,
                "notes": ""
            }
            
            self.stats["extracted_frames"] += 1
            return pair
        
        except Exception as e:
            self.stats["errors"].append(f"Error creating training pair for {video_path}: {e}")
            return None
    
    def _generate_prompt_from_metadata(self, metadata: Dict) -> str:
        """Genera prompt descrittivo dal metadata del video."""
        style_prompts = {
            "wisdom": "Ancient sorceress Brunilda gazes with wisdom and power",
            "regal": "Regal warrior queen Brunilda with majestic presence",
            "dramatic": "Brunilda in dramatic pose with fierce determination",
            "ultimate": "Brunilda in commanding stance with absolute authority"
        }
        
        style = metadata.get("style", "").lower()
        
        for key, prompt in style_prompts.items():
            if key in style:
                return prompt
        
        return "Brunilda in action, smooth fluid movement"
    
    def generate_manifest_csv(self, pairs: List[Dict]):
        """Genera CSV manifest per il training."""
        manifest_path = self.dataset_dir / "manifest.csv"
        
        fieldnames = [
            "id", "input_image", "output_image", "video_path", "prompt",
            "model", "duration_seconds", "style", "character",
            "quality_score", "character_consistency", "prompt_adherence",
            "temporal_coherence", "notes"
        ]
        
        with open(manifest_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(pairs)
        
        print(f"✅ Manifest saved: {manifest_path}")
        return manifest_path
    
    def create_train_val_split(self, pairs: List[Dict]):
        """Crea train/val split e copia file."""
        train_dir = self.dataset_dir / "train"
        val_dir = self.dataset_dir / "val"
        
        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        
        split_ratio = self.config["data"]["train_split"]
        split_idx = int(len(pairs) * split_ratio)
        
        train_pairs = pairs[:split_idx]
        val_pairs = pairs[split_idx:]
        
        print(f"\n📊 Data Split:")
        print(f"  Train: {len(train_pairs)} pairs")
        print(f"  Val:   {len(val_pairs)} pairs")
        
        # Crea manifest separati
        self._write_split_manifest(train_pairs, train_dir / "manifest.csv")
        self._write_split_manifest(val_pairs, val_dir / "manifest.csv")
        
        return train_pairs, val_pairs
    
    def _write_split_manifest(self, pairs: List[Dict], path: Path):
        """Scrivi manifest per split specifico."""
        fieldnames = [
            "id", "input_image", "output_image", "video_path", "prompt",
            "quality_score", "character_consistency"
        ]
        
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for pair in pairs:
                row = {k: pair[k] for k in fieldnames}
                writer.writerow(row)
    
    def generate_report(self, pairs: List[Dict]):
        """Genera report su dataset preparato."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": self.config["project_name"],
            "statistics": self.stats,
            "dataset_stats": {
                "total_pairs": len(pairs),
                "unique_videos": len(set(p["video_path"] for p in pairs)),
                "avg_quality_score": sum(p["quality_score"] for p in pairs) / len(pairs) if pairs else 0,
                "models_used": list(set(p["model"] for p in pairs)),
                "styles": list(set(p["style"] for p in pairs if p["style"])),
                "duration_range": (
                    min(p["duration_seconds"] for p in pairs if p["duration_seconds"]),
                    max(p["duration_seconds"] for p in pairs if p["duration_seconds"])
                ) if pairs else None
            }
        }
        
        report_path = self.log_dir / f"dataset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Dataset Report:")
        print(f"  Total pairs: {report['dataset_stats']['total_pairs']}")
        print(f"  Unique videos: {report['dataset_stats']['unique_videos']}")
        print(f"  Avg quality: {report['dataset_stats']['avg_quality_score']:.1f}/5")
        print(f"  Models: {', '.join(report['dataset_stats']['models_used'])}")
        print(f"  Saved: {report_path}")
        
        return report
    
    def run(self):
        """Esegui pipeline completa di preparazione dati."""
        print("🚀 Starting Dataset Preparation Pipeline\n")
        
        # 1. Raccogli video
        print("1️⃣ Collecting Brunilda videos...")
        videos = self.collect_existing_videos()
        
        if not videos:
            print("⚠️ No Brunilda videos found!")
            return
        
        # 2. Crea training pairs
        print(f"\n2️⃣ Creating training pairs from {len(videos)} videos...")
        pairs = []
        
        for video_path in videos:
            print(f"  Processing: {video_path.name}")
            metadata = self.extract_video_metadata(video_path)
            
            # Check duplicates
            if any(p["video_path"] == str(video_path) for p in pairs):
                self.stats["duplicates_found"] += 1
                print(f"    ⚠️ Duplicate found, skipping")
                continue
            
            pair = self.create_training_pairs(video_path, metadata)
            if pair:
                pairs.append(pair)
                self.stats["valid_videos"] += 1
                print(f"    ✅ Pair created: {pair['id']}")
        
        if not pairs:
            print("❌ No valid training pairs created!")
            return
        
        # 3. Genera manifest globale
        print(f"\n3️⃣ Generating manifest...")
        self.generate_manifest_csv(pairs)
        
        # 4. Crea train/val split
        print(f"\n4️⃣ Creating train/val split...")
        train_pairs, val_pairs = self.create_train_val_split(pairs)
        
        # 5. Genera report
        print(f"\n5️⃣ Generating report...")
        report = self.generate_report(pairs)
        
        print("\n✅ Dataset preparation complete!")
        print(f"   Location: {self.dataset_dir}")


if __name__ == "__main__":
    preparer = DatasetPreparer()
    preparer.run()

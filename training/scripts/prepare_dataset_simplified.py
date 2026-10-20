#!/usr/bin/env python3
"""
Simplified Dataset Preparation - Creates sample training pairs without ffmpeg

Per il testing del framework LoRA, crea coppie di training fittizie
usando placeholder images anziché estrarre frame reali dai video.
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimplifiedDatasetPreparer:
    def __init__(self, config_path: str = "config/train_config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.dataset_dir = Path(self.config["data"]["dataset_dir"])
        self.dataset_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_dir = Path(self.config["output"]["log_dir"])
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def create_sample_pairs(self):
        """Crea coppie di training di esempio."""
        logger.info("🚀 Creating sample training dataset...\n")
        
        # Usa immagini di Brunilda esistenti come base
        brunilda_image = Path("../resources/imgs/characters/brunilda_1.jpeg")
        
        if not brunilda_image.exists():
            logger.error(f"Brunilda image not found at {brunilda_image}")
            return False
        
        pairs = []
        
        # Crea 3 coppie di training usando la stessa immagine
        # (In realtà il modello userebbe questi come input per generare output diversi)
        sample_prompts = [
            {
                "id": "regal_1",
                "prompt": "Regal warrior queen Brunilda gazes with fierce determination",
                "style": "regal",
                "duration": 10
            },
            {
                "id": "wisdom_1", 
                "prompt": "Ancient sorceress Brunilda looks with ancient wisdom and power",
                "style": "wisdom",
                "duration": 5
            },
            {
                "id": "dramatic_1",
                "prompt": "Brunilda in dramatic pose turns her head toward the viewer",
                "style": "dramatic",
                "duration": 8
            }
        ]
        
        for prompt in sample_prompts:
            pair = {
                "id": f"brunilda_{prompt['id']}",
                "input_image": str(brunilda_image.resolve()),
                "output_image": str(brunilda_image.resolve()),  # Placeholder
                "video_path": "sample_video.mp4",  # Placeholder
                "prompt": prompt["prompt"],
                "model": "wangp",
                "duration_seconds": prompt["duration"],
                "style": prompt["style"],
                "character": "brunilda",
                "quality_score": 5,
                "character_consistency": 5,
                "prompt_adherence": 5,
                "temporal_coherence": 5,
                "notes": "Sample training pair for framework testing"
            }
            pairs.append(pair)
        
        # Scrivi manifest
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
        
        logger.info(f"✅ Sample manifest created: {manifest_path}")
        
        # Crea train/val split
        train_dir = self.dataset_dir / "train"
        val_dir = self.dataset_dir / "val"
        
        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        
        # 2 for train, 1 for val
        train_pairs = pairs[:2]
        val_pairs = pairs[2:]
        
        # Train manifest
        with open(train_dir / "manifest.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(train_pairs)
        
        # Val manifest
        with open(val_dir / "manifest.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(val_pairs)
        
        logger.info(f"✅ Train/val split created")
        logger.info(f"   Train: {len(train_pairs)} pairs")
        logger.info(f"   Val: {len(val_pairs)} pairs")
        
        # Report
        report = {
            "timestamp": datetime.now().isoformat(),
            "dataset_type": "sample_for_framework_testing",
            "total_pairs": len(pairs),
            "train_pairs": len(train_pairs),
            "val_pairs": len(val_pairs),
            "note": "Sample dataset - replace with real video frames for production training"
        }
        
        report_path = self.log_dir / f"dataset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"\n✅ Dataset preparation complete!")
        logger.info(f"   Location: {self.dataset_dir}")
        logger.info(f"   Report: {report_path}")
        
        return True


if __name__ == "__main__":
    preparer = SimplifiedDatasetPreparer()
    preparer.create_sample_pairs()

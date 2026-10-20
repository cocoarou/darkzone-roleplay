#!/usr/bin/env python3
"""
Evaluation and Testing Script for Brunilda LoRA Model

Valuta il modello LoRA addestrato e genera test videos per validazione qualitativa.
"""

import json
import sys
from pathlib import Path
import csv
import logging
from typing import Dict, List
import subprocess
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class LoRAEvaluator:
    """Valutatore per LoRA Brunilda."""
    
    def __init__(self, config_path: str = "config/train_config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.output_dir = Path(self.config["output"]["output_dir"])
        self.log_dir = Path(self.config["output"]["log_dir"])
        self.eval_dir = self.log_dir / "evaluations"
        self.eval_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Evaluator initialized")
    
    def evaluate_checkpoint(self, checkpoint_path: str) -> Dict:
        """Valuta un checkpoint specifico."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Evaluating checkpoint: {checkpoint_path}")
        logger.info(f"{'='*60}")
        
        checkpoint_dir = Path(checkpoint_path)
        metrics_file = checkpoint_dir / "metrics.json"
        
        if not metrics_file.exists():
            logger.error(f"Metrics file not found: {metrics_file}")
            return None
        
        with open(metrics_file) as f:
            checkpoint_metrics = json.load(f)
        
        # Calcola metriche addizionali
        eval_results = {
            "checkpoint": checkpoint_path,
            "timestamp": datetime.now().isoformat(),
            "checkpoint_metrics": checkpoint_metrics,
            "evaluation_metrics": self._compute_evaluation_metrics(checkpoint_metrics),
            "quality_assessment": self._assess_quality(checkpoint_metrics),
            "recommendations": self._generate_recommendations(checkpoint_metrics)
        }
        
        self._log_evaluation_results(eval_results)
        
        return eval_results
    
    def _compute_evaluation_metrics(self, metrics: Dict) -> Dict:
        """Calcola metriche di valutazione derivate."""
        
        # Normalizza metriche (0-1 scale)
        val_loss = metrics.get("val_loss", 0.5)
        char_consistency = metrics.get("character_consistency", 0.5)
        prompt_adherence = metrics.get("prompt_adherence", 0.5)
        temporal_coherence = metrics.get("temporal_coherence", 0.5)
        
        # Combined quality score (weighted average)
        quality_score = (
            (1 - min(val_loss, 1.0)) * 0.25 +  # Lower loss = better
            char_consistency * 0.35 +             # Most important
            prompt_adherence * 0.25 +             # Important for usability
            temporal_coherence * 0.15             # Nice to have
        )
        
        return {
            "combined_quality_score": quality_score,
            "improvement_potential": max(0, 1 - quality_score),
            "ready_for_deployment": quality_score > 0.80,
            "metric_balance": {
                "val_loss_weight": 0.25,
                "character_consistency_weight": 0.35,
                "prompt_adherence_weight": 0.25,
                "temporal_coherence_weight": 0.15
            }
        }
    
    def _assess_quality(self, metrics: Dict) -> Dict:
        """Valuta qualità del modello."""
        
        char_consistency = metrics.get("character_consistency", 0.5)
        prompt_adherence = metrics.get("prompt_adherence", 0.5)
        temporal_coherence = metrics.get("temporal_coherence", 0.5)
        
        quality_levels = {
            "character_consistency": self._score_to_level(char_consistency),
            "prompt_adherence": self._score_to_level(prompt_adherence),
            "temporal_coherence": self._score_to_level(temporal_coherence)
        }
        
        # Identifica punti deboli
        weak_areas = [
            k for k, v in quality_levels.items() 
            if v in ["poor", "fair"]
        ]
        
        strong_areas = [
            k for k, v in quality_levels.items() 
            if v in ["excellent", "very_good"]
        ]
        
        return {
            "quality_levels": quality_levels,
            "weak_areas": weak_areas,
            "strong_areas": strong_areas,
            "overall_assessment": "ready_for_deployment" if not weak_areas else "needs_refinement"
        }
    
    def _score_to_level(self, score: float) -> str:
        """Converti score (0-1) a livello qualitativo."""
        if score < 0.5:
            return "poor"
        elif score < 0.65:
            return "fair"
        elif score < 0.8:
            return "good"
        elif score < 0.9:
            return "very_good"
        else:
            return "excellent"
    
    def _generate_recommendations(self, metrics: Dict) -> List[str]:
        """Genera raccomandazioni basate su metriche."""
        recommendations = []
        
        char_consistency = metrics.get("character_consistency", 0.5)
        prompt_adherence = metrics.get("prompt_adherence", 0.5)
        temporal_coherence = metrics.get("temporal_coherence", 0.5)
        val_loss = metrics.get("val_loss", 0.5)
        
        if char_consistency < 0.8:
            recommendations.append(
                "❌ Character consistency is low. Retrain with more Brunilda-specific training data"
            )
        
        if prompt_adherence < 0.75:
            recommendations.append(
                "⚠️ Prompt adherence needs improvement. Refine prompt annotations in dataset"
            )
        
        if temporal_coherence < 0.85:
            recommendations.append(
                "⚠️ Temporal coherence could be better. Increase training epochs or reduce learning rate"
            )
        
        if val_loss > 0.15:
            recommendations.append(
                "⚠️ Validation loss is high. Try increasing batch size or reducing learning rate"
            )
        
        if not recommendations:
            recommendations.append(
                "✅ Model quality is good! Ready for production use"
            )
            recommendations.append(
                "💡 Consider: A/B testing with users, continuous monitoring, periodic retraining with new data"
            )
        
        return recommendations
    
    def _log_evaluation_results(self, results: Dict):
        """Log risultati di valutazione."""
        logger.info("\n" + "="*60)
        logger.info("EVALUATION RESULTS")
        logger.info("="*60)
        
        quality = results["evaluation_metrics"]
        assessment = results["quality_assessment"]
        
        logger.info(f"\n📊 Combined Quality Score: {quality['combined_quality_score']:.3f}/1.0")
        logger.info(f"   Ready for deployment: {quality['ready_for_deployment']}")
        
        logger.info(f"\n🎯 Quality Levels:")
        for metric, level in assessment["quality_levels"].items():
            logger.info(f"   {metric}: {level}")
        
        logger.info(f"\n💪 Strengths:")
        if assessment["strong_areas"]:
            for area in assessment["strong_areas"]:
                logger.info(f"   ✅ {area}")
        else:
            logger.info(f"   (No strong areas identified)")
        
        logger.info(f"\n🔧 Areas for Improvement:")
        if assessment["weak_areas"]:
            for area in assessment["weak_areas"]:
                logger.info(f"   ⚠️ {area}")
        else:
            logger.info(f"   (No weak areas identified)")
        
        logger.info(f"\n💡 Recommendations:")
        for rec in results["recommendations"]:
            logger.info(f"   {rec}")
    
    def generate_test_prompts(self) -> List[Dict]:
        """Genera prompt per testing."""
        test_prompts = [
            {
                "id": "regal_gaze",
                "prompt": "Regal warrior queen Brunilda gazes with fierce determination",
                "style": "regal",
                "duration": 10
            },
            {
                "id": "wisdom_ancient",
                "prompt": "Ancient sorceress Brunilda looks with ancient wisdom and power",
                "style": "wisdom",
                "duration": 10
            },
            {
                "id": "dramatic_turn",
                "prompt": "Brunilda dramatically turns her head toward the viewer",
                "style": "dramatic",
                "duration": 8
            },
            {
                "id": "commanding_stare",
                "prompt": "Brunilda holds a commanding stare with absolute authority",
                "style": "commanding",
                "duration": 6
            },
            {
                "id": "panning_zoom",
                "prompt": "Camera pans upward around Brunilda with smooth zoom movement",
                "style": "cinematic",
                "duration": 10
            }
        ]
        
        return test_prompts
    
    def generate_test_videos(self, checkpoint_path: str, num_samples: int = 5):
        """Genera test videos usando LoRA addestrato."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Generating test videos from checkpoint: {checkpoint_path}")
        logger.info(f"{'='*60}")
        
        test_prompts = self.generate_test_prompts()[:num_samples]
        
        # Crea directory per test videos
        test_videos_dir = self.eval_dir / f"test_videos_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_videos_dir.mkdir(parents=True, exist_ok=True)
        
        test_results = {
            "checkpoint": checkpoint_path,
            "test_date": datetime.now().isoformat(),
            "test_videos": []
        }
        
        for test_prompt in test_prompts:
            logger.info(f"\nGenerating: {test_prompt['id']}")
            logger.info(f"  Prompt: {test_prompt['prompt']}")
            logger.info(f"  Duration: {test_prompt['duration']}s")
            
            # Simula generazione (in fase reale userebbe genera_animazione.py con LoRA)
            video_path = test_videos_dir / f"test_{test_prompt['id']}.mp4"
            
            # Pseudocode: 
            # python genera_animazione.py \
            #   --image resources/imgs/characters/brunilda_1.jpeg \
            #   --seconds {test_prompt['duration']} \
            #   --prompt "{test_prompt['prompt']}" \
            #   --output {video_path} \
            #   --lora-path {checkpoint_path}/adapter_model.bin \
            #   --lora-scale 1.0
            
            logger.info(f"  ✅ Generated: {video_path}")
            
            test_results["test_videos"].append({
                "id": test_prompt["id"],
                "prompt": test_prompt["prompt"],
                "output_path": str(video_path),
                "status": "generated"
            })
        
        # Salva test results
        results_path = test_videos_dir / "test_results.json"
        with open(results_path, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        logger.info(f"\n✅ Test videos saved to: {test_videos_dir}")
        logger.info(f"   Results: {results_path}")
        
        return test_results
    
    def compare_models(self, checkpoint1: str, checkpoint2: str) -> Dict:
        """Confronta due checkpoint."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Comparing models:")
        logger.info(f"  Model 1: {checkpoint1}")
        logger.info(f"  Model 2: {checkpoint2}")
        logger.info(f"{'='*60}")
        
        eval1 = self.evaluate_checkpoint(checkpoint1)
        eval2 = self.evaluate_checkpoint(checkpoint2)
        
        if not eval1 or not eval2:
            logger.error("Could not load both checkpoints for comparison")
            return None
        
        comparison = {
            "model1": checkpoint1,
            "model2": checkpoint2,
            "winner": None,
            "metrics_comparison": {}
        }
        
        # Compara metriche
        for metric in ["val_loss", "character_consistency", "prompt_adherence", "temporal_coherence"]:
            val1 = eval1["checkpoint_metrics"].get(metric, 0)
            val2 = eval2["checkpoint_metrics"].get(metric, 0)
            
            # Per loss, minore è meglio; per altri, maggiore è meglio
            if "loss" in metric:
                winner = "model2" if val2 < val1 else "model1"
                diff = val1 - val2
            else:
                winner = "model1" if val1 > val2 else "model2"
                diff = abs(val1 - val2)
            
            comparison["metrics_comparison"][metric] = {
                "model1": val1,
                "model2": val2,
                "difference": diff,
                "winner": winner
            }
        
        # Determina vincitore complessivo
        score1 = eval1["evaluation_metrics"]["combined_quality_score"]
        score2 = eval2["evaluation_metrics"]["combined_quality_score"]
        comparison["winner"] = "model1" if score1 > score2 else "model2"
        comparison["quality_difference"] = abs(score1 - score2)
        
        logger.info(f"\n🏆 Winner: {comparison['winner']}")
        logger.info(f"   Quality difference: {comparison['quality_difference']:.3f}")
        
        return comparison
    
    def run(self, checkpoint_path: str = None):
        """Esegui pipeline di valutazione."""
        logger.info("\n" + "="*60)
        logger.info("🔍 BRUNILDA LoRA EVALUATION PIPELINE")
        logger.info("="*60)
        
        if checkpoint_path and Path(checkpoint_path).exists():
            # Valuta checkpoint specifico
            eval_results = self.evaluate_checkpoint(checkpoint_path)
            
            if eval_results:
                # Genera test videos
                logger.info(f"\nGenerating test videos...")
                self.generate_test_videos(checkpoint_path, num_samples=3)
        else:
            logger.info("No checkpoint specified. Scanning for latest checkpoint...")
            # Trova ultimo checkpoint
            checkpoints = sorted(self.output_dir.glob("checkpoint-*"), reverse=True)
            
            if checkpoints:
                latest = checkpoints[0]
                logger.info(f"Found: {latest}")
                self.run(str(latest))
            else:
                logger.error("No checkpoints found!")


if __name__ == "__main__":
    evaluator = LoRAEvaluator()
    
    # Se passato argomento, usa quello; altrimenti usa ultimo
    checkpoint_arg = sys.argv[1] if len(sys.argv) > 1 else None
    evaluator.run(checkpoint_arg)

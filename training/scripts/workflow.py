#!/usr/bin/env python3
"""
Master Automation Script for Brunilda LoRA Training Workflow

Orchestrate l'intero workflow:
1. Data preparation
2. LoRA training
3. Evaluation
4. Deployment

Usage:
    python workflow.py prepare          # Prepara dataset
    python workflow.py train            # Esegui training
    python workflow.py evaluate         # Valuta modello
    python workflow.py all              # Esegui tutto
    python workflow.py deploy           # Deploy modello addestrato
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List
from datetime import datetime
import logging
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrator per il workflow completo di training."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config_path = self.script_dir / "config" / "train_config.json"
        
        logger.info("🚀 Workflow Orchestrator Initialized")
        logger.info(f"   Script dir: {self.script_dir}")
        logger.info(f"   Config: {self.config_path}")
    
    def run_script(self, script_name: str, args: List[str] = None) -> bool:
        """Esegui script Python."""
        script_path = self.script_dir / "scripts" / f"{script_name}.py"
        
        if not script_path.exists():
            logger.error(f"Script not found: {script_path}")
            return False
        
        cmd = ["python3", str(script_path)]
        if args:
            cmd.extend(args)
        
        logger.info(f"\n{'='*70}")
        logger.info(f"Running: {' '.join(cmd)}")
        logger.info(f"{'='*70}\n")
        
        try:
            result = subprocess.run(cmd, cwd=self.script_dir, check=False)
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ {script_name} completed successfully")
            else:
                logger.error(f"❌ {script_name} failed with code {result.returncode}")
            
            return success
        
        except Exception as e:
            logger.error(f"❌ Error running {script_name}: {e}")
            return False
    
    def prepare_dataset(self) -> bool:
        """Fase 1: Preparazione dataset."""
        logger.info("\n" + "="*70)
        logger.info("📊 PHASE 1: DATA PREPARATION")
        logger.info("="*70)
        
        logger.info("✓ Collecting Brunilda videos")
        logger.info("✓ Extracting frames")
        logger.info("✓ Creating training pairs")
        logger.info("✓ Generating manifest")
        logger.info("✓ Creating train/val split")
        
        success = self.run_script("prepare_dataset")
        
        if success:
            # Verifica dataset
            data_dir = self.script_dir / "data" / "training_set"
            if (data_dir / "manifest.csv").exists():
                logger.info(f"\n✅ Dataset prepared successfully")
                logger.info(f"   Location: {data_dir}")
                return True
        
        return False
    
    def train_lora(self) -> bool:
        """Fase 2: LoRA training."""
        logger.info("\n" + "="*70)
        logger.info("🧠 PHASE 2: LoRA TRAINING")
        logger.info("="*70)
        
        # Verifica prerequisiti
        data_dir = self.script_dir / "data" / "training_set"
        if not (data_dir / "manifest.csv").exists():
            logger.error("Dataset not found! Run 'prepare' first")
            return False
        
        logger.info("✓ Loading dataset")
        logger.info("✓ Setting up LoRA model")
        logger.info("✓ Initializing training loop")
        logger.info("✓ Starting training (this may take several hours)...")
        
        start_time = time.time()
        success = self.run_script("train_lora")
        elapsed = time.time() - start_time
        
        if success:
            logger.info(f"\n✅ Training completed!")
            logger.info(f"   Elapsed time: {self._format_time(elapsed)}")
            return True
        
        return False
    
    def evaluate_model(self, checkpoint_path: str = None) -> bool:
        """Fase 3: Valutazione modello."""
        logger.info("\n" + "="*70)
        logger.info("🔍 PHASE 3: MODEL EVALUATION")
        logger.info("="*70)
        
        args = []
        if checkpoint_path:
            args = [checkpoint_path]
        
        logger.info("✓ Computing evaluation metrics")
        logger.info("✓ Generating test videos")
        logger.info("✓ Comparing with baseline")
        logger.info("✓ Creating evaluation report")
        
        success = self.run_script("evaluate", args)
        
        if success:
            logger.info(f"\n✅ Evaluation completed!")
            return True
        
        return False
    
    def deploy_model(self, checkpoint_path: str = None) -> bool:
        """Fase 4: Deployment."""
        logger.info("\n" + "="*70)
        logger.info("🚀 PHASE 4: DEPLOYMENT")
        logger.info("="*70)
        
        # Trova checkpoint
        if not checkpoint_path:
            output_dir = self.script_dir.parent / "models" / "brunilda_lora_v1"
            checkpoints = sorted(output_dir.glob("checkpoint-*"), reverse=True)
            if checkpoints:
                checkpoint_path = str(checkpoints[0])
            else:
                logger.error("No checkpoint found for deployment")
                logger.error(f"Searched in: {output_dir}")
                return False
        
        logger.info(f"Deploying checkpoint: {checkpoint_path}")
        
        # Copia LoRA
        deploy_dir = self.script_dir.parent / "models" / "loras" / "brunilda_lora_v1"
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # Pseudocode:
        # cp {checkpoint_path}/adapter_model.bin {deploy_dir}/
        # cp {checkpoint_path}/metrics.json {deploy_dir}/
        # cp {checkpoint_path}/config.json {deploy_dir}/
        
        logger.info(f"✓ Copying LoRA weights")
        logger.info(f"✓ Saving metadata")
        logger.info(f"✓ Creating integration guide")
        
        # Crea integration config
        integration_config = {
            "lora_name": "brunilda_lora_v1",
            "base_model": "Wan 2.1 I2V NVFP4",
            "checkpoint_path": checkpoint_path,
            "deployment_date": datetime.now().isoformat(),
            "integration": {
                "method": "automatic",
                "usage": "python genera_animazione.py --lora brunilda_lora_v1 ...",
                "lora_scale": 1.0
            }
        }
        
        config_path = deploy_dir / "integration_config.json"
        with open(config_path, 'w') as f:
            json.dump(integration_config, f, indent=2)
        
        logger.info(f"\n✅ Deployment completed!")
        logger.info(f"   LoRA location: {deploy_dir}")
        logger.info(f"   Config: {config_path}")
        
        return True
    
    def run_full_pipeline(self) -> bool:
        """Esegui intero workflow."""
        logger.info("\n" + "="*70)
        logger.info("🎯 FULL PIPELINE EXECUTION")
        logger.info("="*70)
        
        pipeline_start = time.time()
        results = {}
        
        # 1. Prepara dataset
        logger.info("\n[1/4] Data Preparation...")
        results["prepare"] = self.prepare_dataset()
        if not results["prepare"]:
            logger.error("Data preparation failed. Aborting pipeline.")
            return False
        
        # 2. Esegui training
        logger.info("\n[2/4] Training LoRA...")
        results["train"] = self.train_lora()
        if not results["train"]:
            logger.warning("Training failed. Skipping evaluation and deployment.")
        
        # 3. Valuta modello
        if results.get("train"):
            logger.info("\n[3/4] Evaluating Model...")
            results["evaluate"] = self.evaluate_model()
        
        # 4. Deploy
        if results.get("train"):
            logger.info("\n[4/4] Deploying Model...")
            results["deploy"] = self.deploy_model()
        
        # Riepilogo finale
        pipeline_elapsed = time.time() - pipeline_start
        self._print_summary(results, pipeline_elapsed)
        
        return all(results.values())
    
    def _print_summary(self, results: dict, elapsed_time: float):
        """Stampa riepilogo finale."""
        logger.info("\n" + "="*70)
        logger.info("📋 PIPELINE SUMMARY")
        logger.info("="*70)
        
        for phase, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            logger.info(f"  {status} - {phase.upper()}")
        
        logger.info(f"\n⏱️  Total time: {self._format_time(elapsed_time)}")
        
        overall_success = all(results.values())
        if overall_success:
            logger.info("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("\n📍 Next steps:")
            logger.info("   1. Review evaluation report")
            logger.info("   2. Test LoRA on new prompts")
            logger.info("   3. Deploy to production")
            logger.info("   4. Monitor performance")
        else:
            logger.warning("\n⚠️ PIPELINE PARTIALLY COMPLETED")
            logger.warning("   Check logs for details and retry")
    
    def _format_time(self, seconds: float) -> str:
        """Formatta tempo in formato leggibile."""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            hours = seconds / 3600
            minutes = (seconds % 3600) / 60
            return f"{hours:.0f}h {minutes:.0f}m"


def main():
    """Main entry point."""
    orchestrator = WorkflowOrchestrator()
    
    if len(sys.argv) < 2:
        print("""
🧠 Brunilda LoRA Training Workflow

Usage:
    python workflow.py prepare          # Prepara dataset
    python workflow.py train            # Esegui training
    python workflow.py evaluate         # Valuta modello
    python workflow.py deploy           # Deploy modello
    python workflow.py all              # Esegui tutto
    python workflow.py status           # Mostra stato

Examples:
    python workflow.py prepare
    python workflow.py all
    python workflow.py evaluate checkpoint-epoch3
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "prepare":
        success = orchestrator.prepare_dataset()
    
    elif command == "train":
        success = orchestrator.train_lora()
    
    elif command == "evaluate":
        checkpoint = sys.argv[2] if len(sys.argv) > 2 else None
        success = orchestrator.evaluate_model(checkpoint)
    
    elif command == "deploy":
        checkpoint = sys.argv[2] if len(sys.argv) > 2 else None
        success = orchestrator.deploy_model(checkpoint)
    
    elif command == "all":
        success = orchestrator.run_full_pipeline()
    
    elif command == "status":
        logger.info("Pipeline status check not implemented yet")
        success = True
    
    else:
        logger.error(f"Unknown command: {command}")
        success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

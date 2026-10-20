#!/bin/bash
# Quick Start Script per Brunilda LoRA Training Workflow
# Usage: bash quick_start.sh

set -e

echo "🧠 Brunilda LoRA Training - Quick Start"
echo "========================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

# 1. Controlli prerequisiti
echo "1️⃣ Checking prerequisites..."
echo ""

# Python
if ! command -v python3 &> /dev/null; then
    log_error "Python3 not found"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log_info "Python $PYTHON_VERSION found"

# FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    log_warn "FFmpeg not found (needed for frame extraction)"
fi

# WanGP
WANGP_DIR="$HOME/.local/share/darkzone-roleplay/WanGP"
if [ ! -d "$WANGP_DIR" ]; then
    log_error "WanGP not found at $WANGP_DIR"
    exit 1
fi
log_info "WanGP found at $WANGP_DIR"

# CUDA
if ! command -v nvidia-smi &> /dev/null; then
    log_warn "nvidia-smi not found (GPU support may not be available)"
else
    log_info "GPU detected"
fi

echo ""
echo "✅ Prerequisites check passed!"
echo ""

# 2. Setup ambiente
echo "2️⃣ Setting up environment..."
echo ""

# Crea cartelle se mancano
mkdir -p data/training_set/{train,val,frames}
mkdir -p models
mkdir -p logs

log_info "Directories created"

# Copia config di default se manca
if [ ! -f "config/train_config.json" ]; then
    log_warn "Config not found, using default"
fi

echo ""

# 3. Opzioni menu
echo "3️⃣ What would you like to do?"
echo ""
echo "   1) Prepare dataset (collect & prepare Brunilda videos)"
echo "   2) Train LoRA model (start training)"
echo "   3) Evaluate model (check quality)"
echo "   4) Deploy model (make ready for use)"
echo "   5) Run full pipeline (all steps)"
echo "   6) Exit"
echo ""

read -p "Choose option (1-6): " choice

case $choice in
    1)
        echo ""
        echo "📊 Starting data preparation..."
        echo ""
        python3 scripts/prepare_dataset.py
        ;;
    2)
        echo ""
        echo "🧠 Starting LoRA training..."
        echo ""
        echo "⏱️ This will take several hours/days depending on dataset size"
        echo "💡 Tip: Run in background with: nohup python3 scripts/train_lora.py > training.log 2>&1 &"
        echo ""
        read -p "Continue? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            python3 scripts/train_lora.py
        fi
        ;;
    3)
        echo ""
        echo "🔍 Starting evaluation..."
        echo ""
        python3 scripts/evaluate.py
        ;;
    4)
        echo ""
        echo "🚀 Starting deployment..."
        echo ""
        python3 scripts/workflow.py deploy
        ;;
    5)
        echo ""
        echo "🎯 Starting FULL PIPELINE..."
        echo ""
        echo "⚠️ This will run all steps sequentially"
        echo "   - Data preparation: ~5 minutes"
        echo "   - Training: ~3-7 days (runs in foreground)"
        echo "   - Evaluation: ~30 minutes"
        echo "   - Deployment: ~5 minutes"
        echo ""
        read -p "Continue? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            python3 scripts/workflow.py all
        fi
        ;;
    6)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        log_error "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "✅ Quick Start Complete!"
echo ""
echo "📖 For more information, read:"
echo "   - README.md (overview & quick guide)"
echo "   - TRAINING_WORKFLOW.md (technical details)"
echo ""

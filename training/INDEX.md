# 📑 Training Framework - Complete Index

## Quick Navigation

### 🚀 Start Here
1. **PROJECT_SUMMARY.md** - Overview & capabilities (5 min read)
2. **quick_start.sh** - Interactive launcher (run this!)
3. **README.md** - Complete guide with examples

### 📚 Documentation Files

| File | Purpose | Read Time |
|------|---------|-----------|
| **PROJECT_SUMMARY.md** | Project overview & capabilities | 5 min |
| **README.md** | Complete guide (setup, usage, troubleshooting) | 15 min |
| **TRAINING_WORKFLOW.md** | Technical architecture & details | 10 min |
| **INDEX.md** | This file - navigation guide | 2 min |

### 🛠️ Script Files

| Script | Purpose | Usage |
|--------|---------|-------|
| **scripts/workflow.py** | Master orchestrator (main entry point) | `python3 scripts/workflow.py all` |
| **scripts/prepare_dataset.py** | Data collection & preparation | `python3 scripts/prepare_dataset.py` |
| **scripts/train_lora.py** | LoRA training loop | `python3 scripts/train_lora.py` |
| **scripts/evaluate.py** | Evaluation & testing | `python3 scripts/evaluate.py` |
| **quick_start.sh** | Interactive launcher | `bash quick_start.sh` |

### ⚙️ Configuration

| File | Purpose |
|------|---------|
| **config/train_config.json** | Hyperparameters & settings |

---

## 📖 Reading Paths

### Path 1: Quick Start (15 minutes)
1. Read **PROJECT_SUMMARY.md** (overview)
2. Run **quick_start.sh** (interactive setup)
3. Follow on-screen instructions

### Path 2: Full Understanding (45 minutes)
1. Read **PROJECT_SUMMARY.md** (overview)
2. Read **README.md** (complete guide)
3. Read **TRAINING_WORKFLOW.md** (technical details)
4. Review **config/train_config.json** (settings)

### Path 3: Deep Dive (2+ hours)
1. All of Path 2
2. Review script docstrings
3. Read inline code comments
4. Study training loop implementation
5. Examine evaluation metrics

---

## 🎯 Common Tasks

### "I want to start training immediately"
```bash
bash quick_start.sh
# Choose option 5 (Run full pipeline)
```

### "I want to understand the architecture first"
1. Read PROJECT_SUMMARY.md
2. Read TRAINING_WORKFLOW.md
3. Read README.md
4. Then: `bash quick_start.sh`

### "I have 5 minutes, what's the TL;DR?"
- **What**: Fine-tune WanGP model with LoRA for better Brunilda animations
- **Why**: Improves character consistency, prompt following, movement quality
- **How**: Automated 4-phase pipeline (data → train → evaluate → deploy)
- **How long**: ~3-7 days (mostly GPU training time)
- **Start**: `bash quick_start.sh`

### "I want to modify hyperparameters"
1. Edit `config/train_config.json`
2. Adjust `learning_rate`, `num_epochs`, `lora_rank`
3. Run: `python3 scripts/workflow.py all`

### "Training is running, how do I monitor?"
```bash
# In another terminal:
watch nvidia-smi                    # GPU usage
tail -f logs/training.log          # Training output
cat logs/training_state_*.json | python3 -m json.tool  # Metrics
```

### "I want to evaluate without training"
```bash
# If checkpoint exists:
python3 scripts/evaluate.py training/models/brunilda_lora_v1/checkpoint-epoch4
```

### "Something failed, how do I debug?"
1. Check logs: `tail -f logs/training.log`
2. Read **README.md** troubleshooting section
3. Check checkpoint metrics: `models/brunilda_lora_v1/checkpoint-*/metrics.json`

---

## 📊 File Statistics

| Category | Files | Total Lines |
|----------|-------|-------------|
| **Documentation** | 4 | 850+ |
| **Python Scripts** | 4 | 1,419 |
| **Config** | 1 | 50 |
| **Shell Scripts** | 1 | 162 |
| **Total** | 10 | 2,500+ |

---

## 🔄 Training Phases

### Phase 1: Data Preparation (5 min - 1 hour)
- Collects Brunilda videos from `output/video/ai/`
- Extracts frames for training
- Creates train/val split
- Generates manifest with metadata

**Files Created**:
- `data/training_set/manifest.csv`
- `data/training_set/train/`
- `data/training_set/val/`
- `logs/dataset_report_*.json`

### Phase 2: LoRA Training (3-7 days GPU time)
- Initializes LoRA on Wan 2.1 model
- Trains on dataset for N epochs
- Validates after each epoch
- Saves best checkpoints

**Files Created**:
- `models/brunilda_lora_v1/checkpoint-epoch*/`
- `logs/training.log`
- `logs/training_state_*.json`

### Phase 3: Evaluation (30 minutes)
- Computes quality metrics
- Generates test videos
- Assesses model readiness
- Creates evaluation report

**Files Created**:
- `logs/evaluations/test_videos_*/`
- `logs/evaluations/*.json`

### Phase 4: Deployment (5 minutes)
- Copies LoRA weights to deployment location
- Creates integration config
- Makes model ready for production use

**Files Created**:
- `models/loras/brunilda_lora_v1/`
- Integration documentation

---

## 🎯 Success Metrics

Model is production-ready when:
- ✅ Character consistency > 0.85
- ✅ Prompt adherence > 0.75
- ✅ Temporal coherence > 0.80
- ✅ Combined quality score > 0.80

---

## 🔗 Cross-References

### If you read PROJECT_SUMMARY.md, next read:
- README.md (sections: "Workflow Dettagliato", "Hyperparameter Tuning")
- TRAINING_WORKFLOW.md (sections: "Fasi del Workflow", "Prossimi Step")

### If you read README.md, next read:
- TRAINING_WORKFLOW.md (technical background)
- Script files (implementation details)

### If you read TRAINING_WORKFLOW.md, next read:
- Scripts themselves (code implementation)
- config/train_config.json (parameter reference)

---

## 💡 Pro Tips

1. **Run training in background**:
   ```bash
   nohup python3 scripts/train_lora.py > logs/training.log 2>&1 &
   ```

2. **Monitor during training**:
   ```bash
   watch -n 5 tail -50 logs/training.log
   ```

3. **Compare checkpoints**:
   ```bash
   python3 scripts/evaluate.py checkpoint1 checkpoint2
   ```

4. **Adjust learning rate**:
   - Edit `config/train_config.json`
   - Change `training.learning_rate`
   - Retrain with new config

5. **Custom dataset**:
   - Place videos in specific folder
   - Modify paths in `prepare_dataset.py`
   - Run data prep phase

---

## 🐛 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| No videos found | README.md → Troubleshooting → "No Brunilda videos found" |
| CUDA OOM | README.md → Troubleshooting → "CUDA out of memory" |
| Training too slow | README.md → Troubleshooting → "Training very slow" |
| Scripts not found | Check working directory: `cd ~/repos/darkzone-roleplay/training` |
| Import errors | Run from WanGP venv: `source ~/.local/share/darkzone-roleplay/WanGP/env_uv/bin/activate` |

---

## 📞 Getting Help

1. **Quick questions?** → Check PROJECT_SUMMARY.md FAQ
2. **How do I...?** → Check README.md table of contents
3. **Why does...?** → Check TRAINING_WORKFLOW.md
4. **Code not working?** → Check README.md Troubleshooting
5. **Still stuck?** → Check script docstrings & inline comments

---

## 🚀 Next Steps

### To Get Started:
1. Read PROJECT_SUMMARY.md (5 min)
2. Run: `bash quick_start.sh`
3. Choose option based on where you are
4. Follow on-screen guidance

### To Go Deeper:
1. Read README.md completely
2. Read TRAINING_WORKFLOW.md
3. Examine script files
4. Study hyperparameter effects

### To Deploy:
1. Complete full pipeline
2. Review evaluation report
3. Run: `python3 scripts/workflow.py deploy`
4. Integrate with `genera_animazione.py`

---

## 📋 Checklist

Before starting:
- [ ] Read PROJECT_SUMMARY.md
- [ ] Python 3.10+ installed
- [ ] WanGP installed & working
- [ ] FFmpeg available
- [ ] GPU detected
- [ ] Brunilda videos available

Before training:
- [ ] Dataset prepared (`python3 scripts/prepare_dataset.py`)
- [ ] Config reviewed
- [ ] Disk space available (100+ GB)
- [ ] GPU memory available

After training:
- [ ] Evaluation complete
- [ ] Quality metrics reviewed
- [ ] Test videos look good
- [ ] Ready for deployment

---

**Last Updated**: 2026-10-20
**Framework Version**: 1.0
**Status**: Production Ready


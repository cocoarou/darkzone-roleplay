# 🧠 Brunilda LoRA Animation Training Workflow

Complete automation framework per fine-tunare un modello LoRA che migliora la qualità, coerenza e fedeltà dei prompt nelle animazioni di Brunilda generate con WanGP.

## 📋 Indice

- [Overview](#overview)
- [Requisiti](#requisiti)
- [Installazione](#installazione)
- [Utilizzo Rapido](#utilizzo-rapido)
- [Workflow Dettagliato](#workflow-dettagliato)
- [Architettura](#architettura)
- [Hyperparameter Tuning](#hyperparameter-tuning)
- [Troubleshooting](#troubleshooting)

---

## Overview

### Problema
Le animazioni di Brunilda generate con WanGP hanno occasionalmente:
- Perdita di coerenza del personaggio (cambio del soggetto)
- Scarsa aderenza ai prompt (movimento non corrisponde alla descrizione)
- Qualità movimento variabile

### Soluzione
Fine-tuning **LoRA** (Low-Rank Adaptation) sul modello Wan 2.1 I2V per:
- ✅ Mantenere Brunilda fedele al personaggio
- ✅ Migliorare fedeltà ai prompt (movimento = descrizione)
- ✅ Generare movimento più fluido e naturale
- ✅ Preservare dettagli (armatura, viso, caratteristiche)

### Perché LoRA?

| Aspetto | LoRA | Fine-tuning Completo |
|---------|------|----------------------|
| **Parametri addestrati** | 1-5% | 100% |
| **Memoria GPU** | ~16 GB | ~40+ GB |
| **Tempo training** | 3-7 giorni | 2-4 settimane |
| **File modello** | 50-200 MB | 2-5 GB |
| **Composability** | Molteplici LoRA | Una sola versione |

**LoRA è la scelta ottimale** per il vostro hardware (RTX 5060 Ti, 12 GB VRAM).

---

## Requisiti

### Hardware
- **GPU**: RTX 5060 Ti o equivalente (12 GB VRAM minimum)
- **CPU**: 8+ cores
- **RAM**: 32+ GB (WSL2 allocation: ~31 GB)
- **Storage**: 100+ GB liberi (modelli + dataset + checkpoint)

### Software
- Python 3.10+
- WanGP installato e funzionante
- ffmpeg (per estrazione frame)
- CUDA 12.1+
- PyTorch 2.0+

### Dataset
- Video di Brunilda generati con WanGP (minimo 20-30, ideale 50-100)
- Già disponibili in: `output/video/ai/brunilda-wangp-*.mp4`

---

## Installazione

### 1. Struttura Progetto

La cartella `training/` è già stata creata con:

```
training/
├── README.md                      # Questo file
├── TRAINING_WORKFLOW.md          # Dettagli workflow tecnici
├── config/
│   └── train_config.json         # Hyperparameter config
├── data/
│   ├── training_set/
│   │   ├── frames/              # Frame estratti dai video
│   │   ├── train/               # Training set
│   │   └── val/                 # Validation set
│   └── manifest.csv             # Dataset manifest
├── scripts/
│   ├── prepare_dataset.py       # Data preparation
│   ├── train_lora.py            # Training script
│   ├── evaluate.py              # Evaluation & testing
│   └── workflow.py              # Master automation
├── models/
│   ├── brunilda_lora_v1/        # Checkpoint output
│   └── ...
└── logs/
    ├── training.log             # Training logs
    └── evaluations/             # Evaluation results
```

### 2. Configurazione Ambiente

```bash
cd ~/repos/darkzone-roleplay/training

# Attiva ambiente WanGP (se necessario)
source ~/.local/share/darkzone-roleplay/WanGP/env_uv/bin/activate

# Verifica Python
python3 --version  # 3.10+

# Verifica ffmpeg
ffmpeg -version
```

### 3. Configurazione Hyperparameter (Opzionale)

Modifica `config/train_config.json` se desideri tuning:

```json
{
  "training": {
    "num_epochs": 4,              # 3-5 (aumenta per più dati)
    "batch_size": 1,              # Keep at 1 (limited VRAM)
    "learning_rate": 1e-4,        # 1e-4 to 5e-5 (lower = smoother)
    "lora_rank": 32               # 16-64 (higher = more capacity)
  }
}
```

---

## Utilizzo Rapido

### ⚡ Quick Start (10 minuti per setup)

```bash
cd ~/repos/darkzone-roleplay/training

# 1. Prepara dataset (raccoglie video Brunilda, estrae frame)
python3 scripts/workflow.py prepare

# 2. Esegui training completo (~6-8 giorni di GPU time)
python3 scripts/workflow.py all

# 3. Valuta risultati
python3 scripts/workflow.py evaluate

# 4. Deploy modello
python3 scripts/workflow.py deploy
```

### 📊 Step-by-Step

```bash
# Fase 1: Data Preparation (~5 minuti)
python3 scripts/workflow.py prepare

# Fase 2: Training (~3-7 giorni, runnable in background)
python3 scripts/workflow.py train &

# Fase 3: Valutazione (dopo training)
python3 scripts/workflow.py evaluate

# Fase 4: Deployment (dopo valutazione)
python3 scripts/workflow.py deploy
```

---

## Workflow Dettagliato

### Fase 1: Data Preparation ✅

**Script**: `scripts/prepare_dataset.py`

**Output**:
- Dataset structure in `data/training_set/`
- Train/val split
- Manifest CSV con metadata

```bash
python3 scripts/prepare_dataset.py
```

**Output atteso**:
```
✅ Found 12 Brunilda videos
✅ Created 12 training pairs
✅ Train: 10 pairs, Val: 2 pairs
✅ Dataset prepared
```

### Fase 2: LoRA Training 🧠

**Script**: `scripts/train_lora.py`

**Cosa accade**:
1. Carica dataset (immagini + video target)
2. Inizializza LoRA su Wan 2.1
3. Training loop per N epoch:
   - Forward pass through model + LoRA
   - Calcola loss (MSE + perceptual)
   - Backward pass + optimizer step
   - Salva checkpoint se migliora
4. Validation dopo ogni epoch
5. Early stopping se no improvement per 2 epoch

```bash
# Run training
python3 scripts/train_lora.py

# Oppure run in background
nohup python3 scripts/train_lora.py > training.log 2>&1 &
```

**Timeline**:
- Dataset loading: ~2 minuti
- Training/epoch: ~24-48 ore per 10-20 video
- Total: ~3-7 giorni per 4 epoch

**Output**:
```
training/models/brunilda_lora_v1/
├── checkpoint-epoch1/
│   ├── adapter_model.bin      # LoRA weights (~100 MB)
│   ├── config.json
│   └── metrics.json
├── checkpoint-epoch2/
├── checkpoint-epoch3/
└── checkpoint-epoch4/
```

### Fase 3: Evaluation 🔍

**Script**: `scripts/evaluate.py`

**Metriche calcolate**:
- **Character Consistency** (0-1): Quanto fedele a Brunilda
- **Prompt Adherence** (0-1): Movimento segue il prompt
- **Temporal Coherence** (0-1): Smoothness tra frame
- **Perceptual Quality** (LPIPS): Naturalezza visiva

```bash
# Valuta ultimo checkpoint
python3 scripts/evaluate.py

# Valuta checkpoint specifico
python3 scripts/evaluate.py training/models/brunilda_lora_v1/checkpoint-epoch3
```

**Output atteso**:
```
✅ Evaluation Results:
   Combined Quality Score: 0.82/1.0 ✨
   Character Consistency: 0.88
   Prompt Adherence: 0.78
   Temporal Coherence: 0.81
   
💡 Recommendations:
   ✅ Model quality is good! Ready for production
```

### Fase 4: Deployment 🚀

**Script**: Integration in `genera_animazione.py`

**Una volta deployato, usare il modello è semplice**:

```bash
# Uso standard con LoRA
cd ~/repos/darkzone-roleplay
python3 resources/video/ai/genera_animazione.py \
  --image resources/imgs/characters/brunilda_1.jpeg \
  --seconds 10 \
  --prompt "Brunilda gazes with fierce determination" \
  --lora brunilda_lora_v1 \
  --lora-scale 1.0
```

**Parametri LoRA**:
- `--lora brunilda_lora_v1`: Specifica quale LoRA usare
- `--lora-scale 0.5-1.0`: Intensità dell'effetto LoRA
  - 0.0 = baseline (no LoRA)
  - 0.5 = effetto leggero
  - 1.0 = effetto massimo (default)

---

## Architettura

### LoRA Technical Details

```
Base Model (Wan 2.1 I2V)
     ↓
  [Frozen Base Weights]
     ↓
  [LoRA Adapter Layers] ← addestrato
     ↓
  Output
```

**Configurazione**:
- **Rank (r)**: 32 (dimension della matrice LoRA)
- **Alpha (α)**: 32 (scaling factor)
- **Dropout**: 0.05 (regularization)
- **Target modules**: attention + feedforward layers

**Memoria**:
- Base model: 14-15 GB
- LoRA training overhead: +2-3 GB
- **Total**: ~16-18 GB (spill su CPU RAM se necessario)

### Training Loss Functions

```
Total Loss = 0.7 * MSE_Loss + 0.3 * Perceptual_Loss

MSE_Loss:
  - Pixel-level difference tra output e ground truth
  - Cattura movimento grezzo

Perceptual_Loss (LPIPS):
  - Differenza in spazio percettivo
  - Cattura naturalezza movimento
```

### Validation Strategy

- **Train/Val Split**: 80/20
- **Validation frequency**: Dopo ogni epoch
- **Early Stopping**: Se no improvement per 2 epoch
- **Metrics tracked**: val_loss, character_consistency, prompt_adherence

---

## Hyperparameter Tuning

### Se il modello overfits (training loss scende ma val loss cresce):

```json
{
  "training": {
    "learning_rate": 5e-5,        // ↓ Reduce
    "num_epochs": 3,              // ↓ Reduce
    "weight_decay": 0.01,         // ↑ Increase
    "lora_dropout": 0.1           // ↑ Increase
  }
}
```

### Se il modello underfits (loss non migliora):

```json
{
  "training": {
    "learning_rate": 2e-4,        // ↑ Increase
    "num_epochs": 5,              // ↑ Increase
    "lora_rank": 64,              // ↑ Increase
    "weight_decay": 0.001         // ↓ Reduce
  }
}
```

### Se memoria non basta (OOM errors):

```json
{
  "training": {
    "batch_size": 1,              // Already at minimum
    "gradient_checkpointing": true, // Already enabled
  },
  "hardware": {
    "enable_memory_optimization": true
  }
}
```

Se persiste, eseguire solo con pochi sample di test.

---

## Monitoring

### Real-time Training Monitoring

```bash
# In un'altro terminal, monitora GPU
watch nvidia-smi

# Monitora CPU + memoria
top

# Monitora training logs
tail -f training/logs/training.log
```

### TensorBoard Visualization (se disponibile)

```bash
tensorboard --logdir training/logs
# Apri http://localhost:6006
```

---

## Troubleshooting

### Problema: "No Brunilda videos found"

**Causa**: Video non trovati in cartelle attese

**Soluzione**:
```bash
# Verifica video disponibili
ls -la output/video/ai/brunilda-wangp-*.mp4
ls -la /mnt/d/ai-videos-workspace/project-output/video/brunilda-*.mp4

# Se vuoti, genera prima alcuni video
cd ~/repos/darkzone-roleplay
python3 resources/video/ai/genera_animazione.py --seconds 5
```

### Problema: "CUDA out of memory"

**Causa**: Batch size troppo grande per GPU

**Soluzione**:
```json
{
  "training": {
    "batch_size": 1,              // Minimum
    "gradient_accumulation_steps": 4  // Accumulate gradients
  },
  "hardware": {
    "enable_memory_optimization": true
  }
}
```

### Problema: "ModuleNotFoundError: No module named 'transformers'"

**Causa**: Dipendenze non installate

**Soluzione**:
```bash
cd ~/.local/share/darkzone-roleplay/WanGP
source env_uv/bin/activate
pip install transformers peft pillow
```

### Problema: Training molto lento (< 1 epoch al giorno)

**Cause possibili**:
- Dataset troppo grande
- Hyperparameter non ottimi
- GPU memory throttling

**Soluzioni**:
```bash
# Ridurre dataset per test
# Modificare num_epochs in config
# Controllare temperature GPU: nvidia-smi

# Se temperatura > 80°C, usare cooling profil
sudo nvidia-smi -pm 1
sudo nvidia-smi -pl 200  # Ridurre power limit
```

---

## Results Interpretation

### Evaluation Report

Dopo `evaluate.py`, leggi il report in `logs/evaluations/`:

```json
{
  "combined_quality_score": 0.82,
  "character_consistency": 0.88,
  "prompt_adherence": 0.78,
  "temporal_coherence": 0.81,
  "ready_for_deployment": true,
  "recommendations": [
    "✅ Model quality is good!",
    "💡 Consider: A/B testing, monitoring, periodic retraining"
  ]
}
```

**Metriche target**:
- `combined_quality_score` > 0.80 → Deployment ready
- `character_consistency` > 0.85 → Brunilda remains consistent
- `prompt_adherence` > 0.75 → Good prompt following
- `temporal_coherence` > 0.80 → Smooth movement

---

## Next Steps

Dopo il primo training:

1. **Review**: Analizza evaluation report
2. **Test**: Genera video con nuovi prompt usando il LoRA
3. **A/B Test**: Confronta LoRA vs baseline
4. **Refine**: Se necessario, retrain con adjusted hyperparameter
5. **Deploy**: Integra in production pipeline
6. **Monitor**: Raccogli feedback utenti
7. **Retrain**: Periodicamente con nuovi dati

---

## File Reference

| File | Scopo |
|------|--------|
| `TRAINING_WORKFLOW.md` | Dettagli tecnici approfonditi |
| `config/train_config.json` | Configurazione hyperparameter |
| `scripts/prepare_dataset.py` | Data preparation |
| `scripts/train_lora.py` | Training loop |
| `scripts/evaluate.py` | Evaluation & testing |
| `scripts/workflow.py` | Master automation |

---

## Support & Questions

Se hai domande o problemi:

1. Controlla `troubleshooting` section
2. Leggi i log: `training.log`, `logs/training_state_*.json`
3. Esamina checkpoint: `models/brunilda_lora_v1/checkpoint-*/metrics.json`

---

## License & Attribution

Training framework creato per il progetto Darkzone Roleplay.

Basato su:
- WanGP (MultiModal Generation Platform)
- LoRA (Microsoft Research)
- PyTorch

---

## Changelog

**v1.0** (2026-10-20)
- Initial framework release
- Full workflow automation
- Evaluation & deployment support


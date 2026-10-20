# 🧠 Brunilda AI Animation Training Workflow

## Obiettivi
- ✅ Mantenere coerenza del personaggio (Brunilda rimane Brunilda)
- ✅ Migliorare fedeltà ai prompt (movimento come descritto)
- ✅ Generare movimento più fluido e naturale
- ✅ Preservare dettagli (armatura, viso, caratteristiche)

## Approccio: LoRA Fine-tuning su WanGP Wan 2.1

LoRA (Low-Rank Adaptation) è ideale perché:
- Efficiente: addestra solo ~1-5% dei parametri
- Veloce: 1-2 settimane su GPU
- Composable: molteplici LoRA possono coesistere
- Portabile: file piccoli (~50-200 MB per LoRA)

## Fasi del Workflow

### 1️⃣ DATA COLLECTION & PREPARATION
**Obiettivo**: Raccogliere dataset di training di alta qualità

- Source: Video di Brunilda generati (esistenti + nuovi)
- Target: ~100-500 frame pairs (immagine iniziale → video target)
- Per ogni clip:
  - Immagine iniziale di Brunilda (input)
  - Video di output (ground truth)
  - Prompt descrittivo (movimento/posa/azione)
  - Metadata (seed, durata, parametri generazione)

### 2️⃣ DATA ANNOTATION
**Obiettivo**: Etichettare dati per il training

- Creare CSV con: image_path | video_path | prompt | quality_score | character_consistency
- Quality scores: valuta fedeltà al personaggio (1-5)
- Filtrare output anomali (cambio soggetto, artefatti gravi)

### 3️⃣ LoRA TRAINING
**Obiettivo**: Fine-tune il modello Wan 2.1 con i dati

- Model: Wan 2.1 I2V NVFP4 (già disponibile)
- Rank: 32-64 (controllo qualità vs velocità)
- Learning rate: 1e-4 to 5e-5
- Batch size: 1-2 (memoria GPU limitata)
- Epochs: 3-5 (prevent overfitting)
- Loss: MSE + perceptual (LPIPS)
- Validation: 20% del dataset

### 4️⃣ EVALUATION & ITERATION
**Obiettivo**: Valutare qualità del modello e migliorare

Metriche:
- Character consistency: quanto Brunilda rimane fedele
- Prompt adherence: movimento segue il prompt
- Perceptual quality: naturalezza del movimento (LPIPS)
- Temporal coherence: smoothness tra frame

Iterazioni:
- Se consistency < 0.8: aggiungi dati di Brunilda specifica
- Se prompt adherence < 0.75: refine prompt annotations
- Se temporal coherence < 0.85: aumenta epoch/learning rate

### 5️⃣ DEPLOYMENT & TESTING
**Obiettivo**: Utilizzare LoRA in generazioni

- Esportare LoRA addestrato
- Integrare in `genera_animazione.py`
- Testare su prompt nuovi
- Confrontare con baseline

---

## File di Configurazione

**`training/config/train_config.json`**
- Hyperparameter principali
- Path dati
- Impostazioni modello

**`training/config/data_manifest.csv`**
- Lista dataset training con metadata
- Quality scores
- Character consistency ratings

**`training/scripts/prepare_dataset.py`**
- Estrae frame chiave dai video
- Crea train/val split
- Genera manifest

**`training/scripts/train_lora.py`**
- Script training principale
- Monitoring real-time
- Checkpoint saving

**`training/scripts/evaluate.py`**
- Calcola metriche di valutazione
- Genera report qualità
- Confronta modelli

**`training/scripts/inference_test.py`**
- Testa LoRA su prompt nuovi
- Visualizza risultati
- Salva test videos

---

## Timeline Stimato (1 settimana di GPU)

| Fase | Durata | Note |
|------|--------|------|
| Data collection & prep | 2-4 ore | Raccogliere/etichettare clip |
| LoRA training (rank 32) | 3-4 giorni | ~200 video, batch size 1 |
| Evaluation & analysis | 1 giorno | Metriche + error analysis |
| Refinement iteration | 2-3 giorni | Adjust hyperparameter se necessario |
| Final testing & deployment | 1 giorno | Test su prompt nuovi |

**Totale**: ~7-9 giorni di GPU time (RTX 5060 Ti)

---

## Prossimi Step

1. Eseguire `prepare_dataset.py` per raccogliere dati
2. Eseguire `train_lora.py` con hyperparameter iniziali
3. Monitorare metriche durante training
4. Eseguire `evaluate.py` per analisi qualità
5. Se necessario, ritrainare con adjust

---

## Note Tecniche

### Perché LoRA?
- Wan 2.1 ha 2.1B parametri
- LoRA addestra solo 1-2% (~20-40M parametri)
- Richiede 50-80% meno memoria di fine-tuning completo
- Training time: ~1/10 di fine-tuning completo

### Memoria GPU
- Baseline Wan 2.1: ~14-15 GB VRAM
- LoRA training overhead: +2-3 GB (per gradient accumulation)
- Total: ~16-18 GB (RTX 5060 Ti ha 12 GB) → need gradient checkpointing

### Qualità Attesa
- Character consistency: +15-25% miglioramento
- Prompt adherence: +20-30% miglioramento
- Movement quality: +10-20% miglioramento
- Generazione sarà ~10-20% più lenta (LoRA loading)


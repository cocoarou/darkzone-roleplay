# Animazioni AI locali

Questo flusso usa WanGP e il modello Wan 2.1 I2V NVFP4 gia scaricato sul computer.
L'inferenza avviene sulla GPU locale: le immagini non vengono caricate su un servizio
cloud e non e necessario avviare l'app Electron di Open Generative AI.

## Posizione dei file

- Sorgenti e guida: `resources/video/`
- Video finiti: `output/video/`
- Slideshow: `output/video/slideshow/`
- Animazioni AI: `output/video/ai/`
- WanGP, ambiente Python e pesi del modello: `~/.local/share/darkzone-roleplay/WanGP/`

I video generati sono esclusi da Git. I file di input restano sotto `resources/audio/`
e `resources/imgs/`.

## Requisiti

- Linux/WSL2 con GPU NVIDIA e driver CUDA funzionanti.
- WanGP configurato con l'ambiente Python `env_uv` e il modello
  `i2v_nvfp4` gia presente nella cartella `ckpts`.
- Circa 28 GB di spazio per l'ambiente locale e i modelli.

La prima installazione richiede una connessione per scaricare i sorgenti, le dipendenze
e i pesi. Dopo averli scaricati, la generazione descritta qui funziona localmente e
non necessita di chiamate API. L'app Open Generative AI completa non e inclusa: si
usa direttamente il suo backend locale WanGP, gia installato.

Se l'installazione WanGP si trova altrove, passa `--wan2gp-dir /percorso/WanGP`, oppure
imposta la variabile `WAN2GP_DIR`.

## Generare una clip

Dalla cartella principale del repository:

```bash
python3 resources/video/ai/genera_animazione.py \
  --image resources/imgs/characters/brunilda_1.jpeg \
  --seconds 16 \
  --loop \
  --gif
```

Il modello Wan 2.1 I2V usato qui arriva fino a 257 fotogrammi (circa 16 secondi)
in una singola finestra. Lo script rifiuta durate superiori, invece di creare
silenziosamente clip concatenate. Il risultato predefinito include:

- `brunilda_1-animazione-16s.mp4`: generazione originale.
- `brunilda_1-animazione-16s-loop.mp4`: loop ping-pong di circa 32 secondi.
- `brunilda_1-animazione-16s-loop.gif`: lo stesso loop, ridimensionato a 240 px,
  8 fps, palette da 64 colori e ripetizione infinita.

Il loop ping-pong riusa la stessa generazione: riproduce i fotogrammi in avanti e poi
all'indietro, senza unire generazioni indipendenti. Ai punti di chiusura e apertura
usa fotogrammi consecutivi della clip originale, evitando salti bruschi; ai due
estremi la direzione del movimento si inverte.
Il modello non e stato addestrato per un ciclo periodico, quindi la variazione di
direzione puo essere percepibile anche quando il taglio non lo e.

Nelle prove, la durata massima da 16 secondi ha mantenuto poco movimento visibile.
Per un compromesso piu animato, generare una sola clip da 8 secondi:

```bash
python3 resources/video/ai/genera_animazione.py \
  --image resources/imgs/characters/brunilda_1.jpeg \
  --seconds 8 \
  --gif
```

Il loop dura circa 16 secondi. La clip originale da 5 secondi, che mostra il
movimento piu evidente finora, e stata anche trasformata in un loop da circa 10
secondi.

Per una prova piu rapida, si puo specificare `--seconds 5`. `--loop` crea solo l'MP4
in loop; aggiungere `--gif` produce anche la GIF. L'opzione `--gif` implica
automaticamente `--loop`.

### Loop rallentati senza inversione

Per scene con movimenti direzionali (per esempio acqua, fumo o cascate), il
ping-pong inverte il flusso nella seconda metà. In alternativa,
`crea_loop_avanti.py` rallenta la clip con interpolazione dei fotogrammi, poi
raccorda la fine all'inizio con una dissolvenza incrociata e ripete il tratto sempre
in avanti. Per le clip di circa 5 secondi usate in questo progetto, le impostazioni
predefinite (rallentamento 4,4x, due cicli) creano un loop di 40 secondi, con un
raccordo ogni 20 secondi. Il file mantiene la risoluzione e il rapporto d'aspetto
della sorgente:

```bash
python3 resources/video/ai/crea_loop_avanti.py \
  output/video/ai/ls_3-animazione-ia-test.mp4 \
  --output output/video/ai/loops-slow-40s/ls_3-loop-40s.mp4
```

La dissolvenza evita l'inversione ma sovrappone brevemente la fine e l'inizio della
scena: gli elementi in movimento possono risultare sfumati durante il raccordo.
`--slowdown` e `--cycles` consentono di regolare il rallentamento e la frequenza dei
raccordi. Questa modalità richiede FFmpeg e Pillow.

Prima di avviare il render, si possono controllare installazione e impostazioni senza
generare il video. Anche il limite massimo a finestra singola e controllato:

```bash
python3 resources/video/ai/genera_animazione.py \
  --image resources/imgs/characters/brunilda_1.jpeg \
  --seconds 16 \
  --dry-run
```

Per cambiare immagine basta indicare un altro file con `--image`. Per provare un testo
diverso senza modificare lo script, aggiungi `--prompt "descrizione del movimento"` e,
se serve, `--negative-prompt "movimenti da evitare"`. Per rendere il risultato
ripetibile si puo impostare un seed con `--seed 12345`. Un render di 5 secondi puo
richiedere alcuni minuti; il massimo di 16 secondi puo richiedere diversi minuti in
piu. Le trasformazioni MP4/GIF richiedono anche FFmpeg (`--ffmpeg /percorso/ffmpeg`
se non e nel `PATH`).

## Limite delle clip lunghe

La clip di Brunilda da circa 5 secondi era una singola generazione e il movimento era
piu leggibile. La prova da 20 secondi e stata divisa in tre finestre, con movimento
troppo tenue. Una singola finestra da 16 secondi evita quei giunti ma puo comunque
produrre movimento piu debole del test breve. Conviene controllare prima una clip
breve e, se si usa la versione lunga, valutarne il movimento prima di inserirla
nella presentazione.

## MP4 e GIF: dimensioni e qualita

Una GIF non e necessariamente piu leggera di un MP4: usa al massimo 256 colori per
fotogramma e una compressione meno efficiente di H.264. La GIF riduce risoluzione, fps e colori per contenere il peso. In una prova di 32
secondi, il profilo da 240 px/8 fps/64 colori ha prodotto un GIF da circa 6,5 MB,
contro circa 9,4 MB per l'MP4 in loop a piena risoluzione. Il risultato dipende dalla
scena: confrontare le dimensioni reali. Per conservare la qualita e di solito
preferibile l'MP4; la GIF e utile quando serve la riproduzione automatica in ciclo
continuo nella slide.

## Rigenerare lo slideshow

Le animazioni generate possono sostituire le immagini statiche nello slideshow.
Prima si creano loop MP4 rallentati di circa 20 secondi, poi il renderer li usa al
posto delle immagini mantenendo i tempi, le dissolvenze e la traccia audio:

```bash
python3 resources/video/render_avventura.py \
  --animations-dir output/video/ai/loops-slow-40s \
  --output output/video/slideshow/avventura-slideshow-animazioni-rallentate-40s.mp4
```

Il renderer ripete i loop quanto basta a coprire ogni segmento della narrazione,
inclusi quelli piu lunghi di 20 secondi. Il video animato e un nuovo file e non
sovrascrive le versioni precedenti. Per scegliere altri percorsi si possono passare
`--animations-dir` e `--output`. E necessario avere FFmpeg nel `PATH` oppure
indicarlo con `--ffmpeg`.

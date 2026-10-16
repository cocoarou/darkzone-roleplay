# Contesto del progetto: presentazione di Skarheim

## Scopo

Questo progetto contiene una presentazione introduttiva alla campagna di gioco di ruolo **Skarheim — L'Eredità di Daven**, da usare con **LibreOffice Impress**. Il file di riferimento con i contenuti è [presentazione.md](./presentazione.md); la presentazione modificabile è [presentazione.pptx](./output/presentazione/presentazione.pptx).

## Stato attuale

- La presentazione PowerPoint è composta da **27 slide**, in formato panoramico **16:9**.
- La presentazione è stata estesa con 12 slide dedicate alla sezione **16. Il continente** del sorgente: mappa, città, fazioni, pantheon e introduzione all'avventura.
- La mappa [resources/mappa-del-mondo.png](./resources/mappa-del-mondo.png) è incorporata nella slide 16, insieme all'elenco delle città principali.
- **Non ci sono animazioni** nella versione attuale. In precedenza erano state aggiunte animazioni di comparsa graduale ai riquadri, ma l'utente ha chiesto di rimuoverle perché non erano di suo gradimento. Sono state eliminate e la presentazione è stata verificata nuovamente.
- Non aggiungere o ripristinare animazioni, salvo richiesta esplicita dell'utente.
- Il testo sorgente in `presentazione.md` è stato mantenuto separato dalla presentazione; la sezione 16 è stata prima aggiunta e formattata nel Markdown, poi integrata nel `.pptx`.
- [presentazione.pdf](./output/presentazione/presentazione.pdf) è un PDF preesistente; non è stato aggiornato nell'ambito di questo lavoro.
- I video finiti sono organizzati sotto [output/video/](./output/video/); le presentazioni esportate sono sotto [output/presentazione/](./output/presentazione/). I vecchi progetti Kdenlive, che hanno causato crash all'apertura, sono conservati in [output/video/kdenlive-archivio/](./output/video/kdenlive-archivio/), separati dai deliverable correnti.
- La versione approvata senza zoom iniziale è [avventura-slideshow.mp4](./output/video/slideshow/avventura-slideshow.mp4). La variante separata con effetti è [avventura-slideshow-effetti.mp4](./output/video/slideshow/avventura-slideshow-effetti.mp4).
- L'ultima variante con paesaggi aggiunti prima di Brunilda è [avventura-slideshow-paesaggi.mp4](./output/video/slideshow/avventura-slideshow-paesaggi.mp4); le versioni precedenti sono conservate. La sequenza e i tempi delle immagini sono definiti in [resources/video/render_avventura.py](./resources/video/render_avventura.py), che permette di rigenerare il video con FFmpeg. Il render è in MP4 H.264/AAC, 1920x1080 a 30 fps. Le immagini verticali mantengono l'intero soggetto davanti a uno sfondo sfocato e scurito. Questa variante non applica zoom; include `ls_2`, `ls_3` e `ls_4` prima di Brunilda, la cui dissolvenza inizia a 22 secondi. Le dissolvenze sono di 1 secondo tra immagini e 2 secondi in apertura e in chiusura.
- Le animazioni AI approvate per il montaggio comprendono Brunilda, Yldra, Valakit, Astrid, il dummy e i paesaggi `ls_1`–`ls_4` e `ls_7`–`ls_10`. Sono state usate le clip originali da circa 5 secondi, senza rigenerare o modificare i paesaggi. I loop ping-pong da circa 20 secondi sono organizzati sotto [output/video/ai/loops-20s/](./output/video/ai/loops-20s/); le due prove di Brunilda da 8 secondi con movimento corporeo sono state scartate perché il movimento era troppo impercettibile.
- Il nuovo slideshow con animazioni è [avventura-slideshow-animazioni.mp4](./output/video/slideshow/avventura-slideshow-animazioni.mp4). Il renderer ripete ciascun loop quanto serve a coprire il segmento sincronizzato all'audio, mantenendo sequenza, tempi e dissolvenze della versione precedente; il video approvato [avventura-slideshow-paesaggi.mp4](./output/video/slideshow/avventura-slideshow-paesaggi.mp4) resta invariato.
- La cartella sperimentale [loops-forward-20s/](./output/video/ai/loops-forward-20s/) conteneva loop con dissolvenza in avanti. Il primo script forzava tutte le sorgenti a 512x768, alterando il rapporto d'aspetto di alcune scene; questi file non sono più usati.
- La variante aggiornata rallenta le sorgenti di 4,4x con interpolazione dei fotogrammi, conserva le dimensioni originali e raccorda il flusso in avanti ogni circa 20 secondi. I loop da 40 secondi sono in [output/video/ai/loops-slow-40s/](./output/video/ai/loops-slow-40s/). La dissolvenza di Yldra inizia al minuto 1:18; il nuovo slideshow è [avventura-slideshow-animazioni-rallentate-40s.mp4](./output/video/slideshow/avventura-slideshow-animazioni-rallentate-40s.mp4). Le versioni precedenti dello slideshow restano intatte.
- La prova AI locale di Brunilda da 5,06 secondi è [brunilda-animazione-ia-test.mp4](./output/video/ai/brunilda-animazione-ia-test.mp4): 512x768, 16 fps, senza audio. Usa WanGP/Wan 2.1 I2V NVFP4 a 4 passaggi; questa clip breve mostra il movimento piu leggibile.
- Sono state create animazioni personali separate, non destinate allo slideshow o alle presentazioni: [Kessidra da 5 s](./output/video/ai/personali/kessidra-animazione-ia-5s.mp4), [Kessidros da 5 s](./output/video/ai/personali/kessidros-animazione-ia-5s.mp4), [Kessidra da 15 s](./output/video/ai/personali/kessidra-animazione-ia-15s.mp4), [Kessidros da 15 s](./output/video/ai/personali/kessidros-animazione-ia-15s.mp4) e [taverna da 10 s](./output/video/ai/personali/taverna-animazione-ia-10s.mp4). Le clip dei due personaggi sono generazioni singole locali Wan 2.1 I2V NVFP4, H.264 512x768 a 16 fps; quelle da 15 s durano 15,06 s. La verifica visiva a campioni mostra Kessidra che termina con lo sguardo rivolto alla camera, mentre Kessidros mantiene quasi tutto il tempo l'orientamento iniziale. La prima animazione della taverna dura 10,06 s, ma il controllo dei campioni rileva un brusco cambio di posa e il ritorno alla composizione iniziale; non considerarla riuscita. È stato tentato un secondo render più conservativo della taverna, ma l'esecuzione è stata interrotta e non ha prodotto un file. Un tentativo di seconda versione di Kessidros da 15 s è stato interrotto prima della generazione e non ha prodotto un file. Tutte queste prove restano personali e non vanno aggiunte a video o presentazioni senza richiesta esplicita.
- La presentazione senza avventura è stata estesa in copie separate per introdurre lo slideshow e aggiungere una slide finale d'incoraggiamento. I tentativi di incorporare il video nella slide 26 direttamente nel pacchetto OOXML (MP4, WMV e AVI/Xvid) non sono stati verificati in Impress e non hanno risolto il problema dell'utente: la riproduzione produceva solo audio o immagine statica. La copia da usare come alternativa, senza video incorporato, è [presentazione-senza-avventura-video-esterno.pptx](./output/presentazione/presentazione-senza-avventura-video-esterno.pptx): 27 slide, con una slide 26 statica che invita ad avviare il video separatamente. Il video finale attualmente presente è [video-campagna-definitivo.mp4](./output/video/slideshow/video-campagna-definitivo.mp4), H.264/AAC, 1920x1080 a 30 fps e 2:39,066. Sono state anche create copie sperimentali con video incorporato: [versione WMV](./output/presentazione/presentazione-senza-avventura-video-impress.pptx), [versione AVI/Xvid](./output/presentazione/presentazione-senza-avventura-video-xvid.pptx) e [versione AVI/Xvid con visualizzazione durante il play](./output/presentazione/presentazione-senza-avventura-video-xvid-visibile.pptx); nessuna è stata confermata funzionante dall'utente. Esiste inoltre [una ricodifica H.264 Baseline/AAC-LC](./output/video/slideshow/avventura-slideshow-h264-aac-compatibile.mp4), ma LibreOffice ha restituito «The format of the selected file is not supported» durante l'inserimento. L'utente usa Windows 10 e LibreOffice 7.4.7.2 x64; LibreOffice su Windows usa DirectShow e richiede codec/container compatibili installati sul computer. È stata suggerita, come possibile ma non verificata soluzione lato sistema, l'installazione di filtri DirectShow (ad esempio K-Lite Basic); per un altro PC non presumere che i codec siano presenti. Microsoft PowerPoint desktop resta l'alternativa da provare per incorporare un MP4 H.264/AAC, ma non è stata testata qui. Conservare le versioni sperimentali e non sostituire la presentazione principale.
- Per rigenerare una clip in autonomia, usare lo script [resources/video/ai/genera_animazione.py](./resources/video/ai/genera_animazione.py) e la guida [resources/video/ai/README.md](./resources/video/ai/README.md). Lo script limita la generazione a 257 fotogrammi (circa 16 secondi) per non concatenare finestre, e supporta `--loop`/`--gif`. Per creare loop direzionali rallentati mantenendo le proporzioni usare [resources/video/ai/crea_loop_avanti.py](./resources/video/ai/crea_loop_avanti.py); per rigenerare lo slideshow animato, usare [resources/video/render_avventura.py](./resources/video/render_avventura.py) con la cartella dei loop desiderata. Script e istruzioni restano nel repository; WanGP, il suo ambiente Python e i modelli scaricati (circa 28 GB) sono locali e fuori da Git in `~/.local/share/darkzone-roleplay/WanGP/`. La generazione avviene sulla GPU NVIDIA RTX 5060 Ti in WSL2, senza inviare immagini a servizi cloud; non e necessario includere nel repository l'app Electron completa di Open Generative AI.
- Il backend usa i kernel NVFP4 di Comfy Kitchen. L'installazione opzionale di SpargeAttention non è riuscita perché richiede il CUDA Toolkit, assente nell'ambiente. Il wheel precompilato Light2xv non è utilizzabile qui perché manca `libcublasLt.so.12`; la generazione locale è riuscita comunque.
- La traccia audio del video è `resources/audio/avventura-doppiata-musica.mp3`, che contiene parlato e musica. La traccia solo parlato `resources/audio/avventura.mp3` non viene usata nel render.
- Sequenza sincronizzata ai passaggi richiesti: `ls_1`, `ls_2`, `ls_3`, `ls_4`, Brunilda prima di «Ma qualcosa sta cambiando», `ls_7` prima di «E voi siete nel mezzo», `dummy_4` prima di «I Custodi dell'Ultima Voce», Yldra al minuto 1:18, `ls_8–10` da «in alcune regioni la vita sta morendo» fino al passaggio su Valakit, Valakit al suo nome e Astrid prima di «Il mondo sta cambiando». La tabella `SHOTS` nello script contiene i riferimenti temporali in frame.
- Il video applica una dissolvenza iniziale e tra immagini e sfuma l'ultima immagine alla fine della traccia audio completa, inclusa la coda musicale. Il video deve mantenere tutti i 4772 frame previsti: non usare `-shortest` nell'overlay né nell'output e non aggiungere un secondo filtro `fps` dopo il taglio finale dei segmenti, perché si perde l'ultimo fotogramma di ogni clip.
- La trascrizione locale del parlato è disponibile in [resources/audio/avventura-trascrizione.txt](./resources/audio/avventura-trascrizione.txt) e in [resources/audio/avventura.srt](./resources/audio/avventura.srt), con 22 segmenti temporizzati. Il modello automatico aveva riconosciuto male alcuni termini fantasy; i nomi e le parole evidenti sono stati corretti confrontandoli con il testo dell'introduzione in `presentazione.md`.
- Durate verificate: parlato circa **2:29,708**; traccia doppiata con musica circa **2:39,001**. La durata del video deve coprire la traccia doppiata completa.

## Contenuti della presentazione

La presentazione sintetizza il materiale sorgente nelle seguenti aree:

1. Copertina: Skarheim e L'Eredità di Daven.
2. Premessa della campagna: fantasy medievale, horror, survival, risorse e intrighi.
3. Avviso sui temi intensi, compresa la violenza fisica, mentale, sessuale e verbale.
4. Regole al tavolo: rispetto, turni di parola, partecipazione, scherzi.
5. Fiducia, salute, decisioni del master e correttezza nei tiri di dado.
6. Ruolo dei giocatori, interpretazione e background.
7. Ruolo del master come collaboratore, non avversario.
8. Skarheim come mondo vivo e reinterpretazione delle leggende.
9. Interpretazione e gestione delle risorse (1 moneta d'oro = 1 pasto).
10. Combattimento e possibilità di risolvere i conflitti in altri modi.
11. Sistema personalizzato D&D 3.5, D20, regole homebrew e power play.
12. Manuali ufficiali D&D 3.5 e Pathfinder, soggetti all'approvazione del master.
13. Occorrente per giocare e set di sette dadi.
14. Sistema di punti, costi della sala e quota di 1 euro per sessione.
15. Sintesi delle conseguenze delle azioni dei giocatori (ora introduce la sezione sul continente).
16–27. Mappa del continente, città di Meridion, Kagen, Hartak-Kar, Tar-Kees e Juvas; fazioni; Nuovi Dei, Dei Antichi ed entità divine; introduzione all'avventura in tre slide.

La formulazione delle slide è una sintesi: per verificare dettagli o recuperare il testo completo, fare riferimento a `presentazione.md`.

## Impostazione visiva

- Tema scuro ispirato al fantasy nordico, con fondo blu-verde molto scuro, riquadri grigio-verdi, testo chiaro e accenti oro, salvia e ruggine.
- Titoli con carattere serif; testi e intestazioni con carattere sans serif.
- Riquadri e decorazioni sono elementi editabili del `.pptx`; non sono rasterizzati in immagini.
- La copertina include una bussola stilizzata composta da forme vettoriali.
- I riquadri sono statici: la comparsa è immediata e non richiede clic per mostrare i singoli contenuti.

## Note operative per agenti futuri

- Aprire e modificare il `.pptx` con LibreOffice Impress, preservando il rapporto 16:9 e il tema esistente.
- Dopo le modifiche, controllare che il testo non esca dai riquadri e che le slide restino leggibili in modalità presentazione.
- Mantenere coerenti le informazioni con `presentazione.md`; non trasformare gli avvisi sui contenuti o le regole di campagna senza istruzioni dell'utente.
- La mappa della sezione sul continente va mantenuta nella slide 16.
- Al momento non è presente uno script di generazione versionato: il `.pptx` è il file editabile da cui proseguire. Il precedente script temporaneo di generazione è stato rimosso.
- I tempi dei cambi sono stati stimati sulla trascrizione locale con timestamp parola. Il video renderizzato è stato decodificato e i frame campione verificati; i progetti Kdenlive non sono una base affidabile per continuare finché non sarà disponibile un progetto creato e salvato dall'utente in Kdenlive.
- Eseguire una verifica strutturale del file dopo modifiche automatiche, oltre a un controllo visivo con Impress quando disponibile.

# Contesto del progetto: presentazione di Skarheim

## Scopo

Questo progetto contiene una presentazione introduttiva alla campagna di gioco di ruolo **Skarheim — L'Eredità di Daven**, da usare con **LibreOffice Impress**. Il file di riferimento con i contenuti è [presentazione.md](./presentazione.md); la presentazione modificabile è [presentazione.pptx](./presentazione.pptx).

## Stato attuale

- La presentazione PowerPoint è composta da **27 slide**, in formato panoramico **16:9**.
- La presentazione è stata estesa con 12 slide dedicate alla sezione **16. Il continente** del sorgente: mappa, città, fazioni, pantheon e introduzione all'avventura.
- La mappa [resources/mappa-del-mondo.png](./resources/mappa-del-mondo.png) è incorporata nella slide 16, insieme all'elenco delle città principali.
- **Non ci sono animazioni** nella versione attuale. In precedenza erano state aggiunte animazioni di comparsa graduale ai riquadri, ma l'utente ha chiesto di rimuoverle perché non erano di suo gradimento. Sono state eliminate e la presentazione è stata verificata nuovamente.
- Non aggiungere o ripristinare animazioni, salvo richiesta esplicita dell'utente.
- Il testo sorgente in `presentazione.md` è stato mantenuto separato dalla presentazione; la sezione 16 è stata prima aggiunta e formattata nel Markdown, poi integrata nel `.pptx`.
- `presentazione.pdf` è un PDF preesistente nella cartella; non è stato aggiornato nell'ambito di questo lavoro.
- Il progetto Kdenlive [avventura-slideshow.kdenlive](./avventura-slideshow.kdenlive) è in profilo 1080p/30 fps. In timeline sono sincronizzati al parlato `ls_1`, `brunilda_1`, `ls_7`, `dummy_4`, `yldra_1`, `ls_8`, `ls_9`, `ls_10`, `valakit_1` e `astrid_1`, con dissolvenze, slow zoom iniziale e fade out finale.
- Il parlato `resources/audio/avventura.mp3` è l'unico audio presente in timeline (traccia A1). La musica `resources/audio/avventura-doppiata-musica.mp3` e tutte le 19 immagini restano nel raccoglitore; non aggiungere la musica in timeline senza richiesta.
- La sequenza immagini va mantenuta sincronizzata ai passaggi richiesti: Brunilda prima di «Ma qualcosa sta cambiando», `ls_7` prima di «E voi siete nel mezzo», `dummy_4` prima di «I Custodi dell'Ultima Voce», Yldra prima di «Valchiria», `ls_8–10` da «in alcune regioni la vita sta morendo» fino al passaggio su Valakit, Valakit al suo nome e Astrid prima di «Il mondo sta cambiando».
- I cambi immagine usano dissolvenze di circa un secondo centrate sulle parole bersaglio; il primo paesaggio ha un lieve zoom progressivo e l'ultima immagine sfuma a nero alla fine del parlato. Mantenere questa impostazione quando si aggiorna il montaggio.
- La trascrizione locale del parlato è disponibile in [resources/audio/avventura-trascrizione.txt](./resources/audio/avventura-trascrizione.txt) e in [resources/audio/avventura.srt](./resources/audio/avventura.srt), con 22 segmenti temporizzati. Il modello automatico aveva riconosciuto male alcuni termini fantasy; i nomi e le parole evidenti sono stati corretti confrontandoli con il testo dell'introduzione in `presentazione.md`.
- Durate verificate: parlato circa **2:29,708**; musica circa **2:39,001**. Le durate dei producer sono esplicitate nel progetto Kdenlive.

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
- Nel progetto Kdenlive, conservare la musica nel raccoglitore finché l'utente non ne richiede l'inserimento in timeline; mantenere i riferimenti delle immagini già sincronizzati salvo nuove indicazioni.
- I tempi dei cambi sono stati stimati sulla trascrizione locale con timestamp parola. Il progetto XML è stato controllato, ma Kdenlive e MLT non sono installati nell'ambiente di lavoro: non dichiarare il rendering o l'apertura nell'applicazione come verificati.
- Eseguire una verifica strutturale del file dopo modifiche automatiche, oltre a un controllo visivo con Impress quando disponibile.

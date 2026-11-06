# GRAVEL CARANO 2027 — Edizione webmaster definitiva

## Struttura

- `index.html`: homepage compatta, un solo pulsante giallo ISCRIZIONI nella testata.
- `evento.html`, `percorsi.html`, `memorial.html`: pagine dedicate.
- `iscrizioni.html`: richiesta informazioni con verifica email (backend richiesto).
- `privacy.html`: **BOZZA** da completare prima della pubblicazione.
- `conferma.html`: pagina di conferma dopo verifica email.
- `assets/css/style.css`: foglio di stile leggibile, una dichiarazione per riga.
- `assets/js/main.js`: menu e invio modulo, codice commentato e indentato.
- `assets/images/`: immagini provvisorie, fotografie AI e materiali da verificare.
- `server/app.py`: Flask + SQLite + SMTP + admin + esportazione CSV.

## Anteprima locale

Apri `index.html` per vedere il sito statico. Il modulo **non funziona** con file://.

## Backend locale

1. Installa Python 3.11+.
2. `python -m venv .venv`
3. Attiva l'ambiente virtuale e installa: `pip install -r server/requirements.txt`
4. Copia le variabili da `server/config.example.env` nel tuo ambiente.
5. Imposta `GC_ADMIN_USER`, `GC_ADMIN_PASSWORD`, `GC_SMTP_HOST`, `GC_SMTP_USER`, `GC_SMTP_PASSWORD`, `GC_SMTP_FROM`, `GC_PUBLIC_URL`.
6. Esegui `python server/app.py` e visita `http://127.0.0.1:5000`.
7. Area riservata: `/admin`; esportazione: `/admin/export.csv`.

## Prima di pubblicare

- Conferma data, orari, luogo di partenza e indirizzo Tenuta Garibaldi.
- Completa l'informativa Privacy e verifica basi giuridiche e tempi di conservazione.
- Attiva HTTPS, backup del database, protezione anti-spam, rate limiting e hosting sicuro.
- Configura e testa SMTP, admin e messaggi di verifica.
- Le immagini AI sono illustrative: **non** sono foto reali della manifestazione né del territorio.
- Le fotografie della seconda versione sono conservate solo come materiali opzionali; verifica diritti e consenso prima di pubblicarle.
- Nessun pagamento o iscrizione definitiva è implementato.

## Google Maps

Link: https://www.google.com/maps/search/?api=1&query=Tenuta+Ravizza+Garibaldi%2C+Via+Carano+129%2C+Aprilia+LT

Il link è un riferimento alla Tenuta Garibaldi; **non** è conferma del punto di ritrovo.

## Personalizzazione

Modifica contenuti nei singoli file `.html`; colori e dimensioni in `assets/css/style.css`; foto in `assets/images/`.
Tutti i file HTML, CSS e JS sono formattati con rientri e interruzioni di riga per manutenzione.


## Fotografie autentiche (aggiornamento)

Le quattro fotografie fornite dagli organizzatori sono conservate senza
ritagli forzati in `assets/images/`:

- `giancarlo-cavallin.webp`: ritratto di Giancarlo, pagina `memorial.html`.
- `gatto-bike-team-reale.webp`: gruppo del team, pagina `evento.html`.
- `edizione-2026.webp`: Ilaria con il vincitore del 2026, pagina `evento.html`.
- `sede-gatto-bike-reale.webp`: sede, negozio e officina, pagina `evento.html`.

Non sono attribuiti ruoli ufficiali a singoli membri del team.
Per sostituire una foto, mantenere il nome del file e il rapporto
d'aspetto oppure modificare il riferimento `<img src="...">`.
I testi rimangono separati dalle immagini e sono editabili in HTML.

**Prima della pubblicazione:** verificare il consenso alla pubblicazione
delle immagini delle persone ritratte, in particolare nel contesto
promozionale dell'evento.


## Fotografie autentiche e attribuzioni
- `assets/images/giancarlo-cavallin.webp`: ritratto di Giancarlo Cavallin, pagina Memorial.
- `assets/images/gatto-bike-team-reale.webp`: foto del team, pagina Evento.
- `assets/images/edizione-2026.webp`: Ilaria con il vincitore del 2026, pagina Evento.
- `assets/images/sede-gatto-bike-reale.webp`: negozio/officina Gatto Bike, pagina Evento.
Non sono attribuite cariche associative non confermate. Le fotografie reali sono presentate con `object-fit: contain` o proporzioni naturali per non tagliare volti e persone.
Prima della pubblicazione verificare il consenso all'uso delle immagini delle persone ritratte.

## Revisione: fotografie centrate e iscrizione visibile

- In `assets/css/style.css`, la fotografia della homepage usa `background-size: contain` anziché `cover`, così non viene tagliata.
- Tutte le fotografie delle pagine interne mantengono il loro rapporto d'aspetto e sono centrate.
- Nella homepage è visibile un pulsante giallo **ISCRIVITI ALL'EVENTO**, collegato a `iscrizioni.html`, accanto a **Scopri l'evento**.
- Il modulo è una **richiesta di partecipazione**: l'iscrizione effettiva richiede conferma e configurazione del server.
- Il pulsante nel menu resta come accesso rapido alla stessa pagina.

## Correzione impaginazione pagine interne
- Evento, Percorsi e Memorial: prima schermata più compatta; fotografie visualizzate per intero con `object-fit: contain`, centrate, e titoli ridimensionati per non troncare il testo.
- Memorial: il ritratto di Giancarlo mantiene proporzioni originali e altezza massima di 355 px su desktop.
- Richiedi informazioni: la prima schermata mostra soltanto l'intestazione; il modulo «Resta aggiornato» compare dopo lo scroll.
- Le regole aggiunte sono alla fine di `assets/css/style.css` e sono commentate per agevolare il webmaster.

## Aggiornamento fotografico
- **Evento:** fotografia alzata tramite riduzione degli spazi sopra il contenuto.
- **Memorial:** ritratto di Giancarlo alzato, con visualizzazione completa.
- **Percorsi:** eliminato definitivamente il rettangolo nero presente nei pixel del JPG originale, ritagliando la sola parte fotografica.
- Regole CSS documentate alla fine di `assets/css/style.css`.

## Ultima modifica: pagina Memorial
- Foto di Giancarlo: proporzioni conservate, nessun ritaglio, centratura.
- Pulsante giallo «Contatta gli organizzatori»: testo ad alto contrasto, dimensione leggibile, va a capo su smartphone e apre il client email.
- Il codice resta separato e modificabile.

## Aggiornamento finale: fotografie e pulsanti
- Memorial: fotografia e blocco di contatto spostati più in alto tramite spaziatura superiore ridotta; pulsante giallo leggibile senza ritagli.
- Percorsi: immagine intera, centrata, senza cornici scure; pulsante «Richiedi aggiornamenti» con bordo interamente visibile.
- Evento: foto e pulsante Maps rialzati; il pulsante va a capo quando necessario senza tagliare le parole.
- Desktop e mobile: layout adattivo; sui telefoni piccoli può essere necessario scorrere per raggiungere il pulsante.
- Modifiche finali in `assets/css/style.css`, con commenti per il webmaster.

## Ritocco finale Evento e Memorial
- Evento: contenuto e pulsante Maps alzati di circa 38 px su desktop (14 px su schermi piccoli).
- Memorial: foto di Giancarlo ridotta a un massimo di 315 px e rialzata di circa 38 px su desktop.
- Su mobile le distanze sono ridotte per non causare sovrapposizioni.

# Arzano B2 2026/27

Calendario, risultati, classifica e mappa dei campi della Serie B2 femminile, girone H, stagione 2026/27, con la Lu.Vo Barattoli Arzano in evidenza.

- `index.html`: la pagina del sito (GitHub Pages).
- `data.json`: risultati e classifica, rigenerati in automatico dai dati ufficiali FIPAV.
- `scripts/gen.py`: converte i JSON FIPAV in `data.json`.

L'aggiornamento è fatto da due attività pianificate di Claude (sabato e domenica, nelle fasce orarie delle partite): scaricano i dati FIPAV, rigenerano `data.json` con `scripts/gen.py` e, se è cambiato, lo salvano in questo repository. GitHub Pages ripubblica il sito a ogni modifica di `main`. I server di GitHub Actions non possono scaricare i dati FIPAV (il portale risponde 403), per questo l'aggiornamento non avviene qui.

Fonte dati: portale FIPAV (federvolley.it). Loghi dai profili Instagram ufficiali delle società.

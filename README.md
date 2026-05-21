# Il Post Filtered RSS

Feed RSS filtrato de **Il Post**, generato automaticamente tramite Raspberry Pi e pubblicato su GitHub.

## Obiettivo del progetto

Il feed RSS ufficiale de Il Post contiene articoli provenienti da tutte le categorie del sito.

Questo progetto crea automaticamente una versione filtrata del feed, mantenendo solo gli articoli appartenenti alle categorie desiderate.

Il sistema:

1. scarica il feed RSS ufficiale de Il Post
2. analizza tutti gli articoli presenti
3. mantiene solo quelli appartenenti alle categorie selezionate
4. genera un nuovo file `feed.xml`
5. pubblica automaticamente il feed aggiornato su GitHub

---

# Feed RSS

Feed aggiornato automaticamente:

```text
https://raw.githubusercontent.com/Michilillo/ilpost-filtered/main/feed.xml
```

> È consigliato utilizzare il link RAW GitHub invece di GitHub Pages, perché aggiorna il feed molto più rapidamente ed evita problemi di cache nei reader RSS.

---

# Categorie incluse

Le categorie possono essere modificate facilmente nel file:

```text
filter_feed.py
```

all'interno della variabile:

```python
WHITELIST = [
    ...
]
```

---

# Come funziona

## Raspberry Pi

Uno script Python viene eseguito automaticamente ogni 5 minuti tramite `cron` su Raspberry Pi.

Lo script:

* scarica il feed RSS originale
* filtra gli articoli
* genera `feed.xml`
* effettua automaticamente commit e push su GitHub solo quando il feed cambia realmente

---

# Stack utilizzato

* Python 3
* requests
* xml.etree.ElementTree
* GitHub
* Raspberry Pi
* cron

---

# Automazione

Il Raspberry Pi esegue automaticamente:

```bash
/home/pi/ilpost-filtered/update.sh
```

tramite:

```cron
*/5 * * * *
```

Lo script aggiorna il feed solo quando vengono trovati nuovi articoli.

---

# Struttura del progetto

```text
.
├── filter_feed.py
├── feed.xml
├── update.sh
└── README.md
```

---

# Note tecniche

Il progetto:

* evita commit inutili
* evita aggiornamenti continui del feed RSS
* utilizza un self-reference Atom link per migliorare la compatibilità con i reader RSS
* mantiene il feed il più compatibile possibile con i principali client RSS

---

# Possibili miglioramenti futuri

* Supporto blacklist categorie
* Supporto keyword filtering
* Supporto feed multipli
* Pubblicazione automatica tramite GitHub Actions
* Web interface per gestione categorie
* Docker container

---

# Licenza

Progetto personale open-source distribuito senza garanzia.

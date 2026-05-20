# ilpost-filtered

Feed RSS personalizzato de **Il Post**, filtrato per categorie, generato automaticamente ogni 15 minuti via GitHub Actions e pubblicato su GitHub Pages.

## Come funziona

1. GitHub Actions scarica `https://www.ilpost.it/feed` ogni 15 minuti
2. Lo script `filter_feed.py` mantiene solo gli articoli nelle categorie della tua whitelist
3. Genera `feed.xml` e fa il commit nel repo
4. GitHub Pages serve il file come URL pubblico

## Configurazione categorie

Modifica `WHITELIST` in `filter_feed.py`:

```python
WHITELIST = [
    "Tecnologia",
    "Internet",
    "Scienza",
    "Cultura",
    "Economia",
    "Mondo",
    "Politica",
    "Italia",
]
```

Categorie disponibili su Il Post:
`Italia` · `Mondo` · `Politica` · `Tecnologia` · `Internet` · `Scienza` · `Cultura` · `Economia` · `Sport` · `Moda` · `Libri` · `Consumismi` · `Storie/Idee` · `Ok Boomer!`

## Setup iniziale

### 1. Crea il repository su GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<TUO-USERNAME>/ilpost-filtered.git
git push -u origin main
```

### 2. Abilita GitHub Pages

- Vai su **Settings → Pages**
- Source: **Deploy from a branch**
- Branch: `main` · Folder: `/ (root)`
- Clicca **Save**

### 3. Prima esecuzione manuale

- Vai su **Actions → Aggiorna feed filtrato Il Post → Run workflow**
- Questo genera subito `feed.xml` senza aspettare

### 4. URL del tuo feed

```
https://<TUO-USERNAME>.github.io/ilpost-filtered/feed.xml
```

## Struttura file

```
ilpost-filtered/
├── filter_feed.py                  # Script di filtraggio
├── feed.xml                        # Feed generato (auto-aggiornato)
├── index.html                      # Pagina GitHub Pages
├── README.md
└── .github/
    └── workflows/
        └── update-feed.yml         # Workflow GitHub Actions
```

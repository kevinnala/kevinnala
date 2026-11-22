# kevinnala

## Skill `caccia-affari`

Skill per Claude Code che trova oggetti vintage, antichi e da collezione venduti sotto
il loro valore, li identifica e attribuisce con un metodo da perito, ne stima il valore
su vendite reali e indica dove rivenderli per il massimo ricavo netto.

Si trova in `.claude/skills/caccia-affari/`:

- `SKILL.md`: il flusso di lavoro (cerca → identifica → stima → scegli il canale → scheda affare)
- `references/`: metodo di perizia, dove cercare, dove rivendere, leggi e fisco, e guide per
  categoria (carte collezionabili, dipinti, metalli, ceramiche e vetri, design, altre)
- `scripts/categoria.py`: instradatore che riconosce la categoria di un annuncio e indica solo le righe da leggere
- `scripts/margine.py`: calcolatore di ricavo netto e prezzo massimo da offrire
- `manuali/testi/`: 20 manuali di dominio pubblico; `dati/`: indici open data di produttori e artisti
- `manuali/`: cartella per i tuoi manuali e appunti personali

### Come usarla

- Dentro questo repository Claude Code la carica da sola. Chiedi per esempio:
  "trovami su Subito quadri dell'Ottocento sotto i 200 € in Toscana", "quanto vale questa
  carta Pokémon e dove la vendo?", "questo candeliere è antico?".
- Per usarla in ogni progetto, copia la cartella in `~/.claude/skills/caccia-affari/`.

Calcolatore:

```bash
python3 .claude/skills/caccia-affari/scripts/margine.py --acquisto 40 --vendita 300 --tutti
```

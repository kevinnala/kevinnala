#!/usr/bin/env python3
"""Scanner GENERALE: non cerca parole decise prima, legge TUTTI gli annunci nuovi di alcune
categorie (Subito, Wallapop) e le aste giudiziarie (Fallcoaste), tiene quelli dei venditori
che probabilmente non sanno cosa hanno e li impagina in griglie di miniature numerate.
Claude guarda le griglie (come un rigattiere che scorre un banco) e sceglie cosa periziare:
la foto dice quello che la descrizione non dice.

  esplora.py                 # giro completo (fonti in scanner_config.json → "esplora")
  esplora.py --pagine 3      # prova veloce (al massimo 3 pagine per categoria)
  esplora.py --griglie       # rifà solo le griglie dall'ultimo giro
  esplora.py --profondo 40   # su richiesta: scava 40 pagine più indietro per categoria (annunci di
                             # qualche giorno fa mai visti); utile quando l'utente chiede "altri"

Uscita (risultati/esplora/): griglia-01.jpg, griglia-02.jpg ... e candidati.json
(numero → annuncio). Poi: Claude scrive i numeri scelti in risultati/esplora/scelti.txt
(uno per riga o separati da spazi) e lancia `perizie.py prepara --scelti`.

Regole: budget massimo per pezzo, solo privati, annunci non già visti né periziati;
"solo ritiro a mano" tenuto solo nelle province di ritiro (le aste giudiziarie restano
tutte: ritiro o spedizione si chiedono all'IVG, e il valore può giustificare il viaggio).
"""
import concurrent.futures as cf
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import categoria as router  # noqa: E402
import memoria  # noqa: E402

RIS = os.path.normpath(os.path.join(QUI, "..", "risultati"))
OUT = os.path.join(RIS, "esplora")
F_CAND = os.path.join(OUT, "candidati.json")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

GENERICHE = ["oggetto", "oggetti", "soprammobile", "soprammobili", "vecchio", "vecchia", "vecchi", "vecchie",
             "antico", "antica", "antichi", "statua", "statuina", "statuetta", "vaso", "vasi", "quadro", "quadri",
             "dipinto", "piatto", "piatti", "lotto", "vari", "varie", "misti", "scultura", "maschera", "figura",
             "bronzo", "ottone", "argento", "vetro", "ceramica", "porcellana", "legno", "lampada", "cornice",
             "scatola", "scatolina", "servizio", "tazze", "bottiglia", "orologio", "penna", "moneta", "monete",
             "francobolli", "libro", "libri", "disco", "dischi", "giocattolo", "bambola", "collezione",
             "candelabro", "candelieri", "specchio", "tappeto", "sedia", "tavolino", "mobile", "cassapanca"]


def norm(s):
    return router.norm(s or "")


# --- fonti -----------------------------------------------------------------------
def subito(cat_cfg, budget, ultimo, pagine_max, profondo=0):
    """Pagine di categoria in ordine di data; si ferma quando arriva agli annunci del giro prima.
    profondo=N: salta le pagine già lette di solito e scava N pagine più indietro (annunci più vecchi)."""
    out = []
    for c in cat_cfg:
        url_base = c["url"].format(budget=budget)
        limite = min(c.get("pagine_max", 15), pagine_max or 999)
        inizio = 0
        if profondo:
            inizio, limite, ultimo = limite, limite + profondo, None
        for blocco in range(inizio, limite, 5):
            ric = [{"url": f"{url_base}&o={p}" if p > 1 else url_base, "zona": "Italia", "query": c["nome"]}
                   for p in range(blocco + 1, min(blocco + 6, limite + 1))]
            proc = subprocess.run(["node", os.path.join(QUI, "subito_fetch.js")], input=json.dumps(ric),
                                  capture_output=True, text=True, timeout=30 * 60)
            sys.stderr.write(proc.stderr)
            righe = [json.loads(r) for r in proc.stdout.splitlines() if r.startswith("{")]
            out += righe
            if not righe or (ultimo and min(r["data"] for r in righe if r.get("data")) < ultimo):
                break  # arrivato agli annunci già passati nel giro precedente
    return out


def wallapop(cfg, budget, pagine_max):
    out = []
    for cat in cfg.get("categorie", []):
        params = {"category_id": cat, "latitude": cfg.get("latitudine", 40.8518), "longitude": cfg.get("longitudine", 14.2681),
                  "order_by": "newest", "source": "side_bar_filters", "max_sale_price": budget}
        prossima = None
        for pag in range(min(cfg.get("pagine_max", 5), pagine_max or 999)):
            p = dict(params)
            if prossima:
                p = {"next_page": prossima, "source": "side_bar_filters"}
            req = urllib.request.Request("https://api.wallapop.com/api/v3/search?" + urllib.parse.urlencode(p),
                                         headers={"Accept": "application/json", "X-DeviceOS": "0", "User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=40) as r:
                    d = json.load(r)
            except Exception as e:  # noqa: BLE001
                sys.stderr.write(f"[Wallapop {cat}] ERRORE {e}\n")
                break
            items = d.get("data", {}).get("section", {}).get("payload", {}).get("items", [])
            for x in items:
                loc = x.get("location") or {}
                if cfg.get("solo_italia", True) and loc.get("country_code") != "IT":
                    continue  # Wallapop non spedisce dalla Spagna all'Italia
                out.append({
                    "id": "wp-" + x["id"], "fonte": "Wallapop", "titolo": x.get("title", ""),
                    "testo": x.get("description", ""), "prezzo": (x.get("price") or {}).get("amount"),
                    "data": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((x.get("created_at") or 0) / 1000)),
                    "categoria_subito": str(cat), "url": "https://it.wallapop.com/item/" + x.get("web_slug", ""),
                    "comune": loc.get("city", ""), "provincia": loc.get("region2") or "",
                    "locale": loc.get("region") in cfg.get("regioni_ritiro", []), "azienda": False,
                    "n_foto": len(x.get("images") or []),
                    "foto": [im.get("urls", {}).get("medium") or im.get("urls", {}).get("big", "")
                             for im in (x.get("images") or [])][:4],
                    "condizione": "", "spedizione": bool((x.get("shipping") or {}).get("item_is_shippable")),
                    "zona": "Wallapop", "query": f"categoria {cat}", "riservato": (x.get("reserved") or {}).get("flag", False),
                })
            sys.stderr.write(f"[Wallapop cat {cat} p.{pag + 1}] {len(items)} annunci\n")
            prossima = (d.get("meta") or {}).get("next_page")
            if not prossima or not items:
                break
            time.sleep(cfg.get("pausa_s", 2))
    return out


def fallcoaste(cfg, visti):
    ric = {"elenchi": cfg["elenchi"], "pagine": cfg.get("pagine", 3), "max_lotti": cfg.get("max_lotti", 60),
           "visti": sorted(v for v in visti if v.startswith("fc-"))}
    proc = subprocess.run(["node", os.path.join(QUI, "fallcoaste_fetch.js")], input=json.dumps(ric),
                          capture_output=True, text=True, timeout=60 * 60)
    sys.stderr.write(proc.stderr)
    lotti = [json.loads(r) for r in proc.stdout.splitlines() if r.startswith("{")]
    # via le immagini comuni a più lotti (loghi, segnaposto)
    conta = {}
    for l in lotti:
        for f in l["foto"]:
            conta[f] = conta.get(f, 0) + 1
    for l in lotti:
        l["foto"] = [f for f in l["foto"] if conta[f] == 1] or l["foto"][:1]
    return lotti


# --- filtro e punteggio ----------------------------------------------------------
def segnali_venditore(a, cfg, bonus):
    s = cfg["segnali"]
    titolo, testo = norm(a["titolo"]), norm(a.get("testo"))
    tutto = f" {titolo} {testo} "
    punti, motivi = 0, []
    for w in s["inconsapevole"]:
        if f" {norm(w)} " in tutto:
            punti += 2
            motivi.append(w)
    for w in s["negativi"] + cfg["esplora"].get("escludi", []):
        if f" {norm(w)} " in tutto:
            return None, [f"escluso: {w}"]
    cat_sub = a.get("categoria_subito") or ""
    for nome, parole_epoca in cfg["esplora"].get("richiedi_epoca", {}).items():
        if cat_sub == nome and not any(f" {norm(w)} " in tutto for w in parole_epoca):
            return None, [f"{nome} senza segnali d'epoca"]  # es. libri e dischi moderni
    parole = titolo.split()
    generiche = [w for w in parole if w in GENERICHE]
    if generiche and len(generiche) >= len(parole) / 3:
        punti += 2
        motivi.append("titolo generico")
    marchi = [w for w in s.get("valore", []) if len(w) > 4 and f" {norm(w)} " in f" {titolo} "]
    if marchi:
        punti -= 1  # il venditore sa cosa ha (nomina il marchio): meno probabile l'affare
        motivi.append("nomina: " + ", ".join(marchi[:2]))
    if len(a.get("testo") or "") < 100:
        punti += 1
        motivi.append("descrizione scarna")
    if (a.get("n_foto") or 0) <= 2:
        punti += 1
        motivi.append("poche foto")
    if a.get("prezzo") is not None and a["prezzo"] <= cfg["esplora"].get("prezzo_basso", 40):
        punti += 1
        motivi.append("prezzo basso")
    cat = router.classifica(f"{a['titolo']} {a.get('testo') or ''}", json.load(open(router.CATALOGO, encoding="utf-8")))
    a["categoria"] = cat[0][1]["id"] if cat else ""
    if a["categoria"]:
        punti += 1
        b = bonus.get(a["categoria"])
        if b:
            punti += b
            motivi.append(f"esiti passati {b:+d}")
    if a.get("fonte", "").startswith("Asta"):
        punti += 3
        motivi.append("asta giudiziaria")
    return punti, motivi


def filtra(annunci, cfg, visti):
    budget = cfg["esplora"]["budget"]
    ritiro = set(cfg.get("province_ritiro", []))
    bonus = memoria.lezioni(testo=False)["bonus"]
    tenuti, scarti = [], {}
    unici = {}
    for a in annunci:
        unici.setdefault(a["id"], a)
    for a in unici.values():
        motivo = None
        if a["id"] in visti:
            motivo = "già visto"
        elif a.get("azienda"):
            motivo = "venditore professionale"
        elif a.get("riservato"):
            motivo = "riservato"
        elif a.get("prezzo") is not None and a["prezzo"] > budget:
            motivo = "oltre il budget"
        elif not a.get("fonte", "").startswith("Asta") and not a.get("spedizione") \
                and not a.get("locale", a.get("provincia") in ritiro):
            motivo = "solo ritiro e lontano"
        elif not a.get("foto"):
            motivo = "senza foto"
        if motivo:
            scarti[motivo] = scarti.get(motivo, 0) + 1
            continue
        punti, motivi = segnali_venditore(a, cfg, bonus)
        if punti is None:
            scarti["parole escluse"] = scarti.get("parole escluse", 0) + 1
            continue
        a["punti"], a["motivi"] = punti, motivi
        tenuti.append(a)
    tenuti.sort(key=lambda x: (-x["punti"], x.get("prezzo") or 0))
    return tenuti, scarti, len(unici)


# --- griglie ---------------------------------------------------------------------
def miniatura(url, lato):
    from PIL import Image
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "image/jpeg,image/*"})
        with urllib.request.urlopen(req, timeout=25) as r:
            im = Image.open(io.BytesIO(r.read())).convert("RGB")
        im.thumbnail((lato, lato))
        return im
    except Exception:  # noqa: BLE001
        return None


def griglie(cand, per_griglia=20, colonne=5, lato=300):
    from PIL import Image, ImageDraw
    for f in os.listdir(OUT):
        if f.startswith("griglia-"):
            os.remove(os.path.join(OUT, f))
    with cf.ThreadPoolExecutor(8) as ex:
        minis = list(ex.map(lambda a: miniatura(a["foto"][0], lato), cand))
    righe = (per_griglia + colonne - 1) // colonne
    alto = lato + 34
    n_griglie = 0
    for g in range(0, len(cand), per_griglia):
        tela = Image.new("RGB", (colonne * lato, righe * alto), "white")
        d = ImageDraw.Draw(tela)
        for k, (a, im) in enumerate(zip(cand[g:g + per_griglia], minis[g:g + per_griglia])):
            x, y = (k % colonne) * lato, (k // colonne) * alto
            if im:
                tela.paste(im, (x + (lato - im.width) // 2, y + 34 + (lato - im.height) // 2))
            prezzo = f"{a['prezzo']:.0f} EUR" if a.get("prezzo") is not None else "? EUR"
            d.rectangle([x, y, x + lato - 1, y + 33], fill=(255, 245, 200))
            d.text((x + 4, y + 2), f"#{a['k']}  {prezzo}  {a.get('fonte', 'Subito')[:12]}", fill=(180, 0, 0))
            d.text((x + 4, y + 17), a["titolo"][:44], fill=(0, 0, 0))
            d.rectangle([x, y, x + lato - 1, y + alto - 1], outline=(200, 200, 200))
        n_griglie += 1
        tela.save(os.path.join(OUT, f"griglia-{n_griglie:02d}.jpg"), quality=78)
    return n_griglie


def main(argv):
    cfg = json.load(open(os.path.join(QUI, "scanner_config.json"), encoding="utf-8"))
    e = cfg["esplora"]
    os.makedirs(OUT, exist_ok=True)
    if "--griglie" in argv:
        cand = json.load(open(F_CAND, encoding="utf-8"))
        print(f"Griglie: {griglie(cand, e.get('per_griglia', 20))}")
        return 0
    pagine_max = int(argv[argv.index("--pagine") + 1]) if "--pagine" in argv else None
    profondo = int(argv[argv.index("--profondo") + 1]) if "--profondo" in argv else 0
    st = memoria.stato()
    ultimo = st.get("esplora_ultimo_giro")
    inizio = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    visti = memoria.visti() | memoria.ids_periziati()
    annunci = []
    if e.get("subito"):
        annunci += subito(e["subito"], e["budget"], ultimo, pagine_max, profondo)
    if e.get("wallapop", {}).get("categorie"):
        w = dict(e["wallapop"], regioni_ritiro=cfg.get("regioni_ritiro", []))
        annunci += wallapop(w, e["budget"], pagine_max)
    if e.get("fallcoaste", {}).get("elenchi"):
        annunci += fallcoaste(e["fallcoaste"], visti)
    tenuti, scarti, letti = filtra(annunci, cfg, visti)
    cand = tenuti[: e.get("max_candidati", 400)]
    for k, a in enumerate(cand, 1):
        a["k"] = k
    with open(F_CAND, "w", encoding="utf-8") as fh:
        json.dump(cand, fh, ensure_ascii=False, indent=1)
    n = griglie(cand, e.get("per_griglia", 20)) if cand else 0
    memoria.aggiungi_coda(cand, "griglie")  # quelli non periziati restano in coda, da vedere a blocchi
    # tutto ciò che è passato dal filtro o dalle griglie non torna al giro dopo
    memoria.aggiungi_visti([a["id"] for a in annunci])
    st = memoria.stato()
    if not profondo:  # lo scavo all'indietro non sposta il punto di partenza dei giri normali
        st["esplora_ultimo_giro"] = inizio
    memoria.salva_stato(st)
    print(f"Annunci letti: {letti} · scartati: {scarti} · candidati nelle griglie: {len(cand)} in {n} griglie")
    print(f"Griglie: {OUT}/griglia-01.jpg ... griglia-{n:02d}.jpg · elenco: {F_CAND}")
    print("Ora: guarda ogni griglia, scrivi i numeri promettenti in risultati/esplora/scelti.txt "
          "e lancia perizie.py prepara --scelti")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

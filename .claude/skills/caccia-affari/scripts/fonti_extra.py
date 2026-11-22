#!/usr/bin/env python3
"""Fonti di annunci oltre a Subito: Vinted (pagina pubblica, via browser) e Wallapop
(interfaccia di ricerca pubblica, Italia e Spagna). Ogni funzione ritorna una lista di
annunci nello stesso formato dello scanner di Subito.
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))


def vinted(queries, cfg):
    url = cfg.get("url", "https://www.vinted.it/catalog?search_text={q}&order=newest_first")
    ric = [{"url": url.format(q=urllib.parse.quote(q)), "query": q} for q in queries]
    proc = subprocess.run(["node", os.path.join(QUI, "vinted_fetch.js")], input=json.dumps(ric),
                          capture_output=True, text=True, timeout=60 * 60)
    sys.stderr.write(proc.stderr)
    out = []
    for riga in proc.stdout.splitlines():
        try:
            out.append(json.loads(riga))
        except json.JSONDecodeError:
            pass
    return out


def wallapop(queries, cfg, province_ritiro_nomi, regioni_ritiro):
    """Wallapop: api.wallapop.com/api/v3/search (pubblica, la usa il sito). Pausa tra le richieste."""
    out = []
    for i, q in enumerate(queries, 1):
        params = {"keywords": q, "latitude": cfg.get("latitudine", 40.8518), "longitude": cfg.get("longitudine", 14.2681),
                  "order_by": "newest", "source": "search_box"}
        url = "https://api.wallapop.com/api/v3/search?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={"Accept": "application/json", "X-DeviceOS": "0",
                                                   "User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)
            items = d.get("data", {}).get("section", {}).get("payload", {}).get("items", [])
            for x in items:
                loc = x.get("location") or {}
                sped = bool((x.get("shipping") or {}).get("item_is_shippable"))
                provincia = loc.get("region2") or ""
                locale = (loc.get("country_code") == "IT" and
                          (loc.get("region") in regioni_ritiro or provincia in province_ritiro_nomi))
                foto = [im.get("urls", {}).get("big") or im.get("urls", {}).get("medium", "")
                        for im in (x.get("images") or [])][:3]
                out.append({
                    "id": "wp-" + x["id"], "fonte": "Wallapop", "titolo": x.get("title", ""),
                    "testo": x.get("description", ""), "prezzo": (x.get("price") or {}).get("amount"),
                    "data": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime((x.get("created_at") or 0) / 1000)),
                    "categoria_subito": "", "url": "https://it.wallapop.com/item/" + x.get("web_slug", ""),
                    "comune": loc.get("city", ""), "provincia": f"{provincia} {loc.get('country_code', '')}".strip(),
                    "locale": locale, "azienda": False, "n_foto": len(x.get("images") or []), "foto": foto,
                    "condizione": "", "spedizione": sped, "zona": "Wallapop", "query": q,
                    "riservato": (x.get("reserved") or {}).get("flag", False),
                })
            sys.stderr.write(f"[Wallapop {i}/{len(queries)}] \"{q}\": {len(items)} annunci\n")
        except Exception as e:  # noqa: BLE001
            sys.stderr.write(f"[Wallapop {i}/{len(queries)}] ERRORE \"{q}\": {e}\n")
        time.sleep(cfg.get("pausa_s", 2))
    return out

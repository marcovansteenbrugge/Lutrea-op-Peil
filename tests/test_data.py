"""Controle van site/data.json tegen de structuur en regels uit routine/ochtendroutine.md.

Draaien: python3 -m unittest discover -s tests -v
Een ander bestand toetsen: OP_PEIL_DATA=pad/naar/data.json python3 -m unittest discover -s tests -v
"""
import datetime
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(os.environ.get("OP_PEIL_DATA", ROOT / "site" / "data.json"))

# Volgorde van de rubrieken uit routine/ochtendroutine.md ("RUBRIEKEN").
RUBRIEKEN = ["civil3d", "dijk", "stedelijk", "grondwerk", "inmeten", "ai",
             "software", "markt", "kennis", "leren", "internationaal"]
# index.html voegt "agenda" zelf toe als rubriek voor bronnen.
EXTRA_BRON_RUBRIEKEN = {"agenda"}

TOPNIVEAU = {
    "edition": str, "editionNo": int, "intro": str, "highlights": list,
    "categories": list, "items": list, "events": list, "recurring": list,
    "sources": list, "archive": list, "footnote": str,
}
VELDEN = {
    "categories": {"id": str, "name": str, "blurb": str},
    "items": {"cat": str, "date": str, "sort": str, "added": str,
              "title": str, "summary": str, "urls": list},
    "events": {"name": str, "start": str, "end": str, "dateLabel": str,
               "place": str, "why": str, "url": str},
    "recurring": {"name": str, "when": str, "why": str, "url": str},
    "sources": {"cat": str, "name": str, "url": str},
    "archive": {"date": str, "headline": str},
}
OPTIONEEL = {"items": {"unsure": bool, "tip": bool}, "events": {"unconfirmed": bool}}

AANTAL_HIGHLIGHTS = 5
MAX_ARCHIEF = 30
MAX_DAGEN_ITEM = 30
MAX_DAGEN_NA_EVENT = 7

ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL = re.compile(r"^https?://\S+$")


def datum(waarde):
    if not isinstance(waarde, str) or not ISO.match(waarde):
        return None
    try:
        return datetime.date.fromisoformat(waarde)
    except ValueError:
        return None


class TestDataJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tekst = DATA.read_text(encoding="utf-8")
        try:
            cls.d = json.loads(tekst)
        except json.JSONDecodeError as e:
            cls.d = None
            cls.json_fout = f"{DATA} is geen geldige JSON: {e}"

    def setUp(self):
        if self.d is None:
            self.fail(self.json_fout)

    def test_geldige_json(self):
        self.assertIsInstance(self.d, dict, f"{DATA}: verwacht een object op het hoogste niveau")

    def test_topniveau(self):
        for sleutel, soort in TOPNIVEAU.items():
            self.assertIn(sleutel, self.d, f"sleutel '{sleutel}' ontbreekt")
            self.assertIsInstance(self.d[sleutel], soort, f"'{sleutel}' moet {soort.__name__} zijn")

    def test_velden_per_onderdeel(self):
        fouten = []
        for lijst, velden in VELDEN.items():
            for n, el in enumerate(self.d.get(lijst, [])):
                if not isinstance(el, dict):
                    fouten.append(f"{lijst}[{n}] is geen object")
                    continue
                for veld, soort in velden.items():
                    if veld not in el:
                        fouten.append(f"{lijst}[{n}] mist '{veld}'")
                    elif not isinstance(el[veld], soort):
                        fouten.append(f"{lijst}[{n}].{veld} moet {soort.__name__} zijn")
                for veld, soort in OPTIONEEL.get(lijst, {}).items():
                    if veld in el and not isinstance(el[veld], soort):
                        fouten.append(f"{lijst}[{n}].{veld} moet {soort.__name__} zijn")
        if fouten:
            self.fail("\n".join(fouten))

    def test_highlights(self):
        hl = self.d["highlights"]
        self.assertEqual(len(hl), AANTAL_HIGHLIGHTS,
                         f"verwacht {AANTAL_HIGHLIGHTS} highlights, gevonden {len(hl)}")
        for n, h in enumerate(hl):
            self.assertTrue(isinstance(h, str) and h.strip(), f"highlights[{n}] is leeg of geen tekst")

    def test_archief_maximaal(self):
        self.assertLessEqual(len(self.d["archive"]), MAX_ARCHIEF,
                             f"archief heeft {len(self.d['archive'])} regels, maximaal {MAX_ARCHIEF}")

    def test_rubrieken(self):
        ids = [c["id"] for c in self.d["categories"]]
        onbekend = [i for i in ids if i not in RUBRIEKEN]
        self.assertEqual(onbekend, [], f"onbekende rubrieken in categories: {onbekend}")
        self.assertEqual(len(ids), len(set(ids)), "dubbele rubriek in categories")
        self.assertEqual(ids, [r for r in RUBRIEKEN if r in ids],
                         "categories staan niet in de volgorde van de routine")

    def test_cat_bestaat(self):
        ids = {c["id"] for c in self.d["categories"]}
        fouten = [f"items[{n}] '{i['title']}': onbekende cat '{i['cat']}'"
                  for n, i in enumerate(self.d["items"]) if i["cat"] not in ids]
        fouten += [f"sources[{n}] '{s['name']}': onbekende cat '{s['cat']}'"
                   for n, s in enumerate(self.d["sources"])
                   if s["cat"] not in ids | EXTRA_BRON_RUBRIEKEN]
        if fouten:
            self.fail("\n".join(fouten))

    def test_datums(self):
        fouten = []
        if datum(self.d["edition"]) is None:
            fouten.append(f"edition '{self.d['edition']}' is geen ISO-datum")
        for lijst, velden in (("items", ("sort", "added")), ("events", ("start", "end")),
                              ("archive", ("date",))):
            for n, el in enumerate(self.d[lijst]):
                for veld in velden:
                    if datum(el[veld]) is None:
                        fouten.append(f"{lijst}[{n}].{veld} '{el[veld]}' is geen ISO-datum")
        if fouten:
            self.fail("\n".join(fouten))

    def test_urls(self):
        fouten = []
        for n, i in enumerate(self.d["items"]):
            if not i["urls"]:
                fouten.append(f"items[{n}] '{i['title']}' heeft geen URL")
            fouten += [f"items[{n}] '{i['title']}': ongeldige URL '{u}'"
                       for u in i["urls"] if not (isinstance(u, str) and URL.match(u))]
        for lijst in ("events", "recurring", "sources"):
            fouten += [f"{lijst}[{n}]: ongeldige URL '{el['url']}'"
                       for n, el in enumerate(self.d[lijst]) if not URL.match(el["url"])]
        if fouten:
            self.fail("\n".join(fouten))

    # Tijdsregels worden getoetst tegen de editiedatum, niet tegen vandaag (besluit B2).
    def test_geen_oude_items(self):
        editie = datum(self.d["edition"])
        self.assertIsNotNone(editie, "edition is geen ISO-datum")
        fouten = [f"items[{n}] '{i['title']}': added {i['added']} is meer dan {MAX_DAGEN_ITEM} dagen vóór de editie"
                  for n, i in enumerate(self.d["items"])
                  if not i.get("tip") and datum(i["added"])
                  and (editie - datum(i["added"])).days > MAX_DAGEN_ITEM]
        if fouten:
            self.fail("\n".join(fouten))

    def test_geen_verlopen_events(self):
        editie = datum(self.d["edition"])
        self.assertIsNotNone(editie, "edition is geen ISO-datum")
        fouten = [f"events[{n}] '{e['name']}': end {e['end']} is meer dan {MAX_DAGEN_NA_EVENT} dagen vóór de editie"
                  for n, e in enumerate(self.d["events"])
                  if datum(e["end"]) and (editie - datum(e["end"])).days > MAX_DAGEN_NA_EVENT]
        if fouten:
            self.fail("\n".join(fouten))


if __name__ == "__main__":
    unittest.main()

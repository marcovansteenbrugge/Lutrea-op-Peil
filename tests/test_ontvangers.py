"""Controle dat de ontvangers in routine/ontvangers.md en in stap 5 van routine/ochtendroutine.md gelijk zijn.

Draaien: python3 -m unittest discover -s tests -v
Andere bestanden toetsen: OP_PEIL_ONTVANGERS=... OP_PEIL_ROUTINE=... python3 -m unittest discover -s tests -v
"""
import collections
import json
import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ONTVANGERS = Path(os.environ.get("OP_PEIL_ONTVANGERS", ROOT / "routine" / "ontvangers.md"))
ROUTINE = Path(os.environ.get("OP_PEIL_ROUTINE", ROOT / "routine" / "ochtendroutine.md"))

# Veld in de tabel van ontvangers.md -> sleutel in stap 5 van de routine.
VELDEN = {"aan": "to", "bcc": "bcc"}
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.IGNORECASE)


def lees_tabel(pad):
    """Rijen '| adres | Veld |' uit ontvangers.md, als lijst (veld, adres)."""
    rijen = []
    for regel in pad.read_text(encoding="utf-8").splitlines():
        cellen = [c.strip() for c in regel.strip().strip("|").split("|")]
        if len(cellen) == 2 and "@" in cellen[0]:
            rijen.append((cellen[1].lower(), cellen[0].lower()))
    return rijen


def lees_routine(pad):
    """Regels '- to: [...]' en '- bcc: [...]' uit de routine, als lijst (sleutel, adres)."""
    rijen = []
    for regel in pad.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*-\s*(to|cc|bcc):\s*(\[.*\])\s*$", regel)
        if m:
            rijen += [(m.group(1), a.lower()) for a in json.loads(m.group(2))]
    return rijen


class TestOntvangers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tabel = lees_tabel(ONTVANGERS)
        cls.routine = lees_routine(ROUTINE)

    def test_lijsten_gevonden(self):
        self.assertTrue(self.tabel, f"geen ontvangers gevonden in de tabel van {ONTVANGERS.name}")
        self.assertTrue(self.routine, f"geen regels '- to:'/'- bcc:' gevonden in {ROUTINE.name}")

    def test_bekende_velden(self):
        onbekend = sorted({v for v, _ in self.tabel} - set(VELDEN))
        self.assertEqual(onbekend, [], f"onbekend veld in {ONTVANGERS.name}: {onbekend}")
        onbekend = sorted({k for k, _ in self.routine} - set(VELDEN.values()))
        self.assertEqual(onbekend, [], f"onverwacht ontvangersveld in {ROUTINE.name}: {onbekend}")

    def test_geldige_adressen(self):
        fouten = [f"{ONTVANGERS.name}: ongeldig adres '{a}'" for _, a in self.tabel if not EMAIL.match(a)]
        fouten += [f"{ROUTINE.name}: ongeldig adres '{a}'" for _, a in self.routine if not EMAIL.match(a)]
        if fouten:
            self.fail("\n".join(fouten))

    def test_geen_dubbele_adressen(self):
        fouten = []
        for naam, rijen in ((ONTVANGERS.name, self.tabel), (ROUTINE.name, self.routine)):
            fouten += [f"{naam}: '{a}' staat {n} keer in de lijst"
                       for a, n in collections.Counter(a for _, a in rijen).items() if n > 1]
        if fouten:
            self.fail("\n".join(fouten))

    def test_gelijk_per_veld(self):
        fouten = []
        for veld, sleutel in VELDEN.items():
            lijst = {a for v, a in self.tabel if v == veld}
            routine = {a for k, a in self.routine if k == sleutel}
            fouten += [f"'{a}' staat als {veld.upper()} in {ONTVANGERS.name}, maar niet in '{sleutel}' van {ROUTINE.name}"
                       for a in sorted(lijst - routine)]
            fouten += [f"'{a}' staat in '{sleutel}' van {ROUTINE.name}, maar niet als {veld.upper()} in {ONTVANGERS.name}"
                       for a in sorted(routine - lijst)]
        if fouten:
            self.fail("\n".join(fouten))


if __name__ == "__main__":
    unittest.main()

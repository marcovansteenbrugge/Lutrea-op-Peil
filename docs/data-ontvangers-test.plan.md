---
plan: data-ontvangers-test
titel: Test voor data.json en de ontvangerslijst
versie: 1
status: in-uitvoering        # berekend door de skill, nooit met de hand gezet
voortgang: F0 ✅ · F1 ▶ · F2 ▶ · F3 ⏳           # berekend door de skill
opgesteld: 2026-10-02
opgesteld_door: agent (Claude Code, Opus 5.5)
beslisser: Marco van Steenbrugge, beheerder
beslisdocument: data-ontvangers-test.beslis.md
basis_commit: ede3e54
vervangt: -
samenvatting: Een testsuite die controleert dat site/data.json klopt met de afgesproken structuur en dat de ontvangers in ontvangers.md en de routine-instructie gelijk zijn.
trefwoorden: [test, data.json, ontvangers, routine, CI]
---

# Plan: Test voor data.json en de ontvangerslijst

## 1. In het kort
1. Er komt een kleine testsuite in de repo, zonder installatie, die twee afspraken uit CLAUDE.md afdwingt die nu alleen op papier staan.
2. Test 1 controleert `site/data.json`: geldige JSON, de verwachte velden, en de regels uit de ochtendroutine (5 highlights, maximaal 30 archiefregels, bekende rubrieken, geldige datums).
3. Test 2 controleert dat de ontvangers in `routine/ontvangers.md` en in stap 5 van `routine/ochtendroutine.md` gelijk zijn, inclusief Aan/BCC.
4. De tests draaien automatisch bij elke push naar main (GitHub Actions).
5. Of de routine de test zelf ook draait vóór publiceren, is een apart besluit voor een latere fase.

## 2. Aanleiding en doel
CLAUDE.md noemt onder "Nog niet afgedwongen, wel afgesproken" twee regels: `site/data.json` is geldige JSON, en de ontvangers in `routine/ontvangers.md` en `routine/ochtendroutine.md` zijn gelijk. Er is geen testsuite ("Er is nog geen testsuite") en CI-regel in de Tech Stack staat op `{{nog geen CI}}`. Een fout in data.json laat de pagina leeg ("De nieuwsdata kon niet worden geladen", `site/index.html` regel 251-253); een verschil in de ontvangerslijst betekent dat iemand de mail mist of ten onrechte krijgt.

Geslaagd als: beide afspraken met één commando lokaal te toetsen zijn, ze bij elke push naar main automatisch draaien, en CLAUDE.md ze onder "Afgedwongen" noemt met het pad naar de test.

## 3. Onderzoek en bevindingen
Getoetst tegen `ede3e54`.
- **Structuur data.json** (`site/data.json`, gemeten met Python): sleutels `edition`, `editionNo`, `intro`, `highlights` (5), `categories` (11), `items` (159), `events` (18), `recurring` (5), `sources` (49), `archive` (8), `footnote`. Items hebben altijd `cat, date, sort, added, title, summary, urls`; optioneel `unsure` (32x) en `tip` (8x). Events hebben altijd `name, start, end, dateLabel, place, why, url`; optioneel `unconfirmed`. Dit komt overeen met de beschrijving in `routine/ochtendroutine.md` stap 1.
- **Rubriek "agenda" bij bronnen**: `sources` gebruikt de cat `agenda`, die niet in `categories` staat. Dat is bedoeld: `site/index.html` regel 240 voegt `{id:"agenda"}` zelf toe. De test moet `agenda` dus toestaan voor bronnen, niet voor items.
- **Huidige stand is schoon**: alle item-cats bestaan, `sort` en `added` zijn ISO-datums, alle items hebben minstens één http(s)-URL, geen dubbele titels, geen items ouder dan 30 dagen (gerekend vanaf `edition` 2026-10-02, behalve tips), geen events met `end` meer dan 7 dagen voorbij.
- **Regels uit de routine** (`routine/ochtendroutine.md` stap 3): 5 highlights; archief maximaal 30; items ouder dan 30 dagen weg behalve tips; events weg als `end` meer dan 7 dagen voorbij is; rubrieken in vaste volgorde (civil3d, dijk, stedelijk, grondwerk, inmeten, ai, software, markt, kennis, leren, internationaal).
- **Ontvangers**: `routine/ontvangers.md` is een markdown-tabel `| Adres | Veld |` met 1x Aan en 6x BCC. `routine/ochtendroutine.md` stap 5 heeft regels `- to: [...]` en `- bcc: [...]` met JSON-achtige lijsten. Beide zijn met een eenvoudige regex te lezen. Op `ede3e54` zijn ze gelijk.
- **Gereedschap**: Python 3.11 en Node 22 zijn aanwezig in deze omgeving; de routine gebruikt al `python3` voor validatie en datum. Er is geen `package.json` of `requirements.txt`.
- **Bestaande CI**: alleen `.github/workflows/brbnt-scan.yml` (gegenereerd door brbnt-scan, niet met de hand wijzigen). Een nieuwe workflow komt dus in een eigen bestand.
- **Momentopname**: CLAUDE.md zegt dat de live data bij het artifact staat en `site/data.json` een momentopname is. De test in de repo dekt dus alleen de momentopname, niet de live editie.

## 4. Niet in scope
- Controle van de live data.json op claude.ai: die staat niet in de repo; zie B3 voor de routine-kant.
- Controle of de routine op claude.ai gelijk is aan `routine/ochtendroutine.md`: daar is geen leesbare bron in de repo voor.
- Inhoudelijke controle van nieuws (kloppen de links, is een item relevant): niet automatisch te toetsen zonder netwerk en oordeel.
- Wijzigen van `site/index.html` of de structuur van data.json.

## 5. Uitgangspunten
| Uitgangspunt | Herkomst |
|---|---|
| Geen build-stap en geen extra installatie | CLAUDE.md, Tech Stack ("zonder build-stap") |
| De routine valideert al met Python | CLAUDE.md, Testing Strategy; `routine/ochtendroutine.md` stap 3 |
| Commit-berichten in het Nederlands, direct op main | CLAUDE.md, Git-regels |
| `brbnt-scan.yml` niet met de hand wijzigen | kop van `.github/workflows/brbnt-scan.yml` |
| Ontvangers moeten in twee bestanden gelijk blijven | CLAUDE.md, Architectuur |

## 6. Ontwerp en besluiten (technisch)
Map `tests/` in de root met:
- `tests/test_data.py`: laadt `site/data.json` en controleert (a) geldige JSON, (b) verplichte sleutels en types op het hoogste niveau, (c) verplichte velden per item, event, bron, archiefregel, (d) `highlights` precies 5, `archive` maximaal 30, (e) item-`cat` bestaat in `categories`, bron-`cat` in `categories` of `agenda`, (f) `sort`, `added`, `edition`, `start`, `end`, archief-`date` zijn ISO-datums, (g) elk item heeft minstens één http(s)-URL, (h) volgens B2: items ouder dan 30 dagen (niet-tip) en events met `end` meer dan 7 dagen vóór `edition`.
- `tests/test_ontvangers.py`: leest de tabel uit `routine/ontvangers.md` en de regels `to:`/`bcc:` uit `routine/ochtendroutine.md`, en vergelijkt de verzamelingen per veld (Aan ↔ to, BCC ↔ bcc). Controleert ook dat elk adres een geldig e-mailformaat heeft en dat geen adres dubbel voorkomt. Bij verschil toont de foutmelding welk adres waar ontbreekt.
- Draaien met één commando: `python3 -m unittest discover -s tests -v` (zie B1).
- `.github/workflows/tests.yml`: draait dat commando bij push naar main en handmatig; geen rechten nodig behalve `contents: read`, actions vastgezet op een volledige commit (zelfde stijl als brbnt-scan).
- CLAUDE.md: de twee regels verhuizen van "Nog niet afgedwongen" naar "Afgedwongen" met het pad; Testing Strategy en Tech Stack (CI) bijgewerkt.

**Verdieping per besluit:**

- **B1 Testgereedschap** (nodig vóór F0). Opties: Python `unittest` uit de standaardbibliotheek, `pytest`, of Node `node:test`. `unittest` vraagt geen installatie, sluit aan op de Python die de routine al gebruikt, en draait op elke GitHub-runner. `pytest` geeft nettere uitvoer maar vraagt `pip install`. Node is ook aanwezig, maar de routine werkt al met Python. Voorstel: `unittest`.
- **B2 Tijdsregels toetsen tegen `edition`** (nodig vóór F0). De regels "items ouder dan 30 dagen weg" en "events 7 dagen na `end` weg" hangen af van een datum. Toetsen tegen vandaag maakt de test rood zodra de momentopname in de repo een paar weken oud is, ook als er niets mis is. Toetsen tegen `edition` controleert of de editie op dat moment klopte en blijft stabiel. Alternatief: de tijdsregels helemaal weglaten. Voorstel: toetsen tegen `edition`.
- **B3 Routine draait de test vóór publiceren** (nodig vóór F3). De routine leest data.json van het artifact en heeft de repo niet vanzelf. Om de test daar te draaien moet de routine de repo hebben of het script als tekst meekrijgen; dat is nog niet vastgesteld (zie Open vragen). Voorstel: F3 pas uitwerken na F0-F2, en tot die tijd blijft de bestaande `json.load`-controle in de routine.

## 7. Fasering
Een fase mag starten als de vrijgave voor die fase er is én alle besluiten waar de fase op leunt zijn genomen. Een planwijziging raakt alleen de fasen en besluiten die in het wijzigingslog staan; de vrijgave van de overige fasen blijft geldig.

| Fase | Status | Scope | Acceptatie (toetsbaar) | Hangt af van | Omvang | Gepland model en effort | Commit-prefix |
|---|---|---|---|---|---|---|---|
| F0 | ✅ gebouwd | `tests/test_data.py` met de controles (a) t/m (h) uit punt 6 | 1. `python3 -m unittest discover -s tests -v` is groen op de huidige `site/data.json`. 2. Een kopie met een kapotte komma, een onbekende item-cat, 6 highlights of een item zonder URL laat de test elk afzonderlijk rood worden met een leesbare melding. 3. Geen andere afhankelijkheid dan de Python-standaardbibliotheek. | B1, B2 | S | Opus 5.5, medium | `F0:` |
| F1 | ▶ vrijgegeven | `tests/test_ontvangers.py` | 1. Groen op de huidige twee bestanden. 2. Een adres weghalen uit één van beide, of een adres van BCC naar Aan verplaatsen, maakt de test rood met een melding die het adres en het bestand noemt. 3. Een ongeldig of dubbel adres maakt de test rood. | F0, B1 | S | Opus 5.5, medium | `F1:` |
| F2 | ▶ vrijgegeven, na F1 | `.github/workflows/tests.yml` en CLAUDE.md (Afgedwongen, Testing Strategy, Tech Stack) | 1. De workflow draait groen op GitHub na de push. 2. De workflow heeft alleen `contents: read` en actions op een volledige commit. 3. CLAUDE.md noemt beide regels onder "Afgedwongen" met het pad naar de test, en niet meer onder "Nog niet afgedwongen". | F1 | S | Opus 5.5, medium | `F2:` |
| F3 | ⏳ wacht op B3 | De routine draait de data-test vóór publiceren (`routine/ochtendroutine.md` en de routine op claude.ai) | Wordt ingevuld na B3 en de open vraag over toegang tot de repo; vóór vrijgave komt hier een planwijziging. | F2, B3 | S | Opus 5.5, medium | `F3:` |

Werkafspraak: één fase per keer, groene tests vóór de volgende fase, commit-berichten beginnen met de fase-prefix.

## 8. Gevolgen en bronnen voor afgeleide documenten
**Gegevens en privacy.** De ontvangerstest leest e-mailadressen die al in de repo staan; er komen geen nieuwe persoonsgegevens bij en niets wordt verstuurd. Foutmeldingen in de CI-log kunnen een adres noemen; die log is net zo zichtbaar als de repo zelf.
**Beveiliging.** Nieuwe workflow met alleen leesrecht en vastgezette actions; geen secrets.
**Gebruikers en handleiding.** Lezers merken niets. De beheerder krijgt een rode check op GitHub bij een fout.
**Beheer en configuratie.** Nieuwe map `tests/` en workflow `tests.yml`. Wie de ontvangers wijzigt, moet beide bestanden aanpassen, anders wordt de check rood.
**Releasenotes (kernpunten).** De nieuwsdata en de ontvangerslijst worden nu automatisch gecontroleerd bij elke wijziging.

## 9. Risico's en terugweg
- De momentopname van data.json wijkt af van wat de routine later schrijft (bijvoorbeeld een nieuw veld): de test wordt rood. Terugweg: de test aanpassen of het nieuwe veld als optioneel toelaten.
- De opmaak van stap 5 in de routine verandert (andere schrijfwijze van `to:`/`bcc:`): de parser vindt niets. De test faalt dan expliciet ("geen ontvangers gevonden") in plaats van stil groen te zijn.
- Terugdraaien: `tests/` en `tests.yml` verwijderen en CLAUDE.md terugzetten; niets anders hangt ervan af.

## 10. Open vragen
| Vraag | Default als er geen antwoord komt |
|---|---|
| Heeft de routine op claude.ai toegang tot deze repo (bron gekoppeld aan de routine)? Niet vast te stellen vanuit de repo. | F3 blijft open; de routine houdt de huidige `json.load`-controle. |
| Moet de test ook de volgorde van de rubrieken afdwingen (routine stap "RUBRIEKEN ... in deze volgorde")? | Ja, de volgorde van `categories` moet de volgorde uit de routine volgen voor de ids die er zijn. |

## 11. Uitvoering
Alleen aanvullen, nooit herschrijven. Alle meetgegevens per fase; het beslisdocument toont alleen dát een fase is uitgevoerd.

| Fase | Start | Einde | Opdracht van | Uitgevoerd door | Effort | Tokens invoer / uitvoer | Commits | Bron |
|---|---|---|---|---|---|---|---|---|
| F0 | 2026-10-02 17:25 | 2026-10-02 17:25 | Marco van Steenbrugge | claude-opus-5-5, sessie 6a787076-ce2d-5379-9282-08bfe806fdd8 | medium | 8 / 4.862 | 13e3fb6 | transcript (Claude Code 2.1.287) |

Tokens zijn invoer en uitvoer zonder cache. Is een waarde niet te meten, dan staat er "onbekend"; nooit een schatting.

### Toetsing per fase
Vóórdat een fase als gebouwd wordt gemarkeerd, is elk acceptatiecriterium uit punt 7 afzonderlijk getoetst met bewijs: een uitgevoerd commando met zijn uitvoer, of een aanwijsbare plek in een bestand. Alleen aanvullen: een nieuwe toetsing voegt rijen met een nieuw tijdstip toe, en alleen de laatste toetsing van een fase telt. Oordeel: gehaald, niet gehaald of niet toetsbaar.

| Fase | Tijdstip | Criterium | Controle en uitkomst | Oordeel |
|---|---|---|---|---|
| F0 | 2026-10-02 17:25 | 1. `python3 -m unittest discover -s tests -v` is groen op de huidige `site/data.json` | Uitgevoerd: 11 tests, "Ran 11 tests ... OK" | gehaald |
| F0 | 2026-10-02 17:25 | 2a. Kapotte komma laat de test rood worden met leesbare melding | Kopie met eerste komma verwijderd, `OP_PEIL_DATA=komma2.json`: "komma2.json is geen geldige JSON: Expecting ',' delimiter: line 3 column 2", FAILED (failures=11) | gehaald |
| F0 | 2026-10-02 17:25 | 2b. Onbekende item-cat laat de test rood worden | Kopie met items[0].cat = "onbekend": FAIL test_cat_bestaat, "items[0] 'AU 2026: Civil 3D wordt een Forma Connected Client': onbekende cat 'onbekend'", failures=1 | gehaald |
| F0 | 2026-10-02 17:25 | 2c. 6 highlights laat de test rood worden | Kopie met zesde highlight: FAIL test_highlights, "verwacht 5 highlights, gevonden 6", failures=1 | gehaald |
| F0 | 2026-10-02 17:25 | 2d. Item zonder URL laat de test rood worden | Kopie met items[0].urls = []: FAIL test_urls, "items[0] 'AU 2026: ...' heeft geen URL", failures=1 | gehaald |
| F0 | 2026-10-02 17:25 | 3. Geen andere afhankelijkheid dan de Python-standaardbibliotheek | `tests/test_data.py` regels 6-11: alleen datetime, json, os, re, unittest, pathlib | gehaald |

## 12. Afwijkingen
Ook een afwijkend model of afwijkende effort ten opzichte van "Gepland model en effort" (punt 7) staat hier, met de reden of "reden onbekend".

| Fase | Wat week af van het plan | Waarom |
|---|---|---|
| F0 | Scope: ook de volgorde van de rubrieken wordt gecontroleerd (`test_rubrieken`), niet genoemd in punt 6 | Default van de open vraag in punt 10 ("Ja, de volgorde ... volgen") |
| F0 | Scope: de te toetsen data is in te stellen met de omgevingsvariabele `OP_PEIL_DATA` | Nodig om acceptatiecriterium 2 op kopieën te toetsen; handig voor F3 |

## 13. Wijzigingslog
| Versie | Datum | Wat | Geraakt | Gevolg voor vrijgave |
|---|---|---|---|---|
| 1 | 2026-10-02 17:21 | Eerste versie | - | Nog geen vrijgave |

## 14. Bronnen
- `CLAUDE.md`, stand `ede3e54`
- `site/data.json` en `site/index.html` (regels 240-253), stand `ede3e54`
- `routine/ochtendroutine.md` (stappen 1, 3 en 5) en `routine/ontvangers.md`, stand `ede3e54`
- `.github/workflows/brbnt-scan.yml`, stand `ede3e54`

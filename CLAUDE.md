# Lutrea Op Peil: Project Root

## Project Overview
Lutrea Op Peil is een dagelijks vaknieuwsoverzicht voor civiel ontwerpers (Civil 3D, dijkontwerp, binnenstedelijk werk, grondwerk, inmeten en drones, AI, software en markt). Een Claude-routine zoekt elke werkdag nieuws, werkt de nieuwsdata bij, publiceert de pagina als Claude-artifact en mailt het team.

## Repository Structure
```
/
├── site/            # index.html (vaste pagina) en data.json (nieuws, agenda, bronnen, archief)
├── routine/         # ochtendroutine.md (instructie van de routine) en ontvangers.md
├── docs/            # Plannen en beslisdocumenten (zie "Plan en besluit")
├── memory/          # Geheugenarchief (MEMORY.md is de index)
├── .claude/skills/  # BRBNT-skills
├── README.md
└── CLAUDE.md        # Dit bestand
```

## Tech Stack
| Laag | Technologie |
|---|---|
| Frontend | Statische HTML, CSS en JavaScript in `site/index.html`, zonder build-stap |
| Data | `site/data.json`, door de pagina geladen met `fetch` |
| Hosting | Claude-artifact https://claude.ai/artifact/TeBB5UtsHJaTdeymdMsX3A |
| Automatisering | Claude-routine (werkdagen, `30 4 * * 1-5` UTC) met de Gmail-connector |
| CI/CD | {{nog geen CI}} |

## Architectuur
- `site/index.html` is vast; dagelijkse wijzigingen gaan alleen in `data.json`. De routine publiceert index.html ongewijzigd opnieuw.
- De live data staat bij het artifact op claude.ai; `site/data.json` in deze repo is een momentopname.
- `routine/ochtendroutine.md` is een kopie van de instructie van de routine op claude.ai. Wijzig je de een, werk dan de ander bij.
- Ontvangers van de ochtendmail staan in `routine/ontvangers.md` en in stap 5 van de routine-instructie; die twee moeten gelijk blijven.

---

## Git-regels
- Commit-berichten in het Nederlands.
- Alles gaat direct op main; dit project heeft één beheerder.
- Nooit `--force` zonder expliciete toestemming.

## Testing Strategy
Er is nog geen testsuite. De routine valideert `data.json` met Python (`json.load`) voordat hij publiceert.

---

## Gedragsregels
- Vraag door bij twijfel; nooit aannames doen over intentie of scope.
- Leg na elke wijziging kort uit wat en waarom.
- Werk in stappen: één logische eenheid per keer, niet alles ineens.
- Vraag altijd bevestiging vóór destructieve acties.

## Plan en besluit
<!-- brbnt-plan-regel: v1 -->
- Bij een nieuwe functie, een wijziging die uit meer dan één fase bestaat, een schema- of architectuurwijziging, of wanneer de gebruiker erom vraagt: stel eerst een plan en een beslisdocument op met de skill `brbnt-plan`, ook wanneer je in plan mode werkt. Bij een kleine, afgebakende fix is dat niet nodig.
- Bouw nooit voordat de beslisser akkoord heeft gegeven voor die fase in het beslisdocument. Ontbreekt het akkoord, of is het niet expliciet genoeg, dan stel je voor om het eerst op te halen in plaats van te beginnen.
- Plannen en beslisdocumenten staan in `docs/` als `<naam>.plan.md` en `<naam>.beslis.md`. Zoek eerst in `plan-beslis-index.md`, lees dan het beslisdocument, en open het plan alleen als je techniek nodig hebt.
- Commit-berichten voor planwerk beginnen met de fase-prefix uit het plan, bijvoorbeeld `F2:`.

## Scope-grenzen
- `site/`: de pagina en de nieuwsdata.
- `routine/`: hoe de dagelijkse editie tot stand komt en naar wie hij gaat.
- `docs/` en `memory/`: plannen, besluiten en het geheugenarchief; geen code.

## Conventies die worden afgedwongen (niet alleen gedocumenteerd)
Afgedwongen:
- {{Regel}}: afgedwongen door `{{pad naar test/lint-regel}}`

Nog niet afgedwongen, wel afgesproken:
- `site/data.json` is geldige JSON: alleen een controle in de routine, nog geen test in de repo.
- De ontvangers in `routine/ontvangers.md` en in `routine/ochtendroutine.md` zijn gelijk: alleen een afspraak, nog niet getest.

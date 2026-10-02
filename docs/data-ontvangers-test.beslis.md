---
beslis: data-ontvangers-test
titel: Test voor data.json en de ontvangerslijst
plan: data-ontvangers-test.plan.md
beslisser: Marco van Steenbrugge, beheerder
voorgelegd: 2026-10-02 17:21          # datum en tijd waarop de beslisser dit heeft gekregen; wordt door de skill gezet
status: ter-akkoord        # berekend door de skill, nooit met de hand gezet
---

> Legenda: ✅ akkoord of klaar · ✏️ akkoord, maar anders · ⏳ nog niet beoordeeld · 🔨 wordt gebouwd · ▶ vrijgegeven, nog niet gestart · ○ nog niet vrijgegeven · ⚠ vrijgave vervallen door planwijziging

# Beslisdocument: Test voor data.json en de ontvangerslijst

> **Nu van jou gevraagd:** besluiten B1 en B2, en daarna vrijgave voor F0 tot en met F2.
> **Later nodig:** B3 (vóór F3).

Er komt een automatische controle die nagaat of het nieuwsbestand van Op Peil in orde is en of de lijst met ontvangers van de ochtendmail op beide plekken hetzelfde is. Het werk is verdeeld in vier fasen; je geeft per fase akkoord.

## Vrijgave per fase
Een fase mag pas starten als de vrijgave er staat én alle besluiten waar de fase op leunt zijn genomen. Een vrijgave blijft geldig zolang het plan voor die fase en die besluiten niet is gewijzigd; het plan houdt dat bij in het wijzigingslog.

| Fase | Wat wordt gebouwd | Vrijgave | Door, wanneer | Leunt op | Gebouwd |
|---|---|---|---|---|---|
| F0 | Controle van het nieuwsbestand: klopt de opbouw en volgt het de regels van de ochtendroutine | ○ nog niet | - | B1, B2 | - |
| F1 | Controle dat de ontvangers in de ontvangerslijst en in de routine-instructie gelijk zijn | ○ nog niet | - | B1 | - |
| F2 | De controles draaien vanzelf op GitHub bij elke wijziging, en de projectregels noemen ze als afgedwongen | ○ nog niet | - | - | - |
| F3 | De ochtendroutine draait de controle zelf voordat hij publiceert | ○ nog niet | - | B3 | - |

## Overzicht besluiten
| | # | Onderwerp | Besluit | Nodig vóór |
|---|---|---|---|---|
| ⏳ | B1 | Testgereedschap | **Nog niet beoordeeld** | F0 |
| ⏳ | B2 | Datumregels toetsen tegen de editiedatum | **Nog niet beoordeeld** | F0 |
| ⏳ | B3 | Routine draait de controle vóór publiceren | **Nog niet beoordeeld** | F3 |

## Besluiten

### ⏳ B1 · Testgereedschap
**Je beslist:** met welk gereedschap de controles worden geschreven.

| | Ons voorstel | Alternatief |
|---|---|---|
| **Wat** | Python, alleen wat standaard al aanwezig is | Python met een extra testpakket (pytest) |
| **Voordeel** | Niets te installeren; de routine gebruikt al Python | Iets prettiger leesbare uitvoer |
| **Nadeel** | Uitvoer is wat kaler | Vraagt een installatie, lokaal en op GitHub |

**Jouw keuze**
- [ ] Akkoord met ons voorstel
- [ ] Anders:
- [ ] Vervalt

**Besloten door** nog niemand · **status** nog niet beoordeeld · **wacht op** Marco van Steenbrugge · **voorgelegd op** 2026-10-02 17:21 · **nodig vóór** F0

Meer uitleg: plan, punt 6, B1

### ⏳ B2 · Datumregels toetsen tegen de editiedatum
**Je beslist:** of de regels "berichten ouder dan 30 dagen gaan eruit" en "afgelopen evenementen gaan na een week eruit" worden gecontroleerd vanaf de datum van de editie, of helemaal niet.

| | Ons voorstel | Alternatief |
|---|---|---|
| **Wat** | Controleren vanaf de datum van de editie in het bestand | Deze twee regels niet controleren |
| **Voordeel** | Controleert of de editie klopte, en de test wordt niet vanzelf rood als de kopie in de repo ouder wordt | Eenvoudiger |
| **Nadeel** | Zegt niets over hoe oud de kopie in de repo is | Een vergeten opruimstap valt niet op |

**Jouw keuze**
- [ ] Akkoord met ons voorstel
- [ ] Anders:
- [ ] Vervalt

**Besloten door** nog niemand · **status** nog niet beoordeeld · **wacht op** Marco van Steenbrugge · **voorgelegd op** 2026-10-02 17:21 · **nodig vóór** F0

Meer uitleg: plan, punt 6, B2

### ⏳ B3 · Routine draait de controle vóór publiceren
**Je beslist:** of de ochtendroutine later zelf deze controle draait voordat hij de pagina publiceert, in plaats van alleen te kijken of het bestand leesbaar is.

| | Ons voorstel | Alternatief |
|---|---|---|
| **Wat** | Eerst F0 tot en met F2 bouwen, dan uitzoeken of de routine bij de repo kan en F3 daarna uitwerken | F3 laten vallen; de controle draait alleen op GitHub |
| **Voordeel** | Fouten worden gevangen vóórdat het team ze in de mail ziet | Niets aan de routine veranderen |
| **Nadeel** | Vraagt een aanpassing van de routine op claude.ai | De live editie wordt niet gecontroleerd, alleen de kopie in de repo |

**Jouw keuze**
- [ ] Akkoord met ons voorstel
- [ ] Anders:
- [ ] Vervalt

**Besloten door** nog niemand · **status** nog niet beoordeeld · **wacht op** Marco van Steenbrugge · **voorgelegd op** 2026-10-02 17:21 · **nodig vóór** F3

Meer uitleg: plan, punt 6, B3

## Historie
Alleen aanvullen, nooit herschrijven. De technische uitvoeringsdetails staan in het plan, punt 11.

| Datum en tijd | Wat | Door |
|---|---|---|
| 2026-10-02 17:21 | Plan opgesteld en voorgelegd | agent (Claude Code, Opus 5.5) |

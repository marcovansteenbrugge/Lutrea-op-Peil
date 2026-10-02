---
plan: zoektermen
titel: Eigen zoektermen met proefperiode en beslismoment
versie: 2
status: in-uitvoering        # berekend door de skill, nooit met de hand gezet
voortgang: F0 ✅ · F1 ⏳ · F2 ⏳ · F3 ⏳           # berekend door de skill
opgesteld: 2026-10-02
opgesteld_door: agent (Claude Code, Opus 5.5)
beslisser: Marco van Steenbrugge, beheerder
beslisdocument: zoektermen.beslis.md
basis_commit: 7457513
vervangt: -
samenvatting: Marco vult eigen zoektermen in op een privépagina; de routine zoekt er eerst op proef op, Marco beoordeelt de resultaten en zet een term pas daarna live in de nieuwsbrief.
trefwoorden: [zoektermen, proef, beslismoment, routine, artifact, db, hoofdgroepen, zoekboom]
---

# Plan: Eigen zoektermen met proefperiode en beslismoment

## 1. In het kort
1. Marco krijgt een invoerveld waarin hij eigen zoektermen zet die de nieuwsbrief aanvullen (bijvoorbeeld een project, een norm, een leverancier).
2. Een nieuwe term begint als **proef**: de ochtendroutine zoekt erop, maar de resultaten gaan niet in de nieuwsbrief of de mail. Ze staan alleen op Marco's eigen pagina.
3. Marco bekijkt de proefresultaten en kiest per term **Live zetten** of **Afwijzen**. Dat is het beslismoment.
4. Een live term wordt een vast onderdeel van de dagelijkse zoektocht; de berichten komen in de gewone rubrieken.
5. De teampagina en de mail blijven voor het team hetzelfde.

## 2. Aanleiding en doel
Nu bepaalt alleen de vaste instructie van de routine waarop wordt gezocht (`routine/ochtendroutine.md` stap 2, vijf subagents met vaste onderwerpen). Marco kan geen eigen onderwerpen toevoegen zonder de routine-instructie te wijzigen, en kan een onderwerp niet eerst uitproberen.

Geslaagd als: Marco een term kan invullen zonder Claude of de routine aan te raken; de volgende werkdag proefresultaten voor die term ziet die niet in de nieuwsbrief staan; met één klik een term live zet of afwijst; en een live term de werkdag daarna aantoonbaar meezoekt in de gewone editie.

## 3. Onderzoek en bevindingen
Getoetst tegen `7457513`.
- **De routine** (`routine/ochtendroutine.md`): leest het artifact en `data.json` met de Artifact-tool (stap 1), zoekt met 5 parallelle subagents met WebSearch/WebFetch (stap 2), werkt `data.json` bij (stap 3), publiceert (stap 4) en mailt (stap 5). Elke uitvoering is een nieuwe sessie met alleen deze instructie.
- **De teampagina** (`site/index.html`) is vast en heeft geen invoer behalve het vinkje "alleen nieuw vandaag" (regel 199). De routine publiceert haar elke dag ongewijzigd opnieuw zonder `capabilities` mee te geven; volgens de Artifact-tool blijft een eerder opgegeven declaratie dan staan.
- **Opslag voor invoer** (skill `artifact-capabilities`, runtime contract 0.2.66): een artifact-pagina kan met de capability `db` gegevens buiten de pagina bewaren, met toegangsregels per pad (bijvoorbeeld alleen de eigenaar schrijft). Claude leest en schrijft die gegevens met de tool `ArtifactData`. De capability `user` vertelt of de kijker de eigenaar is (`isOwner()`).
- **Zoeken vanaf de pagina zelf**: de capability `sample` laat een pagina Claude iets vragen, maar zonder websearch; resultaten over actueel nieuws zouden dan verzonnen kunnen zijn. Echt zoeken kan alleen in een Claude-sessie met WebSearch, zoals de routine. Een knop "nu proberen" kan zo'n sessie starten via de capability `mcp` met de connector "Claude Code Remote" (`fire_trigger` met tekst); zie B2.
- **Niet vastgesteld**: of de routine-sessie op claude.ai de tool `ArtifactData` heeft. Deze sessie heeft hem wel (als uitgestelde tool). Zie Open vragen; F0 toetst dit.
- **Proefzoektocht 2 oktober** (in de sessie, niet via de routine): per term één zoekopdracht. Recente berichten voor "Kademuren en bruggen vervanging" en "BRO"; vooral achtergrond voor "Bodemdaling slappe bodem", "Integraal Riviermanagement" en "Kustlijnzorg"; officiële bouwputmeldingen (ruis) voor "Bemaling grondwater"; niets voor "OTL Rijkswaterstaat" en "Kavel10" (wel bedrijfsinformatie onder de spelling "Kavel 10"). Conclusie: veel termen hebben geen dagelijks nieuws (B6).
- **Tests** (`tests/test_data.py`): items hebben verplichte velden en optioneel `unsure` en `tip`; een extra optioneel veld moet in `OPTIONEEL` worden toegevoegd, anders blijft de test groen maar ongecontroleerd (onbekende velden worden niet afgekeurd).

## 4. Niet in scope
- Zoektermen voor collega's: de pagina is voor Marco alleen (eigenaar).
- Een knop die direct, buiten de ochtendroutine om, zoekt: alleen als B2 daarvoor kiest; dan als aparte fase.
- Wijzigen van de teampagina `site/index.html`, behalve wat B4 eventueel vraagt.
- Automatisch live zetten op basis van een score: het beslismoment blijft altijd bij Marco.

## 5. Uitgangspunten
| Uitgangspunt | Herkomst |
|---|---|
| "Voor mezelf": de invoer is niet zichtbaar of bewerkbaar voor het team | verzoek van Marco, 2026-10-02 |
| Eerst testen of er bruikbare info uitkomt, daarna een beslismoment vóór live | verzoek van Marco, 2026-10-02 |
| De teampagina blijft vast; dagelijkse wijzigingen alleen in `data.json` | CLAUDE.md, Architectuur |
| Routine-instructie in de repo en op claude.ai blijven gelijk | CLAUDE.md, Architectuur |
| Niets verzinnen: alleen echte bronnen met URL | `routine/ochtendroutine.md` stap 2 |
| Hoofdgroepen ordenen alleen de eigen termen; de vaste zoektocht van de routine blijft ongewijzigd (optie 1) | Marco, 2026-10-02 18:53, via chat: "optie 1) daarna beslissen we maandag welke we houden" |
| Op maandag 5 oktober beslist Marco welke proeftermen hij houdt | idem |

## 6. Ontwerp en besluiten (technisch)
**Onderdelen**
1. **Privépagina "Op Peil zoektermen"** (nieuw artifact, `site/zoektermen.html` in de repo), met `capabilities: {db: {rules: ...}, user: {}}`. Alleen de eigenaar mag schrijven (`write: "owner"` op `zoektermen` en `proef`). Onderdelen:
   - invoer: zoekterm (verplicht), hoofdgroep (B5), rubriek (keuzelijst met de 11 rubrieken, of "laat de routine kiezen"), zoekfrequentie voor live (B6), korte notitie;
   - weergave per status, daarbinnen gegroepeerd per hoofdgroep;
   - lijst van termen met status `proef`, `live`, `afgewezen`, met datum toegevoegd en datum laatste beslissing;
   - per proefterm de proefresultaten per dag (titel als link, datum, samenvatting) en een teller;
   - knoppen **Live zetten**, **Afwijzen**, **Terug naar proef**, **Verwijderen**.
2. **Gegevens in de db** van dat artifact:
   - `zoektermen/<id>`: `{term, groep, cat|null, frequentie: "dagelijks"|"wekelijks", notitie, status: "proef"|"live"|"afgewezen", toegevoegd, besloten|null, beslotenDoor|null}`
   - `proef/<id>-<datum>`: `{termId, datum, resultaten: [{title, date, summary, urls[]}], opmerking}` (geschreven door de routine).
3. **Routine-uitbreiding** (`routine/ochtendroutine.md` en de routine op claude.ai):
   - nieuwe stap 1b: lees `zoektermen` met `ArtifactData` (`list`) van het zoektermen-artifact;
   - proeftermen: één extra subagent zoekt op alle proeftermen; de routine schrijft per term een `proef`-document (ook bij 0 resultaten, met opmerking) en zet deze resultaten **niet** in `data.json` en **niet** in de mail;
   - live termen met frequentie "dagelijks" elke werkdag, met "wekelijks" alleen op maandag en dan over de afgelopen 7 dagen; ze worden meegegeven aan de subagent van de gekozen rubriek (of aan alle, als de rubriek "laat de routine kiezen" is); hun berichten gaan als gewone items in `data.json`.
4. **Tests**: `tests/test_data.py` krijgt het optionele itemveld uit B4 in `OPTIONEEL` als B4 daarvoor kiest.

**Verdieping per besluit:**

- **B1 Waar komt het invoerveld** (nodig vóór F0). (a) Een aparte privépagina, alleen voor Marco, met eigen db. De teampagina en wat de routine daarop publiceert, blijven ongemoeid; geen risico dat een collega termen ziet of wijzigt. (b) Een verborgen deel op de teampagina, alleen zichtbaar als `user.isOwner()`. Eén pagina, maar de teampagina krijgt dan `db` en `user`, en de routine publiceert haar dagelijks opnieuw; een fout in dat deel raakt de pagina van het hele team. Voorstel: (a).
- **B2 Hoe de proefzoektocht draait** (nodig vóór F2). (a) Mee in de ochtendroutine: de proefresultaten staan er de volgende werkdag. Geen extra onderdelen; kost per proefterm een paar zoekopdrachten in de bestaande run. (b) Daarnaast een knop "Nu proberen" op de privépagina die via `mcp` met "Claude Code Remote" een aparte routine start (`fire_trigger` met de term als tekst); resultaat binnen enkele minuten. Vraagt een extra routine, toestemming voor de connector bij het openen van de pagina, en kost een aparte sessie per klik. Voorstel: (a) nu, (b) eventueel later als eigen plan.
- **B3 Het beslismoment** (nodig vóór F1). (a) Knoppen op de privépagina; alleen de eigenaar kan klikken; de pagina legt vast wie en wanneer. (b) Via chat met Claude, die de status zet. Voorstel: (a); dat werkt zonder Claude erbij en laat de beslissing zichtbaar achter.
- **B5 Hoofdgroepen** (nodig vóór F1). (a) Een vaste lijst van zeven hoofdgroepen uit het zoekboomvoorstel (https://claude.ai/artifact/GNMUZwBBSvkhHS8NJWfqDk): Waterveiligheid, Stad en openbare ruimte, Grond en bodem, Inmeten en data, Ontwerpsoftware en AI, Regels en kennis, Markt en opdrachtgevers; bij keuze van een groep stelt de pagina de bijbehorende rubriek voor. Wijzigen van de lijst gaat via een kleine aanpassing van de pagina. (b) Marco maakt zelf groepen aan en hernoemt ze op de pagina; flexibeler, maar meer knoppen en een extra collectie in de opslag. Voorstel: (a). De groep is alleen ordening: proef, live en afwijzen blijven per term.
- **B6 Zoekfrequentie** (nodig vóór F1). Uit de proefzoektocht van 2 oktober (zie punt 3) blijkt dat de meeste nieuwe termen niet dagelijks nieuws hebben. (a) Proeftermen elke werkdag; live termen per term "dagelijks" of "wekelijks" (op maandag, over 7 dagen, in de maandagbrief). Eén brief per dag blijft gelden. (b) Alles dagelijks. Voorstel: (a).
- **B4 Zijn berichten uit eigen zoektermen herkenbaar** (nodig vóór F3). (a) Een optioneel veld `term` per item in `data.json`, niet zichtbaar op de teampagina of in de mail; Marco kan op de privépagina zien wat elke live term oplevert. (b) Daarnaast een zichtbaar label op de teampagina. (c) Niet bijhouden. Voorstel: (a).

## 7. Fasering
Een fase mag starten als de vrijgave voor die fase er is én alle besluiten waar de fase op leunt zijn genomen. Een planwijziging raakt alleen de fasen en besluiten die in het wijzigingslog staan; de vrijgave van de overige fasen blijft geldig.

| Fase | Status | Scope | Acceptatie (toetsbaar) | Hangt af van | Omvang | Gepland model en effort | Commit-prefix |
|---|---|---|---|---|---|---|---|
| F0 | ✅ gebouwd | Proef op de techniek: leeg zoektermen-artifact met `db`, en één losse testroutine (eenmalig, geen mail, geen publish) die nagaat of een routine-sessie `ArtifactData` kan lezen en schrijven | 1. Het artifact bestaat en `ArtifactData list zoektermen` vanuit deze sessie werkt. 2. De testroutine heeft één testdocument gelezen en één document geschreven; dat is terug te lezen met `ArtifactData`. 3. De testroutine heeft geen mail verstuurd en niets gepubliceerd (transcript of tooloverzicht). 4. Het testdocument en de testroutine zijn opgeruimd. | B1 | S | Opus 5.5, medium | `F0:` |
| F1 | ⏳ wacht op B5, B6 | De privépagina: invoer met hoofdgroep en zoekfrequentie, lijst per status en per hoofdgroep, proefresultaten tonen, knoppen voor het beslismoment; bron in `site/zoektermen.html` | 1. Marco kan een term met hoofdgroep, rubriek, frequentie en notitie toevoegen; die staat daarna in `zoektermen` (ArtifactData). 2. Live zetten, afwijzen, terug naar proef en verwijderen veranderen de status met datum. 3. Een met ArtifactData geplaatst `proef`-document verschijnt bij de juiste term. 4. Een kijker die niet de eigenaar is kan niet schrijven (lezen met lager `as_level` en een geweigerde schrijfactie). 5. De pagina werkt op telefoonbreedte en in donkere modus. 6. Termen staan binnen elke status gegroepeerd per hoofdgroep; een bestaande term zonder groep staat onder "Zonder groep" en de groep is te wijzigen. 7. De frequentie is per term te wijzigen. | F0, B1, B3, B5, B6 | M | Opus 5.5, medium | `F1:` |
| F2 | ⏳ wacht op B2 | Routine zoekt op proeftermen en schrijft proefresultaten; `routine/ochtendroutine.md` en de routine op claude.ai bijgewerkt en gelijk | 1. De tekst in de repo en op claude.ai is gelijk (letterlijke vergelijking). 2. Na de eerstvolgende routinerun staat voor elke proefterm een `proef`-document van die dag, ook bij 0 resultaten. 3. Geen proefresultaat staat in `data.json` of in de mail van die dag. 4. Elk proefresultaat heeft minstens één URL. 5. De tests in `tests/` blijven groen. | F1, B2 | M | Opus 5.5, medium | `F2:` |
| F3 | ⏳ wacht op B4, B6 | Live termen zoeken mee in de gewone editie; `data.json` en `tests/test_data.py` volgens B4 | 1. Na de eerstvolgende run na het live zetten is de term meegegeven aan de juiste subagent (transcript). 2. Berichten uit een live term staan in de gewone rubrieken van `data.json` (en volgens B4 herkenbaar). 3. Een afgewezen term wordt niet meer gezocht. 4. Een wekelijkse term wordt alleen op maandag gezocht, over de afgelopen 7 dagen (transcript). 5. De tests in `tests/` zijn groen en controleren het veld uit B4. | F2, B4, B6 | S | Opus 5.5, medium | `F3:` |

Werkafspraak: één fase per keer, groene tests vóór de volgende fase, commit-berichten beginnen met de fase-prefix.

## 8. Gevolgen en bronnen voor afgeleide documenten
**Gegevens en privacy.** De db bevat zoektermen en notities van Marco en openbare nieuwsresultaten; geen persoonsgegevens van anderen. De pagina is privé (alleen de eigenaar schrijft; delen gebeurt alleen als Marco dat zelf doet).
**Beveiliging.** De routine leest de zoektermen als gegevens, niet als opdrachten: een term wordt alleen als zoekwoord gebruikt. Dat staat expliciet in de nieuwe routinestap.
**Gebruikers en handleiding.** Marco krijgt een nieuwe pagina met een uitleg van de drie statussen. Het team merkt alleen dat er berichten bij kunnen komen.
**Beheer en configuratie.** Nieuw artifact (URL komt in CLAUDE.md en README), nieuwe routinestap; bij F0 tijdelijk een testroutine die weer verdwijnt.
**Releasenotes (kernpunten).** Eigen zoektermen toevoegen, eerst op proef uitproberen en pas na eigen akkoord laten meelopen in Op Peil.

## 9. Risico's en terugweg
- De routine-sessie heeft geen `ArtifactData`: F0 vangt dit af vóór er iets gebouwd is. Terugweg: zoektermen opslaan in een bestand dat de routine met de Artifact-tool kan lezen; dat is een planwijziging.
- De routine wordt langer of duurder door extra zoekopdrachten. Beperking: maximaal een vast aantal proeftermen per dag (zie Open vragen).
- Een fout in de nieuwe routinestap laat de hele ochtendeditie mislukken. De stap wordt zo geschreven dat een fout bij de zoektermen gemeld wordt en de gewone editie doorgaat.
- Terugweg: de routinestap weghalen (repo en claude.ai); het zoektermen-artifact kan blijven staan of verwijderd worden.

## 10. Open vragen
| Vraag | Default als er geen antwoord komt |
|---|---|
| Heeft de routine-sessie op claude.ai de tool `ArtifactData`? | Wordt in F0 getoetst; bij nee een planwijziging. |
| Hoeveel proeftermen mag de routine per dag meenemen? | Maximaal 5; de oudste eerst. |
| Hoe lang blijft een term op proef zonder besluit? | Onbeperkt; de pagina toont hoeveel dagen hij al op proef staat. Marco beslist maandag 5 oktober over de eerste termen. |
| Moet de routine ook test B3 uit plan data-ontvangers-test (zelf de test draaien) meenemen, nu hij toch wordt aangepast? | Nee, apart houden. |

## 11. Uitvoering
Alleen aanvullen, nooit herschrijven. Alle meetgegevens per fase; het beslisdocument toont alleen dát een fase is uitgevoerd.

| Fase | Start | Einde | Opdracht van | Uitgevoerd door | Effort | Tokens invoer / uitvoer | Commits | Bron |
|---|---|---|---|---|---|---|---|---|
| F0 | 2026-10-02 17:38 | 2026-10-02 17:44 | Marco van Steenbrugge | claude-opus-5-5, sessie 6a787076-ce2d-5379-9282-08bfe806fdd8 | medium | 38 / 9.291 | 3fb8f7e | transcript (Claude Code 2.1.287); testroutine apart, sessie cse_01EM9Uf9R95r2HZ8HRieThoB, tokens onbekend |

Tokens zijn invoer en uitvoer zonder cache. Is een waarde niet te meten, dan staat er "onbekend"; nooit een schatting.

### Toetsing per fase
Vóórdat een fase als gebouwd wordt gemarkeerd, is elk acceptatiecriterium uit punt 7 afzonderlijk getoetst met bewijs: een uitgevoerd commando met zijn uitvoer, of een aanwijsbare plek in een bestand. Alleen aanvullen: een nieuwe toetsing voegt rijen met een nieuw tijdstip toe, en alleen de laatste toetsing van een fase telt. Oordeel: gehaald, niet gehaald of niet toetsbaar.

| Fase | Tijdstip | Criterium | Controle en uitkomst | Oordeel |
|---|---|---|---|---|
| F0 | 2026-10-02 17:44 | 1. Het artifact bestaat en `ArtifactData list zoektermen` vanuit deze sessie werkt | Gepubliceerd als https://claude.ai/artifact/71hvtjywngmBpL9iAiaFmi (versie 1, capabilities db met regel read/write owner, user). `ArtifactData set zoektermen/f0-test` gaf version 1; `list zoektermen` gaf 1 document terug. Extra: `list` met `as_level: admin` gaf "No documents matched", dus alleen de eigenaar leest | gehaald |
| F0 | 2026-10-02 17:44 | 2. De testroutine heeft één testdocument gelezen en één document geschreven; terug te lezen met `ArtifactData` | Testroutine trig_01ME15ocxucms6dpb37qmmcK, run SUCCEEDED (sessie cse_01EM9Uf9R95r2HZ8HRieThoB, 17:43:50-17:44:08 UTC), eindregel "F0-RESULTAAT: stap 2, 3 en 4 zijn alle drie gelukt". Vanuit deze sessie `list proef`: document f0-test-2026-10-02 met gelezenTerm "F0-testterm (wordt verwijderd)", version 1 | gehaald |
| F0 | 2026-10-02 17:44 | 3. De testroutine heeft geen mail verstuurd en niets gepubliceerd | Routine aangemaakt zonder connectors (`mcp_connections: []`), dus Gmail was niet beschikbaar. Transcript (list_events, assistant): alleen ToolSearch, ArtifactData get, ArtifactData set, ArtifactData get; geen Artifact publish | gehaald |
| F0 | 2026-10-02 17:44 | 4. Het testdocument en de testroutine zijn opgeruimd | `ArtifactData batch` delete zoektermen/f0-test en proef/f0-test-2026-10-02: committed; daarna `list zoektermen` en `list proef`: "No documents matched". `delete_trigger`: verwijderd; `get_trigger`: "not found" | gehaald |

## 12. Afwijkingen
Ook een afwijkend model of afwijkende effort ten opzichte van "Gepland model en effort" (punt 7) staat hier, met de reden of "reden onbekend".

| Fase | Wat week af van het plan | Waarom |
|---|---|---|
| F0 | Scope: de testroutine is aangemaakt zonder het veld connectors (het eerste verzoek met `connectors: []` werd geweigerd: "not available for this organization"); de routine kreeg toch geen connectors (`mcp_connections: []`) | Beperking van de organisatie |
| F0 | Scope: de toegangsregel is strenger dan in punt 6 (lezen én schrijven alleen door de eigenaar, op de hele opslag) | "Voor mezelf" (punt 5); de routine draait als Marco en voldoet daaraan, zoals F0 aantoonde |
| F0 | Scope: de bron van het skelet staat al in `site/zoektermen.html` (punt 7 noemt dat pas bij F1) | Dezelfde pagina wordt in F1 uitgebouwd |

## 13. Wijzigingslog
| Versie | Datum | Wat | Geraakt | Gevolg voor vrijgave |
|---|---|---|---|---|
| 1 | 2026-10-02 17:32 | Eerste versie | - | Nog geen vrijgave |
| 2 | 2026-10-02 18:53 | Hoofdgroepen (B5) en zoekfrequentie per term (B6) toegevoegd; F1 uitgebreid met groep, frequentie en criteria 6-7; F3 krijgt een criterium voor wekelijkse termen en leunt op B6; uitgangspunt optie 1 (vaste zoektocht ongewijzigd); bevinding proefzoektocht 2 oktober | F1, F3, B5, B6 | Vrijgave F1 (versie 1) vervalt; F0 blijft gebouwd; B1 en B3 blijven geldig |

## 14. Bronnen
- `routine/ochtendroutine.md` (stappen 1-5), stand `7457513`
- `site/index.html` (regels 133-199), stand `7457513`
- `tests/test_data.py`, stand `7457513`
- CLAUDE.md, stand `7457513`
- Skill `artifact-capabilities`, runtime contract 0.2.66 (capabilities `db`, `user`, `sample`, `mcp`)

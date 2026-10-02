# Index van plannen en beslisdocumenten

> Wordt door de skill gegenereerd uit de kopgegevens van elk plan en beslisdocument, nooit met de hand bijgehouden.
> Zoekvolgorde voor Claude: eerst deze index, dan het (korte) beslisdocument, en pas als er techniek nodig is het plan.
> Legenda: ✅ gebouwd · 🔨 lopend · ▶ vrijgegeven · ⏳ wacht op besluit · ⚠ vrijgave vervallen · ○ nog niet vrijgegeven

| Naam | Titel | Status | Voortgang per fase | Wacht op jou | Beslisser | Laatst vrijgegeven | Samenvatting | Trefwoorden |
|---|---|---|---|---|---|---|---|---|
| data-ontvangers-test | Test voor data.json en de ontvangerslijst | in-uitvoering | F0 ✅ · F1 ✅ · F2 ✅ · F3 ⏳ | B3 (vóór F3) | Marco van Steenbrugge, beheerder | F0 t/m F2, 2026-10-02 | Een testsuite die controleert dat site/data.json klopt met de afgesproken structuur en dat de ontvangers in ontvangers.md en de routine-instructie gelijk zijn. | test, data.json, ontvangers, routine, CI |
| zoektermen | Eigen zoektermen met proefperiode en beslismoment | in-uitvoering | F0 ✅ · F1 ⏳ · F2 ⏳ · F3 ⏳ | B5, B6 (vóór F1), B2 (vóór F2), B4 (vóór F3) | Marco van Steenbrugge, beheerder | F0, 2026-10-02 | Marco vult eigen zoektermen in op een privépagina; de routine zoekt er eerst op proef op, Marco beoordeelt de resultaten en zet een term pas daarna live in de nieuwsbrief. | zoektermen, proef, beslismoment, routine, artifact, db, hoofdgroepen, zoekboom |

**Statussen** (berekend, nooit met de hand gezet): concept · ter-akkoord · deels-vrijgegeven · vrijgegeven · in-uitvoering · gebouwd · afgerond · geparkeerd · vervallen.
Een plan is **deels-vrijgegeven** zodra minstens één fase mag starten terwijl andere fasen nog op een besluit wachten. Dat is een normale toestand, geen tussenstop: de vrijgegeven fasen kunnen al gebouwd worden.

**Naamgeving:** `docs/<naam>.plan.md` en `docs/<naam>.beslis.md` (sorteren samen), index: `docs/plan-beslis-index.md`.

# Lutrea Op Peil

Dagelijks vaknieuwsoverzicht voor civiel ontwerpers: Civil 3D, dijkontwerp, binnenstedelijk werk, grondwerk, inmeten en drones, AI, software en markt.

<!-- brbnt-scan:start (automatisch neergezet door de skill brbnt-scan; de inhoud tussen deze markeringen wordt bij een volgende installatie vervangen) -->
## BRBNT-scan

[![BRBNT-scan](../../raw/brbnt-dashboard/scan.svg)](../../blob/brbnt-dashboard/SCAN.md)

De stand van dit project per laag, met het bewijs per criterium: [SCAN.md](../../blob/brbnt-dashboard/SCAN.md). Het volledige dashboard: open [dashboard.html](../../blob/brbnt-dashboard/dashboard.html), kies "Download raw file" en open het bestand; het werkt ook zonder internet. Wordt automatisch bijgewerkt na elke push naar main en elke ochtend.
<!-- brbnt-scan:end -->

- **Pagina:** https://claude.ai/artifact/TeBB5UtsHJaTdeymdMsX3A (alleen voor wie toegang heeft via Share)
- **Ochtendmail:** elke werkdag rond 06:30, zie `routine/ontvangers.md`
- **Routine:** een Claude-routine zoekt elke ochtend nieuws met vijf agents, werkt `data.json` bij, publiceert de pagina en verstuurt de mail. De instructie staat in `routine/ochtendroutine.md`.

## Indeling

| Map | Inhoud |
|---|---|
| `site/` | `index.html` (vaste pagina) en `data.json` (nieuws, agenda, bronnen, archief) |
| `routine/` | de instructie van de ochtendroutine en de ontvangerslijst |
| `.claude/skills/` | de BRBNT-skills voor werken met Claude in dit project |

`site/data.json` is een momentopname; de live versie staat bij de pagina op claude.ai.

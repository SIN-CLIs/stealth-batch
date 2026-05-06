# sinrules.md — stealth-batch: Regeln & Verbote

> **← [stealth-runner/sinrules.md](https://github.com/OpenSIN-AI/stealth-runner/blob/main/sinrules.md) ist das zentrale Regelwerk.**
> Alle Golden Rules sind DORT definiert. Diese Datei ist der Repo-spezifische Mirror.
> **Gültig ab**: 2026-05-05

---

## §1 — Stealth Suite Compliance

Dieses Repo (stealth-batch) ist Teil der **SIN-CLIs Stealth Suite** und MUSS:
1. Alle Regeln aus [stealth-runner/sinrules.md](https://github.com/OpenSIN-AI/stealth-runner/blob/main/sinrules.md) befolgen
2. BANNED Tools vermeiden: webauto-nodriver (absolut), skylight-cli (deprecated), CDP (nur JS)
3. CUA-ONLY Architektur für Browser-Interaktion respektieren
4. Pipeline: perceive → plan → guard → execute → critique

## §2 — Repo-spezifische Verbote

- NIE ohne Pipeline guard.execute() ausführen
- NIE Koordinaten-basiertes Klicken (pyautogui/pynput)
- NIE CDP für Navigation/Klicks
- NIE `pkill -f "heypiggy-bot"` oder `killall Google Chrome`

## §3 — Pflicht-Dokumentation

Alle 14 Pflichtdateien MÜSSEN existieren und aktuell sein.
Check mit: `python3 /Users/jeremy/dev/stealth-runner/scripts/check_doc_health.py --repo stealth-batch`

**Letztes Update**: 2026-05-05

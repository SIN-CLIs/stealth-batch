# banned.md — Verbotene Methoden (stealth-batch)

> **← [stealth-runner/banned.md](https://github.com/OpenSIN-AI/stealth-runner/blob/main/banned.md) für vollständige Liste**

---

## ABSOLUT BANNED

| Tool/Methode | Grund | Ersatz |
|-------------|-------|--------|
| `webauto-nodriver` | MCP-Server, CDP-Missbrauch | cua-driver |
| `skylight-cli` | Index instabil, DEPRECATED | cua-driver |
| CDP Navigation/Klicks | Chrome blockiert, unsicher | cua-driver |
| `pyautogui` | Mausbewegung | cua-driver AXPress |
| `pynput` | Mausbewegung | cua-driver AXPress |
| `pkill -f "heypiggy-bot"` | Killt USER Chrome mit! | `SessionManager.close_all()` |

## BEDINGT ERLAUBT

| Tool | Bedingung |
|------|-----------|
| CDP JS evaluate | NUR für `Runtime.evaluate()` — keine Navigation |
| macos-ax-cli | NUR für System-Scan — nicht für Klicks |

**Letztes Update**: 2026-05-05

# fix.md — Fehlerlog (stealth-batch)

> **Zweck**: Jeder Fehler wird hier mit Datum, Ursache und Korrektur dokumentiert.

---

## 2026-05-05

### Doc-Health Bootstrap
- **Ursache**: Repo hatte keine Pflichtdokumentation
- **Korrektur**: Alle 14 Pflichtdateien via stealth-runner Mass Generator erstellt
- **Betroffene Dateien**: Alle .md im Root


## 2026-05-07 Live Debugging Fixes

### Fix #5: Balance reads 125€ instead of 2.23€
- **ROOT CAUSE**: `read_balance()` took Math.max of all numbers near €. Level progress "125" appeared near € sign.
- **FIX**: Changed to `if (val > 1.0 && val < 1000)` and check adjacent lines for "Level"/"Min" keywords
- **FILE**: survey-cli/survey/scanner.py :: read_balance()
- **VERIFIED**: Balance now reads 2.23€ consistently

### Fix #6: React form inputs not accepting .value
- **ROOT CAUSE**: React synthetic events ignore direct .value= setter
- **FIX**: Use `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(el, val)` + dispatchEvent('input') + dispatchEvent('change')
- **FILE**: survey-cli/survey/snapshot.py
- **VERIFIED**: Zip=10785, Age=53 accepted, button enables

### Fix #7: Multiple stacked modals blocking clicks
- **ROOT CAUSE**: 7-9 layered modals at identical coordinates
- **FIX**: Close all "Schließen" buttons via JS before interacting with survey
- **VERIFIED**: Survey questions visible after closing modals

### Fix #8: Modal-only element scanning
- **ROOT CAUSE**: ELEMENT_EXTRACTOR_JS scanned entire document (84+ elements)
- **FIX**: Topmost modal detection by viewport center distance
- **VERIFIED**: Element count reduced to 3-5 for modal surveys

### Fix #9: New tab detection for Qualtrics
- **ROOT CAUSE**: Survey navigates to external URL in new tab
- **FIX**: Check tab count via /json before/after clickSurvey()
- **VERIFIED**: Survey questions visible after connecting to correct tab

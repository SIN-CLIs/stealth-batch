# learn.md — Learnings (stealth-batch)

> **Zweck**: Positive Erkenntnisse und Best Practices.

---

## 2026-05-05

### Doc-System Bootstrap
- **Erkenntnis**: Standardisierte Pflichtdateien machen Repos agenten-lesbar
- **Best Practice**: Jedes Repo braucht sinrules.md + brain.md + registry.md als Minimum


## §Q — LIVE CRASH-TEST DISCOVERIES (2026-05-07)

> **Status**: 10+ discoveries during live debugging marathon on heypiggy.com
> **Source**: stealth-runner/survey-cli CDP automation

### §Q1 — Surveys open in NEW tabs
Surveys navigate to external URLs (Qualtrics, Samplicio) in NEW Chrome tabs.
CDP connection stays on dashboard tab. MUST detect new tab and reconnect.
```python
# After clickSurvey(), check for new tabs
tabs_after = json.loads(urllib.request.urlopen('http://127.0.0.1:9999/json'))
if len(tabs_after) > len(tabs_before):
    new_tab = [t for t in tabs_after if t['id'] not in seen_ids][0]
    ws_url = f"ws://127.0.0.1:9999/devtools/page/{new_tab['id']}"
```

### §Q2 — Multiple stacked modals on heypiggy
Dashboard has 7-9 layered modals at identical z-index and coordinates.
Clicking "Nächste" at (600,547) hits "Schließen" button instead.
**Fix**: Close all stacked modals via JS before interacting.

### §Q3 — React form filling requires native value setter
`.value = 'X'` does NOT trigger React onChange. Must use:
```javascript
var nativeSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
nativeSetter.set.call(el, '10785');
el.dispatchEvent(new Event('input', {bubbles: true}));
el.dispatchEvent(new Event('change', {bubbles: true}));
```
Alternative: `document.execCommand('insertText', false, val)` for text areas.

### §Q4 — Qualtrics language selector is <select> dropdown
The language picker is `<select class="Q_lang">` with `<option>Deutsch</option>`.
NOT a set of clickable labels. Must set `selectedIndex` + dispatch change event.

### §Q5 — Balance read bug (125€ vs 2.23€)
`read_balance()` used `Math.max()` of all € values on page.
Level progress "125" appeared near € symbol. Fixed by filtering `val > 1.0 && val < 1000`.

### §Q6 — Fill-by-element-ID is most reliable
Angular Material generates dynamic IDs: `Age`, `Zip`, `mat-radio-X-input`, `next_0`.
`document.getElementById('Age')` far more reliable than querySelector approaches.

### §Q7 — CDP Input.dispatchMouseEvent for real clicks
`element.click()` via Runtime.evaluate fails on layered React modals.
Use CDP's Input domain for real mouse events at exact coordinates.

### §Q8 — cua-driver needs --force-renderer-accessibility
cua-driver returns 0 AX elements when Chrome lacks the accessibility flag.
Chrome started without this flag is invisible to macOS accessibility tools.

### See also
- **fix.md**: Fixes #5-#9 (balance, React forms, stacked modals, modal snapshot, tab detection)
- **issues.md**: 11 open issues (3 P0, 3 P1, 3 P2, 2 P3)
- **stealth-runner**: Primary implementation repo at SIN-CLIs/stealth-runner

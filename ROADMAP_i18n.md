# Internationalization (i18n) Roadmap — DrumBurp

**Goal:** Full Qt Linguist support for all user-visible strings, starting with
English (reference) and Spanish, with a clean path to add more languages.

**Total strings:** 625 across 24 translation contexts (622 original + 3 from language menu)  
**Languages:** English (built-in reference), Spanish (`es`)

---

## Phase 0 — Infrastructure

- [x] Create `src/i18n/` directory
- [x] Create `src/i18n/i18n.py` — translation loader
- [x] Add `--language` CLI option to `src/DrumBurp.py`
- [x] Add `LANGUAGE` environment variable support
- [x] Install translator in `DrumBurp.py` before any UI is created
- [x] `i18n.py` handles PyInstaller frozen builds (`sys._MEIPASS`)
- [x] Create `drumburp.pro` — Qt project file for `pylupdate5`
- [x] Run `pylupdate5 drumburp.pro` — generates `drumburp_en.ts` and `drumburp_es.ts`
- [x] English `.ts` filled (622 strings, all marked finished)
- [x] Add `lrelease` step to `build/build_linux.sh`
- [x] Add `lrelease` step to `build/build_windows.ps1`
- [x] Add `.qm` files to PyInstaller `--add-data` in both build scripts
- [x] Add `lrelease` + `qttools5-dev-tools` step to `.github/workflows/build.yml`
- [x] Add i18n section to `README.md`
- [x] Add i18n section to `README_ES.md`

---

## Phase 1 — Wrap strings in Python code

### Files completed

- [x] `src/DrumBurp.py` — `--language` option, `install_translator()` call
- [x] `src/GUI/DBMainwindow.py` — all QMessageBox, status, dialog, window title strings
- [x] `src/GUI/DBInfoDialog.py` — window title, version text, port credit labels
- [x] `src/GUI/DBStartupDialog.py` — welcome window title
- [x] `src/GUI/QScore.py` — load/save errors, kit change confirmation
- [x] `src/GUI/QMeasureContextMenu.py` — delete staff/section/measures confirmations
- [x] `src/GUI/QLilypondPreview.py` — all build/export error messages
- [x] `src/GUI/QDefaultKitManager.py` — kit name dialog, duplicate/overwrite errors
- [x] `src/GUI/QEditKitDialog.py` — kit saved message

### Files that need no wrapping (all strings in .ui files)

- [x] `src/GUI/DBColourPicker.py` — no dynamic strings
- [x] `src/GUI/QAlternateDialog.py` — no dynamic strings
- [x] `src/GUI/QAlternateWidget.py` — no dynamic strings
- [x] `src/GUI/QComplexCountDialog.py` — no dynamic strings
- [x] `src/GUI/QInsertMeasuresDialog.py` — no dynamic strings
- [x] `src/GUI/QRepeatCountDialog.py` — no dynamic strings
- [x] `src/GUI/QVersionDownloader.py` — no dynamic strings
- [x] `src/GUI/DBLicense.py` — no dynamic strings
- [x] `src/GUI/QEditMeasureDialog.py` — no dynamic strings
- [x] `src/GUI/QMetaDataDialog.py` — no dynamic strings
- [x] `src/GUI/QNewScoreDialog.py` — no dynamic strings
- [x] `src/Widgets/measureTabs.py` — no dynamic strings

---

## Phase 2 — Spanish translation: file by file

622 strings total. **ALL DONE — 622/622 translated.**

### Group A — Tiny dialogs (≤ 6 strings each) — 47 strings total

- [x] `repeatCountDialog` (3 strings)
- [x] `dbLicense_dialog` (3 strings)
- [x] `dbStartup` (2 strings)
- [x] `measurePropertiesDialog` (2 strings)
- [x] `QEditKitDialog` (2 strings)
- [x] `AlternateDialog` (4 strings)
- [x] `AlternateWidget` (6 strings)
- [x] `ColourPicker` (6 strings)
- [x] `QMeasureContextMenu` (6 strings)
- [x] `QScore` (6 strings)
- [x] `QDefaultKitManager` (6 strings)
- [x] `newScoreDialog` (6 strings)

### Group B — Small dialogs (9–19 strings each) — 87 strings total

- [x] `InsertMeasuresDialog` (9 strings)
- [x] `QLilypondPreview` (10 strings)
- [x] `InfoDialog` (10 strings)
- [x] `DBInfoDialog` (4 strings)
- [x] `DBStartupDialog` (1 string)
- [x] `VersionDownloader` (3 strings)
- [x] `complexCountDialog` (14 strings)
- [x] `measureTabs` (15 strings)
- [x] `asciiDialog` (19 strings)
- [x] `ScoreDialog` (19 strings)

### Group C — Medium dialogs — 34 strings total

- [x] `DefaulKitManager` (17 strings)

### Group D — Main application strings (62 strings)

- [x] `DrumBurp` (62 strings)

### Group E — Main window UI (240 strings)

- [x] `DrumBurpWindow` (240 strings)

### Group F — Kit editor (147 strings)

- [x] `editKitDialog` (147 strings)

---

## Phase 3 — Compile and test

- [x] Run `lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm`
- [x] Run `lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm`
- [x] Verified Spanish translator loads and translates strings correctly (automated test)
- [ ] Full manual test: `LANGUAGE=es ./run-drumburp.sh` — open menus, dialogs, error messages
- [ ] Fix any missing or broken strings found during manual test
- [ ] Re-run `pylupdate5` + `lrelease` if fixes are needed

---

## Phase 4 — Build integration

- [x] `build/build_linux.sh` — `lrelease` step + `--add-data` for `.qm` files
- [x] `build/build_windows.ps1` — `lrelease` step + `--add-data` for `.qm` files
- [x] `.github/workflows/build.yml` — `qttools5-dev-tools` installed + `lrelease` step
- [x] `src/i18n/i18n.py` — handles PyInstaller frozen builds via `sys._MEIPASS`

---

## Phase 5 — Developer documentation

- [x] Add i18n section to `README.md`
- [x] Add i18n section to `README_ES.md`

---

## Phase 6 — Runtime language switching

- [x] `_buildLanguageMenu()` in `DBMainwindow.py` — builds `Help > Language`
      submenu dynamically from available `.qm` files in `src/i18n/`
- [x] `_selectLanguage()` in `DBMainwindow.py` — saves chosen language to
      `QSettings` key `"Language"` and shows restart notice
- [x] `DrumBurp.py` — reads `QSettings["Language"]` at startup (after
      `setOrganizationName`) so saved preference takes effect before any UI
- [x] Priority order: `--language` CLI flag > `QSettings` > `LANGUAGE` env var
      > system locale
- [x] `QActionGroup` used so only one language is checked at a time
- [x] 3 new strings added (`Language`, `Language changed`, restart notice),
      translated in both EN and ES, `.qm` files recompiled (625 strings total)

---

## Phase 7 — Future

- [ ] French (`fr`), German (`de`), Portuguese (`pt`) translations
      (add to `drumburp.pro`, run `pylupdate5`, translate, `lrelease`)

---

## Quick reference

```bash
# Extract/update strings from source into .ts files
pylupdate5 drumburp.pro

# Compile .ts to binary .qm
lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm
lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm

# Open Qt Linguist GUI
linguist src/i18n/drumburp_es.ts

# Test in Spanish
LANGUAGE=es ./run-drumburp.sh
./run-drumburp.sh --language es

# Count remaining untranslated strings (should be 0)
grep -c 'type="unfinished"' src/i18n/drumburp_es.ts
```

---

## Progress

| Group | Context | Strings | Status |
|-------|---------|---------|--------|
| A | repeatCountDialog | 3 | [x] |
| A | dbLicense_dialog | 3 | [x] |
| A | dbStartup | 2 | [x] |
| A | measurePropertiesDialog | 2 | [x] |
| A | QEditKitDialog | 2 | [x] |
| A | AlternateDialog | 4 | [x] |
| A | AlternateWidget | 6 | [x] |
| A | ColourPicker | 6 | [x] |
| A | QMeasureContextMenu | 6 | [x] |
| A | QScore | 6 | [x] |
| A | QDefaultKitManager | 6 | [x] |
| A | newScoreDialog | 6 | [x] |
| B | InsertMeasuresDialog | 9 | [x] |
| B | QLilypondPreview | 10 | [x] |
| B | InfoDialog | 10 | [x] |
| B | DBInfoDialog | 4 | [x] |
| B | DBStartupDialog | 1 | [x] |
| B | VersionDownloader | 3 | [x] |
| B | complexCountDialog | 14 | [x] |
| B | measureTabs | 15 | [x] |
| B | asciiDialog | 19 | [x] |
| B | ScoreDialog | 19 | [x] |
| C | DefaulKitManager | 17 | [x] |
| D | DrumBurp | 62 | [x] |
| E | DrumBurpWindow | 240 | [x] |
| F | editKitDialog | 147 | [x] |
| — | **Total** | **625** | **625 done ✓** |

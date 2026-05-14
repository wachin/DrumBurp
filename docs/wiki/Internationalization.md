# Internationalization (i18n)

DrumBurp supports multiple languages via Qt Linguist.

---

## Changing the language

### From the menu (persistent)

Go to **Help → Language** and select a language. DrumBurp will show a
message saying the change takes effect on the next launch. The preference
is saved automatically.

### From the command line (one session)

```bash
# Spanish
LANGUAGE=es ./run-drumburp.sh
./run-drumburp.sh --language es

# English (explicit)
./run-drumburp.sh --language en

# Use system locale
./run-drumburp.sh
```

---

## Available languages

| Code | Language |
|------|----------|
| `en` | English (built-in) |
| `es` | Español (Spanish) |

---

## Score metadata and language

The title, artist, and tabber fields in a score are stored as literal text
inside the `.brp` file. The default values for **new scores** are
translated (e.g. "Sin titulo" in Spanish), but **existing files** keep
whatever text was stored when they were saved.

> **Example:** If you open a file that was created before the i18n update,
> the Lilypond preview will show "Untitled", "Unknown", and "Nobody" even
> when running in Spanish. To fix this, open
> **Score → Edit Score Properties** and update the fields manually.

---

## Adding a new language (for developers)

1. Add the new `.ts` file to `drumburp.pro`:
   ```
   TRANSLATIONS = src/i18n/drumburp_en.ts \
                  src/i18n/drumburp_es.ts \
                  src/i18n/drumburp_fr.ts
   ```
2. Run `pylupdate5 drumburp.pro` — creates the new `.ts` file
3. Translate with Qt Linguist: `linguist src/i18n/drumburp_fr.ts`
4. Compile: `lrelease src/i18n/drumburp_fr.ts -qm src/i18n/drumburp_fr.qm`
5. Test: `LANGUAGE=fr ./run-drumburp.sh`

See `ROADMAP_i18n.md` in the repository for the full technical details.

---

## Install translation tools

```bash
sudo apt install pyqt5-dev-tools qttools5-dev-tools
# provides: pylupdate5, lrelease, linguist
```

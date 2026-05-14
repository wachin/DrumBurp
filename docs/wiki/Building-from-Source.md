# Building from Source

## Running directly (development)

```bash
git clone https://github.com/wachin/DrumBurp.git
cd DrumBurp

# Install dependencies
sudo apt install python3-pyqt5 python3-pygame python3-pyqt5.qtmultimedia \
                 pyqt5-dev-tools lilypond fluid-soundfont-gm

# Run
./run-drumburp.sh
```

---

## Running the test suite

```bash
PYTHONPATH=src python3 -m unittest discover -s src/test
```

Expected result: **373 tests, all OK**

---

## Building a standalone Linux binary (PyInstaller)

```bash
# Install build dependencies
pip install pyinstaller

# Build
bash build/build_linux.sh
```

The binary is created at `build/dist/DrumBurp`.

---

## Building a Windows installer (NSIS)

Requires Windows with Python 3.11, NSIS, and the packages in
`build/requirements-windows.txt`.

```powershell
pip install -r build/requirements-windows.txt
.\build\build_windows.ps1
```

The installer is created at `build/output/DrumBurp-X.Y.Z.0-setup.exe`.

---

## Regenerating UI files

If you modify a `.ui` file in Qt Designer:

```bash
pyuic5 src/GUI/archivo.ui -o src/GUI/ui_archivo.py
```

Then restore the `_rc` import at the top of the generated file according
to the resource map in `migration_report_pyqt5.md`.

---

## Regenerating resource files

If you modify a `.qrc` file:

```bash
pyrcc5 src/GUI/DrumBurp.qrc    -o src/GUI/DrumBurp_rc.py
pyrcc5 src/buttons.qrc         -o src/buttons_rc.py
pyrcc5 src/Widgets/buttons.qrc -o src/Widgets/buttons_rc.py
```

---

## Updating translations

```bash
# Re-extract strings from source
pylupdate5 drumburp.pro

# Translate new strings
linguist src/i18n/drumburp_es.ts

# Compile
lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm
lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm
```

---

## GitHub Actions (CI/CD)

Pushing a tag triggers automatic builds and a GitHub Release:

```bash
# Update version in these three files:
# - VERSION
# - src/DBVersionNum.py
# - build/DrumBurp.nsi

git add VERSION src/DBVersionNum.py build/DrumBurp.nsi
git commit -m "Bump version to 1.1.4"
git tag v1.1.4
git push origin dev
git push origin v1.1.4
```

See `docs/publicar-release-github-actions.md` for the full tutorial.

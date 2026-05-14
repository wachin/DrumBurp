# Informe de migracion PyQt4 -> PyQt5

**Proyecto:** DrumBurp — editor de notacion de bateria en Python/PyQt  
**Repositorio:** https://github.com/Whatang/DrumBurp  
**Port realizado por:** Washington Indacochea Delgado  
**Email de contacto:** linuxfrontier@proton.me  
**Iniciado:** 2026-03-28  
**Sistema de destino:** Debian 12 / UbuntuStudio, Python 3.11, PyQt5 5.15.x

---

## Contexto del proyecto

DrumBurp es una aplicacion de escritorio para crear y editar notacion musical
de bateria. Usa PyQt para la interfaz grafica, QGraphicsScene/QGraphicsItem
para el editor visual, QThread para MIDI y exportacion Lilypond, y QSettings
para persistencia.

Estructura de directorios relevante:

```
src/
  DrumBurp.py          # punto de entrada
  Data/                # modelos de datos (Score, Measure, Drum, etc.)
  GUI/                 # ventana principal, dialogos, escena grafica
  Widgets/             # widgets custom (ScoreView, measureTabs)
  Notation/            # exportacion ASCII, Lilypond
  test/                # suite de tests unitarios
  buttons.qrc          # recursos QRC (iconos de botones y cabezas de nota)
  buttons_rc.py        # generado por pyrcc5 desde buttons.qrc
build/                 # scripts de empaquetado
.github/workflows/     # CI GitHub Actions
```

Dependencias principales (ver `requirements-debian12.txt`):

- Python 3.11+
- PyQt5 5.15.x — paquete `python3-pyqt5`
- pyqt5-dev-tools — paquete `pyqt5-dev-tools` (incluye `pyuic5` y `pyrcc5`)
  Instalacion: `sudo apt install pyqt5-dev-tools`
- python3-pyqt5.qtmultimedia — para MIDI
- lilypond 2.24.x — para exportacion de partitura (opcional)

---

## Estado general — MIGRACION COMPLETA

La migracion de PyQt4 a PyQt5 esta completa. El programa:

- [x] Arranca sin errores ni tracebacks
- [x] Abre y edita archivos `.brp`
- [x] Reproduce MIDI
- [x] Exporta a PDF via LilyPond 2.24
- [x] Exporta ASCII
- [x] Imprime
- [x] 373 tests unitarios pasan

---

## Estrategia de migracion

- [x] 1. Mantener temporalmente `src/PyQt4` mientras se corrigen errores funcionales.
- [x] 2. Migrar directo a `PyQt5` (sin capa intermedia `GUI/QtCompat.py`).
- [x] 3. Regenerar los archivos `ui_*.py` con `pyuic5`.
- [x] 4. Regenerar los archivos `*_rc.py` con `pyrcc5`.
- [x] 5. Migrar codigo manual por grupos: arranque, dialogos, score/graphics,
         preferencias, MIDI, exportacion.
- [x] 6. Eliminar la capa temporal `src/PyQt4/` completa.
- [x] 7. Verificar que `grep -R PyQt4` no devuelve resultados en codigo fuente.

---

## Cambios generales PyQt4 -> PyQt5

Referencia rapida para cualquier editor que retome este trabajo:

- [x] `PyQt4.QtGui` dividido en `PyQt5.QtWidgets`, `PyQt5.QtGui` y `PyQt5.QtPrintSupport`.
- [x] `QApplication`, `QDialog`, `QWidget`, layouts, menus, acciones, message boxes,
      `QGraphicsView`, `QGraphicsScene`, `QGraphicsItem`, `QUndoStack`,
      `QUndoCommand` → `QtWidgets`.
- [x] `QFont`, `QFontMetrics`, `QPixmap`, `QIcon`, `QColor`, `QPen`, `QTransform`,
      `QTextCursor` → `QtGui`.
- [x] `QPrinter`, `QPrinterInfo`, `QPrintPreviewDialog` → `QtPrintSupport`.
- [x] `QVariant` eliminado: se usan valores Python directamente.
- [x] `.toInt()`, `.toBool()`, `.toString()`, `.toStringList()` reemplazados por
      conversiones Python o `QSettings.value(..., type=...)`.
      Nota: los `hasattr(value, "toString")` que quedan en `_settingsValue` son
      codigo defensivo para leer settings guardados con PyQt4 — no son un problema.
- [x] `QDesktopServices.storageLocation()` → `QStandardPaths.writableLocation()`.
- [x] `QtCore.SIGNAL(...)` / `QtCore.QObject.connect(...)` → `obj.signal.connect(slot)`.
- [x] `@pyqtSignature(...)` eliminado y reemplazado por `@pyqtSlot(...)`.
- [x] `QApplication.UnicodeUTF8` y `QtCore.QString.fromUtf8` eliminados.
- [x] `QLayout.setMargin()` → `setContentsMargins(...)`.
- [x] `QGraphicsItem.setAcceptsHoverEvents()` → `setAcceptHoverEvents()`.
- [x] `QGraphicsItemGroup` → `QGraphicsItem` con `setParentItem` (en `QStaff`).
- [x] `QFontMetrics.width(text)` → `horizontalAdvance(text)`.
- [x] `exec_()` → `exec()` en todos los dialogos y el event loop principal.

---

## Cambios Python 2 -> Python 3

- [x] `NotePosition.__cmp__`/`cmp()` → `__eq__`/`__lt__`/`__le__`/`__gt__`/`__ge__`/`__hash__`
      (`src/Data/NotePosition.py`).
- [x] `MeasureCount.counterMaker`: division `/` → `//` para evitar float
      (`src/Data/MeasureCount.py`).
- [x] `MeasureCount.iterMidiTicks`/`iterTimesMs`: argumento `swing` hecho opcional
      con default `0` (`src/Data/MeasureCount.py`).
- [x] `Drum.checkShortcuts`: `set.pop()` → `min()` para orden deterministico
      (`src/Data/Drum.py`).
- [x] `fileUtils.Base64StringField`: codec Python 2 `str.encode('base64')` →
      modulo `base64` de Python 3 (`src/Data/fileUtils.py`).
- [x] `dbfsv0.startBarlineString`/`endBarlineString`: corregida logica de bitmask
      para `NO_BAR` (valor 0 siempre pasaba `& 0 == 0`) (`src/Data/fileStructures/dbfsv0.py`).
- [x] `DBMidi.py`: divisiones enteras en calculos MIDI corregidas:
      - `midiVolume / FLAM_VOLUME_CONSTANT` → `//` (volumen MIDI debe ser entero)
      - `MIDITICKSPERBEAT / FLAM_TIME_CONSTANT` → `//` (ticks deben ser enteros)
      - `divisionTicks / 2` → `//` (offset de ticks debe ser entero)
- [x] `Notation/lilypond.py`: divisiones enteras en calculos de duracion corregidas:
      - `note / 2` y `restNote / 2` en comparaciones de ticks → `//`
      - `headCount / 26` en generacion de nombres → `//` (argumento de `chr()`)

---

## Archivos generados por pyuic4 → regenerados con pyuic5

Comando: `pyuic5 archivo.ui -o ui_archivo.py`  
Estado: todos completados.

- [x] `src/GUI/ui_DBComplextCountDialog.py`
- [x] `src/GUI/ui_alternateRepeatWidget.py`
- [x] `src/GUI/ui_alternateRepeats.py`
- [x] `src/GUI/ui_asciiDialog.py`
- [x] `src/GUI/ui_dbColours.py`
- [x] `src/GUI/ui_dbInfo.py`
- [x] `src/GUI/ui_dbLicense.py`
- [x] `src/GUI/ui_dbStartup.py`
- [x] `src/GUI/ui_defaultKitManager.py`
- [x] `src/GUI/ui_drumburp.py`
- [x] `src/GUI/ui_editKit.py`
- [x] `src/GUI/ui_insertMeasuresDialog.py`
- [x] `src/GUI/ui_measurePropertiesDialog.py`
- [x] `src/GUI/ui_newScoreDialog.py`
- [x] `src/GUI/ui_repeatCountDialog.py`
- [x] `src/GUI/ui_scorePropertiesDialog.py`
- [x] `src/GUI/ui_versionDownloader.py`
- [x] `src/Widgets/ui_measureTabs.py`

Cambios aplicados en cada archivo:

- [x] Imports cambiados a `from PyQt5 import QtCore, QtGui, QtWidgets`.
- [x] Clases de widgets `QtGui.QWidget`, `QtGui.QLabel`, etc. → `QtWidgets.*`.
- [x] `QtCore.QString.fromUtf8` eliminado.
- [x] `QApplication.UnicodeUTF8` y translate de 4 argumentos reemplazados.
- [x] `QtCore.QObject.connect(... SIGNAL(...))` → `.connect`.
- [x] `layout.setMargin(n)` → `layout.setContentsMargins(n, n, n, n)`.
- [x] Imports a `DrumBurp_rc` y `buttons_rc` reactivados con recursos PyQt5 reales.
- [x] Lineas huerfanas `QtGui.QPixmap = _CompatQPixmap` eliminadas de todos los archivos.

---

## Recursos QRC → regenerados con pyrcc5

Paquete requerido: `pyqt5-dev-tools`  
Instalacion: `sudo apt install pyqt5-dev-tools`

Comandos:

```bash
pyrcc5 src/GUI/DrumBurp.qrc    -o src/GUI/DrumBurp_rc.py
pyrcc5 src/buttons.qrc         -o src/buttons_rc.py
pyrcc5 src/Widgets/buttons.qrc -o src/Widgets/buttons_rc.py
```

- [x] `src/GUI/DrumBurp_rc.py` — regenerado con pyrcc5 (iconos y fuentes).
- [x] `src/buttons_rc.py` — regenerado con pyrcc5 (botones y cabezas de nota).
- [x] `src/Widgets/buttons_rc.py` — regenerado con pyrcc5.

Mapa de recursos por archivo:

| Archivo | Recursos usados | Import necesario |
|---------|----------------|-----------------|
| `ui_drumburp.py` | `:/Icons/`, `:/fonts/` | `import GUI.DrumBurp_rc` |
| `ui_dbInfo.py` | `:/Icons/` | `import GUI.DrumBurp_rc` |
| `ui_dbLicense.py` | `:/Icons/` | `import GUI.DrumBurp_rc` |
| `ui_alternateRepeatWidget.py` | `:/Icons/` | `import GUI.DrumBurp_rc` |
| `ui_editKit.py` | `:/Icons/`, `:/buttons/` | `import GUI.DrumBurp_rc` + `import buttons_rc` |
| `QNotationScene.py` | `:/heads/` | `import buttons_rc` |

Nota: `GUI/QtResourceCompat.py` fue el mecanismo temporal mientras los `*_rc.py`
eran stubs no-op. Ya no se usa — puede eliminarse en una limpieza futura.

---

## Capa temporal de compatibilidad src/PyQt4

- [x] Archivos `.py` de `src/PyQt4/` eliminados.
- [x] Directorio `src/PyQt4/` eliminado completamente.
- [x] Ningun archivo en `src/`, `build/`, `.github/` ni `pylintrc` importa PyQt4.

---

## Codigo de aplicacion — estado por archivo

### `src/DrumBurp.py`
- [x] `QApplication` desde `PyQt5.QtWidgets`. `app.exec()` modernizado.

### `src/GUI/DBMainwindow.py`
- [x] Widgets → `QtWidgets`; `QFont` → `QtGui`; `QPrinter` → `QtPrintSupport`.
- [x] `QVariant` eliminado en settings, combos y colores.
- [x] `QDesktopServices.storageLocation` → `QStandardPaths`.
- [x] `QFileDialog` adaptado (PyQt5 devuelve tupla).
- [x] Senales `currentIndexChanged` conectadas a sobrecarga `int`.
- [x] Decorador no-op `pyqtSignature` eliminado; `pyqtSlot` importado.
- [x] Los 35 `@pyqtSignature` → `@pyqtSlot` con firma correcta.
- [x] 3 slots `@staticmethod` convertidos a metodos de instancia.
- [x] `exec_()` → `exec()`.

### `src/GUI/QScore.py`
- [x] `QGraphicsScene`, `QGraphicsItem`, `QMessageBox`, `QUndoStack` → `QtWidgets`.
- [x] `exec_()` → `exec()`.

### `src/GUI/QStaff.py`
- [x] Hereda de `QGraphicsItem` (no `QGraphicsItemGroup`).
- [x] `setFiltersChildEvents(False)` en lugar de `setHandlesChildEvents(False)`.

### `src/GUI/QMeasure.py`
- [x] `setAcceptHoverEvents`; `horizontalAdvance`; division entera corregida.

### `src/GUI/QMeasureLine.py`
- [x] `QGraphicsItem` → `QtWidgets`; `QPen` en `QtGui`.

### `src/GUI/QLineLabel.py`
- [x] `setAcceptHoverEvents`.

### `src/GUI/QGraphicsListData.py`
- [x] `setAcceptHoverEvents`; `horizontalAdvance`.

### `src/GUI/QSection.py`
- [x] `QGraphicsTextItem` en `QtWidgets`; `QTextCursor` en `QtGui`.

### `src/GUI/QNotationScene.py`
- [x] `QGraphicsScene` → `QtWidgets`; `QPixmap` desde `PyQt5.QtGui`.
- [x] `import buttons_rc` reactivado con recurso PyQt5 real.

### `src/GUI/QEditKitDialog.py`
- [x] `QVariant`, `toInt`, `setTextColor` corregidos; `QStandardPaths`.
- [x] `exec_()` → `exec()`.

### `src/GUI/QComplexCountDialog.py`
- [x] `QVariant` eliminado; `pyqtSignature` → `pyqtSlot`.

### `src/GUI/QNewScoreDialog.py`
- [x] `QVariant` eliminado; settings protegidos contra valores PyQt4 antiguos.

### `src/GUI/QDefaultKitManager.py`
- [x] `QVariant` eliminado; `pyqtSignature` → `pyqtSlot`.
- [x] `exec_()` → `exec()`.

### `src/GUI/DBColourPicker.py`
- [x] Widgets → `QtWidgets`; `QColor`, `QPen` → `QtGui`.
- [x] `exec_()` → `exec()`.

### `src/GUI/DBMidi.py`
- [x] `QThread`, `QObject`, `QTimer`, `pyqtSignal` en `QtCore`.
- [x] Divisiones enteras en calculos de volumen y ticks MIDI corregidas (`/` → `//`).

### `src/GUI/LilypondExporter.py`
- [x] `QThread` → `QtCore`; escritura UTF-8 corregida para Python 3.

### `src/GUI/QLilypondPreview.py`
- [x] `QMessageBox`, `QGraphicsScene` → `QtWidgets`; `QTimeLine` en `QtCore`.

### `src/GUI/DBCommands.py`
- [x] `QUndoCommand` → `QtWidgets`.

### `src/GUI/DBFonts.py`
- [x] `QFontDatabase`, `QFont` → `QtGui`.

### `src/GUI/DBIcons.py`
- [x] `QIcon`, `QPixmap` → `QtGui`.

### `src/GUI/DBInfoDialog.py`
- [x] Seccion "Technologies" actualizada: Python 3 + PyQt5 (antes decia Python 2.7 + PyQt 4.8).
- [x] Seccion "PyQt4 → PyQt5 Port" agregada con credito al portador.
- [x] `exec_()` → `exec()`.

### Dialogos simples — todos completados
- [x] `src/GUI/DBLicense.py`
- [x] `src/GUI/DBStartupDialog.py`
- [x] `src/GUI/QAlternateDialog.py` — `exec_()` → `exec()`.
- [x] `src/GUI/QAlternateWidget.py`
- [x] `src/GUI/QEditMeasureDialog.py`
- [x] `src/GUI/QInsertMeasuresDialog.py`
- [x] `src/GUI/QMenuIgnoreCancelClick.py`
- [x] `src/GUI/QMetaDataDialog.py` — `exec_()` → `exec()`.
- [x] `src/GUI/QRepeatCountDialog.py`
- [x] `src/GUI/QVersionDownloader.py`

### Menus contextuales
- [x] `src/GUI/DBFSM.py`
- [x] `src/GUI/QMeasureContextMenu.py` — `exec_()` → `exec()`.

### Propiedades/visualizacion
- [x] `src/GUI/QDisplayProperties.py`

---

## Widgets custom

### `src/Widgets/ScoreView.py`
- [x] `QGraphicsView` → `QtWidgets`; `QTimeLine`, `QMutex`, `pyqtSlot`, `pyqtSignal` en `QtCore`.

### `src/Widgets/measureTabs.py`
- [x] `QWidget` → `QtWidgets`; `pyqtSignal` en `QtCore`.
- [x] `exec_()` → `exec()`.

### Plugins de Qt Designer
- [x] `src/Widgets/ScoreView_plugin.py` — migrado a `PyQt5.QtDesigner`.
- [x] `src/Widgets/measureTabs_plugin.py` — migrado a `PyQt5.QtDesigner`.

---

## Exportacion Lilypond — compatibilidad con LilyPond 2.24

- [x] Version en encabezado actualizada de `2.18.2` a `2.24.0`.
- [x] Articuladores de percusion en tabla `dbdrums`: `"open"`/`"stopped"` (strings
      con comillas, invalidos en LilyPond 2.22+) → `open`/`stopped` (simbolos Scheme).
- [x] Division entera en calculo de tuplets: `/` → `//`.
- [x] `note / 2` y `restNote / 2` en comparaciones de ticks → `//`.
- [x] `headCount / 26` en generacion de nombres de instrumento → `//`.
- [x] Exportacion a PDF verificada con LilyPond 2.24.1: genera PDF sin errores.

---

## Build, CI y configuracion

- [x] `build/build_linux.sh` — hidden imports cambiados a modulos PyQt5.
- [x] `build/install_pyqt.ps1` — ya no descarga instaladores PyQt4.
- [x] `.github/workflows/build.yml` — Linux y Windows CI actualizados a PyQt5/Python 3.
- [x] `pylintrc` — `extension-pkg-whitelist` cambiado de `PyQt4` a `PyQt5`.

---

## Suite de tests Python 3 — todos corregidos

Comando: `PYTHONPATH=src python3 -m unittest discover -s src/test`  
Resultado: **373 tests, todos OK**

- [x] `testNotePosition.py` — `__cmp__`/`cmp()` → metodos de comparacion Python 3.
- [x] `testMeasureCount.py` — division entera; `swing` opcional.
- [x] `testCounter.py` — `testIter` actualizado a 23 counters.
- [x] `testScore.py` — `range(...)` → `list(range(...))` en asserts.
- [x] `testLilypond.py` — `\times 2/3` → `\tuplet 3/2`; division entera.
- [x] `testdbfsv0.py` — logica bitmask `NO_BAR`; orden de flags BARLINE.
- [x] `testdbfsv1.py` — `Base64StringField` migrado al modulo `base64`.
- [x] `testDrum.py` — `checkShortcuts` usa `min()` para orden deterministico.
- [x] `testAsciiExport.py` — pasa tras corregir `counterMaker`.

---

## Verificacion final

Todos estos comandos deben ejecutarse sin errores ni advertencias:

```bash
# Sin resultados = sin imports PyQt4
grep -R "from PyQt4\|import PyQt4" -n src build .github pylintrc --exclude-dir=__pycache__

# Sin errores = todo compila
python3 -m py_compile $(find src -name '*.py' -not -path '*/__pycache__/*')

# 373 tests OK
PYTHONPATH=src python3 -m unittest discover -s src/test

# App arranca sin traceback
./run-drumburp.sh
```

---

## Pendientes menores (no bloquean el uso)

- [ ] Eliminar `src/GUI/QtResourceCompat.py` — ya no se usa, es codigo muerto.
- [ ] Validacion manual extendida: edicion de kits, exportacion MIDI, impresion
      en papel fisico, apertura de archivos `.brp` de versiones antiguas.

---

## Comandos de mantenimiento

Si se modifican archivos `.ui` o `.qrc`, regenerar con:

```bash
# Regenerar UI
pyuic5 src/GUI/archivo.ui -o src/GUI/ui_archivo.py
# Luego restaurar el import del _rc correspondiente segun la tabla de recursos.

# Regenerar recursos
pyrcc5 src/GUI/DrumBurp.qrc    -o src/GUI/DrumBurp_rc.py
pyrcc5 src/buttons.qrc         -o src/buttons_rc.py
pyrcc5 src/Widgets/buttons.qrc -o src/Widgets/buttons_rc.py
```

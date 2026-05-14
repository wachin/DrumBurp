# Informe de migracion PyQt4 -> PyQt5

**Proyecto:** DrumBurp — editor de notacion de bateria en Python/PyQt  
**Repositorio:** https://github.com/Whatang/DrumBurp  
**Port realizado por:** Washington Indacochea Delgado  
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
- PyQt5 5.15.x (`python3-pyqt5`)
- pyqt5-dev-tools (`pyuic5`, `pyrcc5`) — necesario para regenerar UI y recursos
- python3-pyqt5.qtmultimedia — para MIDI
- lilypond 2.24.x — para exportacion de partitura (opcional)

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

## Archivos generados por pyuic4 → regenerados con pyuic5

Comando usado: `pyuic5 archivo.ui -o ui_archivo.py`  
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

---

## Recursos QRC → regenerados con pyrcc5

Paquete requerido: `pyqt5-dev-tools` (incluye `pyrcc5`).  
Instalacion en Debian/Ubuntu: `sudo apt install pyqt5-dev-tools`

Comandos usados:

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
eran stubs no-op. Ya no se usa y puede eliminarse en una limpieza futura.

---

## Capa temporal de compatibilidad src/PyQt4

Esta carpeta contenia `__init__.py`, `QtCore.py` y `QtGui.py` que reexportaban
PyQt5 con nombres PyQt4, permitiendo que el codigo original corriera sin cambios.

- [x] Archivos `.py` de `src/PyQt4/` eliminados.
- [x] Directorio `src/PyQt4/` eliminado completamente (incluido `__pycache__`).
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

### Dialogos simples — todos completados
- [x] `src/GUI/DBInfoDialog.py` — `exec_()` → `exec()`.
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

## Build, CI y configuracion

- [x] `build/build_linux.sh` — hidden imports cambiados a modulos PyQt5.
- [x] `build/install_pyqt.ps1` — ya no descarga instaladores PyQt4.
- [x] `.github/workflows/build.yml` — Linux y Windows CI actualizados a PyQt5/Python 3.
- [x] `pylintrc` — `extension-pkg-whitelist` cambiado de `PyQt4` a `PyQt5`.

---

## Suite de tests Python 3 — todos corregidos

Comando: `PYTHONPATH=src python3 -m unittest discover -s src/test`  
Resultado: **373 tests, todos OK**

Bugs Python 2→3 corregidos en el codigo de la app:

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

Bugs corregidos en los tests:

- [x] `testCounter`: `testIter` actualizado de 11 a 23 counters (se agregaron
      Quintuplets, Septuplets y 64ths al registro por defecto).
- [x] `testScore`: comparaciones `range(...)` → `list(range(...))`.
- [x] `testLilypond`: actualizado de `\times 2/3` a `\tuplet 3/2`; division entera corregida.
- [x] `testdbfsv0`: orden de flags BARLINE actualizado para coincidir con dict `BAR_TYPES`.

---

## Exportacion Lilypond — compatibilidad con LilyPond 2.24

- [x] Version en encabezado actualizada de `2.18.2` a `2.24.0`
      (`src/Notation/lilypond.py`).
- [x] Articuladores de percusion en tabla `dbdrums` corregidos: `"open"` y
      `"stopped"` (strings con comillas, invalidos en LilyPond 2.22+) →
      `open` y `stopped` (simbolos Scheme sin comillas)
      (`src/Notation/lilypond.py`, clase `LilyKit._EFFECTS`).
- [x] Division entera en calculo de tuplets: `/` → `//` para evitar `3.0/2`
      (`src/Notation/lilypond.py`).
- [x] Exportacion a PDF verificada con LilyPond 2.24.1: genera PDF sin errores.

---

## Pendientes

- [ ] Eliminar `src/GUI/QtResourceCompat.py` — ya no se usa (todos los `*_rc.py`
      son recursos PyQt5 reales). Conservarlo no causa errores pero es codigo muerto.
- [ ] Validacion manual amplia de flujos de usuario: edicion de notas, reproduccion
      MIDI, exportacion Lilypond desde la UI, impresion.

---

## Comandos de verificacion

```bash
# Sin resultados = sin imports PyQt4
grep -R "from PyQt4\|import PyQt4" -n src build .github pylintrc --exclude-dir=__pycache__

# Sin errores = todo compila
python3 -m py_compile $(find src -name '*.py' -not -path '*/__pycache__/*')

# 373 tests OK
PYTHONPATH=src python3 -m unittest discover -s src/test

# App arranca sin traceback
./run-drumburp.sh

# Regenerar recursos si se modifican los .qrc
pyrcc5 src/GUI/DrumBurp.qrc    -o src/GUI/DrumBurp_rc.py
pyrcc5 src/buttons.qrc         -o src/buttons_rc.py
pyrcc5 src/Widgets/buttons.qrc -o src/Widgets/buttons_rc.py

# Regenerar UI si se modifican los .ui
pyuic5 src/GUI/archivo.ui -o src/GUI/ui_archivo.py
# Luego restaurar el import del _rc correspondiente segun la tabla de recursos.
```

# Informe de migracion PyQt4 -> PyQt5

Port PyQt4 to PyQt5
Por: Washington Indacochea Delgado
Iniciado: 2026-03-28

Este informe parte de `informe_pyqt4.txt`. El proyecto ya corre en Debian 12
porque existe `src/PyQt4`, una capa de compatibilidad que reexporta PyQt5 con
nombres de PyQt4. Eso es util para avanzar, pero no es una migracion completa:
el objetivo final debe ser eliminar los imports `PyQt4` del codigo de la app.

## Estrategia recomendada

- [x] 1. Mantener temporalmente `src/PyQt4` mientras se corrigen errores funcionales.
- [x] 2. Migrar directo a `PyQt5` (sin capa intermedia `GUI/QtCompat.py`).
- [x] 3. Regenerar los archivos `ui_*.py` con `pyuic5` o convertirlos mecanicamente.
- [ ] 4. Regenerar los archivos `*_rc.py` con `pyrcc5` (actualmente son stubs no-op).
- [x] 5. Migrar codigo manual por grupos: arranque, dialogos simples, score/graphics,
         preferencias, MIDI/exportacion.
- [x] 6. Borrar archivos `.py` de `src/PyQt4`. Queda pendiente borrar el directorio
         vacio `src/PyQt4/` y su `__pycache__`.
- [ ] 7. Verificar que `grep -R PyQt4` solo encuentre documentacion historica
         (actualmente pasa, pero el directorio vacio aun existe).

## Cambios generales PyQt4 -> PyQt5

- [x] `PyQt4.QtGui` dividido en `PyQt5.QtWidgets`, `PyQt5.QtGui` y `PyQt5.QtPrintSupport`.
- [x] `QApplication`, `QDialog`, `QWidget`, layouts, menus, acciones, message boxes,
      `QGraphicsView`, `QGraphicsScene`, `QGraphicsItem`, `QUndoStack`,
      `QUndoCommand` pasados a `QtWidgets`.
- [x] `QFont`, `QFontMetrics`, `QPixmap`, `QIcon`, `QColor`, `QPen`, `QTransform`,
      `QTextCursor` pasados a `QtGui`.
- [x] `QPrinter` pasado a `QtPrintSupport`.
- [x] `QVariant` eliminado: se usan valores Python directamente.
- [x] `.toInt()`, `.toBool()`, `.toString()`, `.toStringList()`, `.toByteArray()`
      reemplazados por conversiones Python o `QSettings.value(..., type=...)`.
- [x] `QDesktopServices.storageLocation()` reemplazado por `QStandardPaths`.
- [x] `QtCore.SIGNAL`, `QtCore.SLOT` y `QtCore.QObject.connect(...)` reemplazados
      por senales nuevas: `obj.signal.connect(slot)`.
- [x] `QtCore.pyqtSignature` eliminado y reemplazado por `@pyqtSlot(...)`.
- [x] `QApplication.UnicodeUTF8` y `QtCore.QString.fromUtf8` eliminados.
- [x] `QLayout.setMargin()` reemplazado por `setContentsMargins(...)`.
- [x] `QGraphicsItem.setAcceptsHoverEvents()` reemplazado por `setAcceptHoverEvents()`.
- [x] `QGraphicsItemGroup` reemplazado por `QGraphicsItem` con `setParentItem` en `QStaff`.
- [x] `QFontMetrics.width(text)` reemplazado por `horizontalAdvance(text)`.
- [ ] `exec_()` todavia se usa en varios lugares; se puede modernizar a `exec()` opcionalmente.

## Archivos generados por pyuic4

Estado actual: completado.

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

Port realizado:

- [x] Imports generados cambiados a `from PyQt5 import QtCore, QtGui, QtWidgets`.
- [x] Clases de widgets `QtGui.QWidget`, `QtGui.QLabel`, etc. reemplazadas por `QtWidgets.*`.
- [x] `QtCore.QString.fromUtf8` eliminado.
- [x] `QApplication.UnicodeUTF8` y llamadas de translate de 4 argumentos reemplazadas.
- [x] `QtCore.QObject.connect(... SIGNAL(...))` reemplazado por `.connect`.
- [x] `layout.setMargin(n)` reemplazado por `layout.setContentsMargins(n, n, n, n)`.
- [x] Imports a `DrumBurp_rc` y `buttons_rc` quitados de las UI para evitar segfaults.

Nota: al regenerar de nuevo con `pyuic5` habra que volver a aplicar el ajuste
de `QtResourceCompat` o automatizarlo.

## Recursos generados por pyrcc4

- [ ] `src/buttons_rc.py` — actualmente es stub no-op; regenerar con `pyrcc5`.
- [ ] `src/Widgets/buttons_rc.py` — actualmente es stub no-op; regenerar con `pyrcc5`.
- [ ] `src/GUI/DrumBurp_rc.py` — actualmente es stub no-op; regenerar con `pyrcc5`.

Nota: los stubs no-op permiten que el codigo importe sin crash. No intentar
registrarlos con PyQt5 sin regenerarlos: produjo pixmaps nulos y segfaults.
Los pixmaps `:/...` se resuelven ahora mediante `GUI/QtResourceCompat.py`.

## Capa temporal de compatibilidad

- [x] Archivos `.py` de `src/PyQt4/` eliminados (`__init__.py`, `QtCore.py`, `QtGui.py`).
- [x] No hay imports `from PyQt4` / `import PyQt4` en `src`, `build`, `.github` ni `pylintrc`.
- [ ] Borrar el directorio vacio `src/PyQt4/` y su `__pycache__/`.

## Codigo de aplicacion

### `src/DrumBurp.py`
- [x] Completado. `QApplication` importado desde `PyQt5.QtWidgets`.

### `src/GUI/DBMainwindow.py`
- [x] Completado. Widgets a `QtWidgets`; `QFont` a `QtGui`; `QPrinter` a `QtPrintSupport`.
- [x] `QVariant` eliminado en settings, combos y guardado de colores.
- [x] `QDesktopServices.storageLocation` reemplazado por `QStandardPaths`.
- [x] `QFileDialog` adaptado (PyQt5 devuelve tupla).
- [x] Senales `currentIndexChanged` conectadas a sobrecarga `int`.
- [x] Decorador no-op `pyqtSignature` eliminado; `pyqtSlot` importado de `PyQt5.QtCore`.
- [x] Los 35 `@pyqtSignature` reemplazados por `@pyqtSlot` con firma correcta.
- [x] Los 3 slots `@staticmethod` convertidos a metodos de instancia normales.

### `src/GUI/QScore.py`
- [x] Completado. `QGraphicsScene`, `QGraphicsItem`, `QMessageBox`, `QUndoStack` a `QtWidgets`.

### `src/GUI/QStaff.py`
- [x] Completado. Hereda de `QGraphicsItem`; `setFiltersChildEvents(False)`.

### `src/GUI/QMeasure.py`
- [x] Completado. `setAcceptHoverEvents`; `horizontalAdvance`; division entera corregida.

### `src/GUI/QMeasureLine.py`
- [x] Completado. `QGraphicsItem` a `QtWidgets`; `QPen` en `QtGui`.

### `src/GUI/QLineLabel.py`
- [x] Completado. `setAcceptHoverEvents`.

### `src/GUI/QGraphicsListData.py`
- [x] Completado. `setAcceptHoverEvents`; `horizontalAdvance`.

### `src/GUI/QSection.py`
- [x] Completado. `QGraphicsTextItem` en `QtWidgets`; `QTextCursor` en `QtGui`.

### `src/GUI/QNotationScene.py`
- [x] Completado. `QGraphicsScene` a `QtWidgets`; usa `QtResourceCompat` para pixmaps.

### `src/GUI/QEditKitDialog.py`
- [x] Completado. `QVariant`, `toInt`, `setTextColor` corregidos; `QStandardPaths`.

### `src/GUI/QComplexCountDialog.py`
- [x] Completado. `QVariant` eliminado; `pyqtSignature` reemplazado por `pyqtSlot`.

### `src/GUI/QNewScoreDialog.py`
- [x] Completado. `QVariant` eliminado; settings protegidos contra valores antiguos.

### `src/GUI/QDefaultKitManager.py`
- [x] Completado. `QVariant` eliminado; `pyqtSignature` reemplazado por `pyqtSlot`.

### `src/GUI/DBColourPicker.py`
- [x] Completado. Widgets a `QtWidgets`; `QColor`, `QPen` a `QtGui`.

### `src/GUI/DBMidi.py`
- [x] Completado. `QThread`, `QObject`, `QTimer`, `pyqtSignal` en `QtCore`.

### `src/GUI/LilypondExporter.py`
- [x] Completado. `QThread` a `QtCore`; escritura UTF-8 corregida para Python 3.

### `src/GUI/QLilypondPreview.py`
- [x] Completado. `QMessageBox`, `QGraphicsScene` a `QtWidgets`; `QTimeLine` en `QtCore`.

### `src/GUI/DBCommands.py`
- [x] Completado. `QUndoCommand` a `QtWidgets`.

### `src/GUI/DBFonts.py`
- [x] Completado. `QFontDatabase`, `QFont` a `QtGui`.

### `src/GUI/DBIcons.py`
- [x] Completado. `QIcon`, `QPixmap` a `QtGui`.

### Dialogos simples
- [x] `src/GUI/DBInfoDialog.py`
- [x] `src/GUI/DBLicense.py`
- [x] `src/GUI/DBStartupDialog.py`
- [x] `src/GUI/QAlternateDialog.py`
- [x] `src/GUI/QAlternateWidget.py`
- [x] `src/GUI/QEditMeasureDialog.py`
- [x] `src/GUI/QInsertMeasuresDialog.py`
- [x] `src/GUI/QMenuIgnoreCancelClick.py`
- [x] `src/GUI/QMetaDataDialog.py`
- [x] `src/GUI/QRepeatCountDialog.py`
- [x] `src/GUI/QVersionDownloader.py`

### Menus contextuales
- [x] `src/GUI/DBFSM.py` — completado.
- [x] `src/GUI/QMeasureContextMenu.py` — completado.

### Propiedades/visualizacion
- [x] `src/GUI/QDisplayProperties.py` — completado.

## Widgets custom

### `src/Widgets/ScoreView.py`
- [x] Completado. `QGraphicsView` a `QtWidgets`; `QTimeLine`, `QMutex`, `pyqtSlot`, `pyqtSignal` en `QtCore`.

### `src/Widgets/measureTabs.py`
- [x] Completado. `QWidget` a `QtWidgets`; `pyqtSignal` en `QtCore`.

### Plugins de Qt Designer
- [x] `src/Widgets/ScoreView_plugin.py` — migrado a `PyQt5.QtDesigner`.
- [x] `src/Widgets/measureTabs_plugin.py` — migrado a `PyQt5.QtDesigner`.

### Recursos de Widgets
- [ ] `src/Widgets/buttons_rc.py` — stub no-op; regenerar con `pyrcc5`.

## Build, CI y configuracion

- [x] `build/build_linux.sh` — hidden imports cambiados a modulos PyQt5.
- [x] `build/install_pyqt.ps1` — ya no descarga instaladores PyQt4.
- [x] `.github/workflows/build.yml` — Linux y Windows CI actualizados a PyQt5/Python 3.
- [x] `pylintrc` — `extension-pkg-whitelist` cambiado de `PyQt4` a `PyQt5`.

## Suite de tests Python 3

- [x] `testNotePosition.py` — `NotePosition.__cmp__`/`cmp()` reemplazado por
      `__eq__`/`__lt__`/`__le__`/`__gt__`/`__ge__`/`__hash__`.
- [x] `testMeasureCount.py` — division `/` cambiada a `//` en `counterMaker`;
      argumento `swing` hecho opcional con default `0`.
- [x] `testCounter.py` — `testIter` actualizado de 11 a 23 counters.
- [x] `testScore.py` — comparaciones `range(...)` reemplazadas por `list(range(...))`.
- [x] `testLilypond.py` — actualizado a `\tuplet 3/2`; division entera corregida.
- [x] `testdbfsv0.py` — logica de bitmask `NO_BAR` corregida; orden de flags actualizado.
- [x] `testdbfsv1.py` — `Base64StringField` migrado al modulo `base64` de Python 3.
- [x] `testDrum.py` — `checkShortcuts` usa `min()` para orden deterministico.
- [x] `testAsciiExport.py` — pasa tras corregir `counterMaker`.
- [x] Total: 373 tests, todos OK.

## Pendientes

- [ ] Borrar directorio vacio `src/PyQt4/` (solo contiene `__pycache__`).
- [ ] Regenerar `src/buttons_rc.py`, `src/Widgets/buttons_rc.py` y
      `src/GUI/DrumBurp_rc.py` con `pyrcc5` (actualmente son stubs no-op).
- [ ] Modernizar `exec_()` a `exec()` en los dialogos (opcional, baja prioridad).
- [ ] Validacion manual amplia de flujos de usuario: edicion, MIDI, impresion.
- [ ] Compatibilidad con LilyPond 2.22+ (problema independiente de PyQt):
      el signo de percusion `"open"` en la tabla `dbdrums` ya no es valido
      en LilyPond 2.24; requiere investigar la sintaxis correcta.

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
```

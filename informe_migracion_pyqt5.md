# Informe de migracion PyQt4 -> PyQt5

Este informe parte de `informe_pyqt4.txt`. El proyecto ya corre en Debian 12
porque existe `src/PyQt4`, una capa de compatibilidad que reexporta PyQt5 con
nombres de PyQt4. Eso es util para avanzar, pero no es una migracion completa:
el objetivo final debe ser eliminar los imports `PyQt4` del codigo de la app.

## Estrategia recomendada

1. Mantener temporalmente `src/PyQt4` mientras se corrigen errores funcionales.
2. Crear una capa propia `GUI/QtCompat.py` o migrar directo a `PyQt5`.
3. Regenerar los archivos `ui_*.py` con `pyuic5` o convertirlos mecanicamente.
4. Regenerar los archivos `*_rc.py` con `pyrcc5`.
5. Migrar codigo manual por grupos: arranque, dialogos simples, score/graphics,
   preferencias, MIDI/exportacion.
6. Al final, borrar `src/PyQt4` y verificar que `grep -R PyQt4` solo encuentre
   documentacion historica.

## Cambios generales PyQt4 -> PyQt5

- `PyQt4.QtGui` se divide en `PyQt5.QtWidgets`, `PyQt5.QtGui` y
  `PyQt5.QtPrintSupport`.
- `QApplication`, `QDialog`, `QWidget`, layouts, menus, acciones, message boxes,
  `QGraphicsView`, `QGraphicsScene`, `QGraphicsItem`, `QUndoStack`,
  `QUndoCommand` pasan a `QtWidgets`.
- `QFont`, `QFontMetrics`, `QPixmap`, `QIcon`, `QColor`, `QPen`, `QTransform`,
  `QTextCursor` pasan a `QtGui`.
- `QPrinter` pasa a `QtPrintSupport`.
- `QVariant` desaparece: usar valores Python (`int`, `bool`, `str`, `list`,
  `QByteArray`) directamente.
- `.toInt()`, `.toBool()`, `.toString()`, `.toStringList()`, `.toByteArray()`
  deben reemplazarse por conversiones Python o `QSettings.value(..., type=...)`.
- `QDesktopServices.storageLocation()` desaparece: usar
  `QStandardPaths.writableLocation()` o `standardLocations()`.
- `QtCore.SIGNAL`, `QtCore.SLOT` y `QtCore.QObject.connect(...)` deben cambiarse
  por senales nuevas: `obj.signal.connect(slot)`.
- `QtCore.pyqtSignature` no es necesario. Se puede quitar o reemplazar por
  `@pyqtSlot(...)` si se quiere conservar decoracion explicita.
- `QApplication.UnicodeUTF8` y `QtCore.QString.fromUtf8` desaparecen. Los textos
  son `str` nativos en Python 3.
- `QLayout.setMargin()` debe cambiarse por `setContentsMargins(...)`.
- `QGraphicsItem.setAcceptsHoverEvents()` debe cambiarse por
  `setAcceptHoverEvents()`.
- `QGraphicsItemGroup` no debe usarse para agrupar compases interactivos: en
  Qt5 puede capturar eventos de los hijos. Ya se corrigio `QStaff`.
- `QFontMetrics.width(text)` esta obsoleto en Qt5: preferir
  `horizontalAdvance(text)`.
- `exec_()` todavia existe en PyQt5, pero si se quiere modernizar puede pasarse
  a `exec()`.

## Archivos generados por pyuic4

Estado actual: completado. Estos archivos ya fueron regenerados con
`PyQt5.uic` y ahora importan `PyQt5.QtCore`, `PyQt5.QtGui` y
`PyQt5.QtWidgets`.

Nota importante: se quitaron los imports finales a `DrumBurp_rc` y
`buttons_rc` en las UI regeneradas, porque esos recursos venian de `pyrcc4` y
provocaban segfaults al registrarse en una aplicacion PyQt5. Los pixmaps `:/...`
se resuelven ahora mediante `GUI/QtResourceCompat.py`, que carga los archivos
reales desde `src/GUI/Icons`.

Archivos:

- `src/GUI/ui_DBComplextCountDialog.py`
- `src/GUI/ui_alternateRepeatWidget.py`
- `src/GUI/ui_alternateRepeats.py`
- `src/GUI/ui_asciiDialog.py`
- `src/GUI/ui_dbColours.py`
- `src/GUI/ui_dbInfo.py`
- `src/GUI/ui_dbLicense.py`
- `src/GUI/ui_dbStartup.py`
- `src/GUI/ui_defaultKitManager.py`
- `src/GUI/ui_drumburp.py`
- `src/GUI/ui_editKit.py`
- `src/GUI/ui_insertMeasuresDialog.py`
- `src/GUI/ui_measurePropertiesDialog.py`
- `src/GUI/ui_newScoreDialog.py`
- `src/GUI/ui_repeatCountDialog.py`
- `src/GUI/ui_scorePropertiesDialog.py`
- `src/GUI/ui_versionDownloader.py`
- `src/Widgets/ui_measureTabs.py`

Port realizado:

- Cambiados imports generados a `from PyQt5 import QtCore, QtGui, QtWidgets`.
- Reemplazadas clases de widgets `QtGui.QWidget`, `QtGui.QLabel`,
  `QtGui.QDialogButtonBox`, etc. por `QtWidgets.*`.
- Conservadas clases graficas puras como `QtGui.QIcon`, `QtGui.QPixmap`,
  `QtGui.QFont`.
- Eliminado `QtCore.QString.fromUtf8`.
- Reemplazados `QApplication.UnicodeUTF8` y llamadas de translate de 4 argumentos
  por `QtCore.QCoreApplication.translate(context, text, disambig)`.
- Reemplazado `QtCore.QObject.connect(... SIGNAL(...))` por `.connect`.
- Reemplazado `layout.setMargin(n)` por `layout.setContentsMargins(n, n, n, n)`.

Riesgo restante: bajo-medio. Al regenerar de nuevo con `pyuic5` habra que
volver a aplicar el ajuste de `QtResourceCompat` o automatizarlo.

## Recursos generados por pyrcc4

Archivos:

- `src/buttons_rc.py`
- `src/Widgets/buttons_rc.py`
- `src/GUI/DrumBurp_rc.py`

Port necesario:

- Regenerar desde `.qrc` con `pyrcc5` cuando la herramienta este disponible.
- Mientras no exista `pyrcc5`, no importarlos desde las UI PyQt5. Ya se hizo.
- `src/buttons_rc.py`, `src/Widgets/buttons_rc.py` y `src/GUI/DrumBurp_rc.py`
  fueron reemplazados por stubs no-op para que sigan siendo importables sin
  registrar datos `pyrcc4`.
- No intentar registrarlos directamente con PyQt5 sin regenerarlos: produjo
  pixmaps nulos y segfaults.

Riesgo: medio. Si se vuelven a importar desde UI PyQt5 sin regenerar con
`pyrcc5`, puede volver el segfault.

## Capa temporal de compatibilidad

Archivos:

- `src/PyQt4/__init__.py`
- `src/PyQt4/QtCore.py`
- `src/PyQt4/QtGui.py`

Estado:

- Estado actual: eliminada del arbol fuente.
- Ya no hay imports `from PyQt4` / `import PyQt4` en `src`, `build`, `.github`
  ni `pylintrc` (excluyendo caches generadas).

Riesgo: bajo mientras no se reintroduzcan recursos `pyrcc4` ni imports PyQt4.

## Codigo de aplicacion

### `src/DrumBurp.py`

- Estado actual: completado.
- `QApplication` ya se importa desde `PyQt5.QtWidgets`.
- Influye en arranque completo de la app.
- Riesgo bajo.

### `src/GUI/DBMainwindow.py`

- Estado actual: completado.
- Widgets migrados a `QtWidgets`; `QFont` a `QtGui`; `QPrinter`,
  `QPrinterInfo` y `QPrintPreviewDialog` a `QtPrintSupport`.
- `QVariant` eliminado en settings, combos y guardado de colores.
- Lecturas `settings.value(...).toString()/toBool()/toStringList()` reemplazadas
  por valores Python con `type=...`.
- `QDesktopServices.storageLocation` reemplazado por
  `QStandardPaths.writableLocation`.
- `QFileDialog.getOpenFileName/getSaveFileName` adaptado con helper porque
  PyQt5 devuelve tupla.
- Lectura de `QSettings` endurecida para configuraciones antiguas: algunos
  valores guardados como QVariant/PyQt_PyObject no se pueden convertir con
  `type=str` en PyQt5 y ahora caen a lectura sin tipo o valor por defecto.
- Señales sobrecargadas `currentIndexChanged` conectadas explicitamente a la
  sobrecarga `int`; el slot de `paperBox` tambien acepta texto como fallback.
- Export ASCII corregido para escribir texto UTF-8, no bytes en archivo texto.
- `pyqtSignature` queda como decorador no-op local para evitar tocar todos los
  slots autoconectados de una vez; se puede limpiar mas adelante.
- Influye en casi todos los dialogos, archivos recientes, colores, Lilypond,
  MIDI, guardado/exportacion.
- Riesgo alto.

### `src/GUI/QScore.py`

- Estado actual: completado.
- `QGraphicsScene`, `QGraphicsItem`, `QMessageBox` y `QUndoStack` migrados a
  `QtWidgets`; `QTransform`, `QPainter` y `QFontMetrics` quedan en `QtGui`.
- Menus/dialogos abiertos desde la escena compilan y el arranque offscreen no
  muestra tracebacks.
- Ya depende de `QStaff`, `QMeasure`, `QMeasureLine`, `QKitData`, etc.
- Riesgo alto por interacciones graficas.

### `src/GUI/QStaff.py`

- Estado actual: completado.
- Ya no debe heredar de `QGraphicsItemGroup`; en Qt5 captura eventos de hijos.
- Hereda de `QtWidgets.QGraphicsItem`, hijos con `setParentItem`.
- `setHandlesChildEvents(False)` reemplazado por `setFiltersChildEvents(False)`.
- Riesgo alto si se revierte.

### `src/GUI/QMeasure.py`

- Estado actual: completado.
- `QGraphicsItem` migrado a `QtWidgets`; `QFontMetrics` a `QtGui`; geometria y
  eventos siguen en `QtCore`.
- `setAcceptsHoverEvents` reemplazado por `setAcceptHoverEvents`.
- `QFontMetrics.width` reemplazado por `horizontalAdvance` en textos calculados.
- Corregida division Python 2 en compases simile (`numLines // 2`).
- Influye en clic para agregar notas, seleccion, menus y doble clic.
- Riesgo alto.

### `src/GUI/QMeasureLine.py`

- Estado actual: completado.
- `QGraphicsItem` migrado a `QtWidgets`; `QPen` queda en `QtGui`; geometria y
  eventos en `QtCore`.
- Influye en menus de barras de compas.
- Riesgo medio.

### `src/GUI/QLineLabel.py`

- Estado actual: completado.
- `QGraphicsItem` migrado a `QtWidgets`.
- `setAcceptsHoverEvents` reemplazado por `setAcceptHoverEvents`.
- Influye en etiquetas/abreviaturas de bateria y resaltado de linea.
- Riesgo medio.

### `src/GUI/QGraphicsListData.py`

- Estado actual: completado.
- `QGraphicsItem` migrado a `QtWidgets`; `QFontMetrics` y `QPen` a `QtGui`.
- `setAcceptsHoverEvents` reemplazado por `setAcceptHoverEvents`.
- `QFontMetrics.width` reemplazado por `horizontalAdvance`.
- Riesgo medio.

### `src/GUI/QSection.py`

- Estado actual: completado.
- `QGraphicsTextItem` queda en `QtWidgets`; `QTextCursor` queda en `QtGui`.
- Riesgo medio.

### `src/GUI/QNotationScene.py`

- Estado actual: completado.
- `QGraphicsScene` pasa a `QtWidgets`; `QPixmap` queda en `QtGui`.
- Usa `GUI.QtResourceCompat.QPixmap` para resolver pixmaps `:/heads/...` sin
  cargar recursos `pyrcc4`.
- Ya se corrigio division entera para Python 3.
- Riesgo medio.

### `src/GUI/QEditKitDialog.py`

- Estado actual: completado en codigo Python.
- Dialogo y widgets migrados a `QtWidgets`; `QColor` a `QtGui`.
- Ya se corrigieron `QVariant`, `findData`, `toInt`, `setTextColor`.
- `QDesktopServices.storageLocation` reemplazado por `QStandardPaths`.
- Influye en kits, heads MIDI y default kits.
- Riesgo alto.

### `src/GUI/QComplexCountDialog.py`

- Estado actual: completado.
- `QVariant` reemplazado en `QListWidgetItem.setData`.
- `item.data(...).toInt()[0]` reemplazado por `int(item.data(...))`.
- `pyqtSignature` reemplazado por `pyqtSlot`.
- Riesgo medio.

### `src/GUI/QNewScoreDialog.py`

- Estado actual: completado.
- `QVariant(False/True)` reemplazado por bool.
- `.toBool()` reemplazado por `bool(...)`.
- `settings.value(...).toString()` reemplazado por `settings.value(..., "", type=str)`.
- Lectura de kits personalizados protegida contra settings antiguos que PyQt5
  no puede convertir directamente a `str`.
- Riesgo medio.

### `src/GUI/QDefaultKitManager.py`

- Estado actual: completado.
- `QtCore.QVariant` reemplazado por bool.
- `.toBool()` reemplazado por `bool(...)`.
- `settings.value(...).toString()` reemplazado por str.
- Lectura de kits personalizados protegida contra settings antiguos que PyQt5
  no puede convertir directamente a `str`.
- `pyqtSignature` reemplazado por `pyqtSlot`.
- Riesgo medio.

### `src/GUI/DBColourPicker.py`

- Estado actual: completado.
- Widgets a `QtWidgets`; `QColor`, `QPen` a `QtGui`.
- `QColor.toString()` sigue existiendo.
- `QColorDialog` esta en `QtWidgets`.
- Riesgo medio.

### `src/GUI/DBMidi.py`

- Estado actual: completado.
- `QThread`, `QObject`, `QTimer`, `pyqtSignal` pasan a `QtCore`.
- Revisar senales y thread lifetime.
- Riesgo alto por reproduccion MIDI.

### `src/GUI/LilypondExporter.py`

- Estado actual: completado.
- `QThread` pasa a `QtCore`.
- Escritura del `.ly` corregida para Python 3: archivo texto con
  `encoding='utf-8'` y escritura de `str`, no `bytes`.
- Riesgo medio.

### `src/GUI/QLilypondPreview.py`

- Estado actual: completado.
- `QMessageBox` y `QGraphicsScene` pasan a `QtWidgets`; `QPixmap` queda en
  `QtGui`; `QTimeLine` y `pyqtSignal` quedan en `QtCore`.
- Riesgo medio.

### `src/GUI/DBCommands.py`

- Estado actual: completado.
- `QUndoCommand` pasa a `QtWidgets`.
- Riesgo medio-alto porque afecta undo/redo.

### `src/GUI/DBFonts.py`

- Estado actual: completado.
- `QFontDatabase`, `QFont` pasan a `QtGui`.
- Riesgo bajo.

### `src/GUI/DBIcons.py`

- Estado actual: completado.
- `QIcon`, `QPixmap` pasan a `QtGui`.
- Revisar rutas de recursos.
- Riesgo bajo.

### Dialogos simples

Archivos:

- `src/GUI/DBInfoDialog.py`
- `src/GUI/DBLicense.py`
- `src/GUI/DBStartupDialog.py`
- `src/GUI/QAlternateDialog.py`
- `src/GUI/QAlternateWidget.py`
- `src/GUI/QEditMeasureDialog.py`
- `src/GUI/QInsertMeasuresDialog.py`
- `src/GUI/QMenuIgnoreCancelClick.py`
- `src/GUI/QMetaDataDialog.py`
- `src/GUI/QRepeatCountDialog.py`
- `src/GUI/QVersionDownloader.py`

Estado actual: completado para estos dialogos.

Port realizado:

- `QDialog`, `QWidget`, `QMenu` pasan a `QtWidgets`.
- Quitar `pyqtSignature` donde aparezca.
- `exec_()` puede mantenerse temporalmente.
- Riesgo bajo-medio.

### Menus contextuales

Archivos:

- `src/GUI/DBFSM.py`
- `src/GUI/QMeasureContextMenu.py`

Port necesario:

- `QTimer` sigue en `QtCore`.
- Menus y acciones deben venir de `QtWidgets`.
- Revisar `event.screenPos()`; en PyQt5 todavia funciona en `QGraphicsSceneMouseEvent`.
- Riesgo medio por flujo de estados y menus.

### Propiedades/visualizacion

Archivos:

- `src/GUI/QDisplayProperties.py`

Port necesario:

- `QObject`, `pyqtSignal` quedan en `QtCore`.
- `QFontMetrics`, `QFont` pasan a `QtGui`.
- Riesgo medio porque afecta layout.

## Widgets custom

### `src/Widgets/ScoreView.py`

- Estado actual: completado.
- `QGraphicsView` pasa a `QtWidgets`.
- `QTimeLine`, `QMutex`, `pyqtSlot`, `pyqtSignal` quedan en `QtCore`.
- Influye en scroll, zoom y navegacion visual.
- Riesgo medio.

### `src/Widgets/measureTabs.py`

- Estado actual: completado.
- `QWidget` pasa a `QtWidgets`; `pyqtSignal` queda en `QtCore`.
- Riesgo bajo-medio.

### Plugins de Qt Designer

Archivos:

- `src/Widgets/ScoreView_plugin.py`
- `src/Widgets/measureTabs_plugin.py`

Port necesario:

- `QPyDesignerCustomWidgetPlugin` en PyQt5 esta en `PyQt5.QtDesigner`.
- Solo necesarios si se usa Qt Designer; no son criticos para ejecutar DrumBurp.
- Riesgo bajo.

### `src/Widgets/buttons_rc.py`

- Regenerar con `pyrcc5`.
- Riesgo bajo-medio.

## Build, CI y configuracion

### `build/build_linux.sh`

- Estado actual: completado.
- Hidden imports cambiados de `PyQt4.QtGui` a los modulos PyQt5 usados:
  `PyQt5.QtWidgets`, `PyQt5.QtGui`, `PyQt5.QtCore`, `PyQt5.QtPrintSupport`.
- Revisar PyInstaller hooks para PyQt5.
- Riesgo medio.

### `build/install_pyqt.ps1`

- Estado actual: completado.
- Ya no descarga instaladores PyQt4; queda como placeholder indicando que PyQt5
  se instala via `build/requirements-windows.txt`.
- Riesgo bajo para Debian 12.

### `.github/workflows/build.yml`

- Estado actual: completado parcialmente.
- Linux CI actualizado para importar PyQt5 e instalar requirements con Python 3.
- Windows CI actualizado a `actions/setup-python@v5` con Python 3.11 y sin cache
  ni instalador PyQt4.
- Riesgo medio.

### `pylintrc`

- Estado actual: completado.
- `extension-pkg-whitelist=PyQt4` cambiado a `PyQt5`.
- Riesgo bajo.

## Orden de implementacion propuesto

1. Completado: corregir fallos runtime iniciales.
2. Completado temporal: recursos `*_rc.py` reemplazados por stubs no-op; queda
   pendiente regenerarlos con `pyrcc5` solo si se quiere volver a usar QRC.
3. Completado: regenerar `ui_*.py` con `PyQt5.uic`.
4. Completado: migrar dialogos simples.
5. Completado: migrar `QNewScoreDialog`, `QDefaultKitManager`,
   `QComplexCountDialog`.
6. Completado: migrar `QEditKitDialog`.
7. Completado: migrar score/graphics:
   `QScore`, `QStaff`, `QMeasure`, `QMeasureLine`, `QLineLabel`,
   `QGraphicsListData`, `QSection`, `QNotationScene`.
8. Completado: migrar soporte de aplicacion: `DBMainwindow`, `DBCommands`,
   `DBFonts`, `DBIcons`, `DBColourPicker`, `QDisplayProperties`.
9. Completado: migrar MIDI/exportacion: `DBMidi`, `LilypondExporter`,
   `QLilypondPreview`, `DBFSM`, `QMeasureContextMenu`.
10. Completado: plugins de Designer, build Linux, requirements, workflow CI y
    `pylintrc` migrados a PyQt5/Python 3.
11. Completado: eliminada la capa temporal `src/PyQt4`.
12. Completado: corregidos todos los fallos de la suite de tests Python 3
    (`testScore.py`, `testDrum.py`, `testNotePosition.py`, `testMeasureCount.py`,
    `testCounter.py`, `testdbfsv0.py`, `testdbfsv1.py`, `testLilypond.py`,
    `testAsciiExport.py`). 373 tests pasan.
13. Siguiente: validacion manual de flujos de usuario (edicion, MIDI, exportacion
    Lilypond, impresion).

## Comandos de verificacion

```bash
grep -R "from PyQt4\\|import PyQt4" -n src build .github pylintrc
python3 -m py_compile $(find src -name '*.py' -not -path '*/__pycache__/*')
python3 -m unittest discover -s src/test
./run-drumburp.sh
```

Nota: la suite completa aun contiene fallos de migracion Python 3 no
relacionados directamente con PyQt. `testScore.py` tiene problemas de
`NotePosition`/comparaciones con `range`, y `testDrum.py` falla en
`testGetShortcuts` por una diferencia de atajo esperado (`c` vs `z`).
Conviene arreglarlos antes de usar toda la suite como semaforo final.

## Estado de avance

- Hecho: `ui_*.py` fue regenerado con `PyQt5.uic`.
- Hecho: se agrego `GUI/QtResourceCompat.py` para que las UI PyQt5 puedan cargar
  pixmaps desde archivos reales cuando aparezcan rutas `:/...`.
- Hecho: se quitaron imports `DrumBurp_rc` y `buttons_rc` de las UI regeneradas
  para evitar segfaults con recursos `pyrcc4`.
- Hecho: dialogos simples migrados a imports PyQt5.
- Hecho: `QNewScoreDialog`, `QDefaultKitManager`, `QComplexCountDialog` migrados
  sin `QVariant`.
- Hecho: `QEditKitDialog` migrado a PyQt5 directo.
- Hecho: `DrumBurp.py`, `Widgets/ScoreView.py` y `Widgets/measureTabs.py`
  migrados a PyQt5.
- Hecho: score/graphics migrado a PyQt5 directo: `QScore`, `QStaff`,
  `QMeasure`, `QMeasureLine`, `QLineLabel`, `QGraphicsListData`, `QSection`,
  `QNotationScene`.
- Hecho: soporte de aplicacion migrado: `DBMainwindow`, `DBCommands`,
  `DBFonts`, `DBIcons`, `DBColourPicker`, `QDisplayProperties`.
- Hecho: MIDI/exportacion/Lilypond migrado: `DBMidi`, `LilypondExporter`,
  `QLilypondPreview`, `DBFSM`, `QMeasureContextMenu`.
- Hecho: `python3 -m py_compile src/GUI/*.py src/Widgets/*.py` pasa.
- Hecho: `QT_QPA_PLATFORM=offscreen timeout 10s ./run-drumburp.sh` no muestra
  traceback ni segfault; termina por timeout porque la ventana queda abierta.
- Hecho: corregido crash de arranque por `QSettings.value(..., type=str)` con
  settings antiguos de QVariant tipo 1025.
- Hecho: corregido crash de `paperBox.currentIndexChanged` cuando PyQt5 enviaba
  texto en vez de indice.
- Hecho: conexiones `currentIndexChanged` restantes pasadas a sobrecarga `int`.
- Hecho: `*_rc.py` reemplazados por stubs no-op compatibles con PyQt5.
- Hecho: plugins de Qt Designer migrados a `PyQt5.QtDesigner`.
- Hecho: build/requirements/workflow/pylintrc actualizados a PyQt5/Python 3.
- Hecho: eliminada la capa temporal `src/PyQt4`.
- Hecho: suite de tests Python 3 completamente corregida (373 tests, todos OK):
  - `NotePosition.__cmp__`/`cmp()` reemplazado por `__eq__`/`__lt__`/`__le__`/
    `__gt__`/`__ge__`/`__hash__` (Python 3 no tiene `__cmp__` ni `cmp()`).
  - `MeasureCount.counterMaker`: division `/` cambiada a `//` para evitar float.
  - `MeasureCount.iterMidiTicks`/`iterTimesMs`: argumento `swing` hecho opcional
    con valor por defecto `0`.
  - `Drum.checkShortcuts`: `availableShortcuts.pop()` reemplazado por
    `min(availableShortcuts)` para orden deterministico en Python 3.
  - `fileUtils.Base64StringField`: codificacion base64 migrada de codec Python 2
    (`str.encode('base64')`) al modulo `base64` de Python 3.
  - `dbfsv0.startBarlineString`/`endBarlineString`: corregida logica de bitmask
    para `NO_BAR` (valor 0 siempre pasaba la condicion `& 0 == 0`).
  - `testCounter.TestDefaultRegistry.testIter`: actualizado de 11 a 23 counters
    (se agregaron Quintuplets, Septuplets y 64ths al registro por defecto).
  - `testScore`: comparaciones `range(...)` en asserts reemplazadas por
    `list(range(...))` (Python 3 `range` no es lista).
  - `testLilypond`: actualizado de `\times 2/3` a `\tuplet 3/2` (sintaxis
    moderna de LilyPond); corregida division entera en calculo de tuplet.
  - `testdbfsv0.testWriteDecorations`: actualizado orden de flags BARLINE para
    que coincida con el orden del dict `BAR_TYPES`.
- Hecho: `DBMainwindow.py` completamente limpiado de PyQt4:
  - Decorador no-op `pyqtSignature` eliminado del archivo.
  - `pyqtSlot` agregado al import de `PyQt5.QtCore`.
  - Los 35 `@pyqtSignature("")/("bool")/("int")` reemplazados por
    `@pyqtSlot()`/`@pyqtSlot(bool)`/`@pyqtSlot(int)`.
  - Los 3 slots `@staticmethod` convertidos a metodos de instancia normales
    (`on_actionWhatsThis_triggered`, `on_actionOnlineManual_triggered`,
    `on_actionMuteNotes_toggled`) para compatibilidad con autoconexion PyQt5.
- Pendiente: validacion manual amplia de flujos de usuario.
- Pendiente separado (no PyQt): compatibilidad con LilyPond 2.22+ — el signo
  de percusion `"open"` en la tabla `dbdrums` ya no es valido; requiere
  investigar la sintaxis correcta para LilyPond 2.24.

## Imports PyQt4 pendientes

Segun el ultimo grep:

- `grep -R "from PyQt4\\|import PyQt4" -n src build .github pylintrc --exclude-dir=__pycache__`
  no devuelve resultados.
- `grep -R "PyQt4\\|python2\\|Python 2.7\\|2.7.16" -n src build .github pylintrc --exclude-dir=__pycache__`
  no devuelve resultados.

Prioridad sugerida inmediata: usar la aplicacion manualmente para detectar
errores de runtime PyQt5 restantes y luego limpiar/fijar la suite de tests
Python 3.

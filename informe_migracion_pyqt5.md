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

Estos archivos no conviene editarlos a mano salvo como parche temporal. Lo
correcto es regenerarlos desde sus `.ui` con `pyuic5`.

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

Port necesario:

- Cambiar imports generados a `from PyQt5 import QtCore, QtGui, QtWidgets`.
- Reemplazar clases de widgets `QtGui.QWidget`, `QtGui.QLabel`,
  `QtGui.QDialogButtonBox`, etc. por `QtWidgets.*`.
- Mantener clases graficas puras como `QtGui.QIcon`, `QtGui.QPixmap`,
  `QtGui.QFont`.
- Reemplazar `QtCore.QString.fromUtf8` por identidad o eliminarlo.
- Reemplazar `QApplication.UnicodeUTF8` y llamadas de translate de 4 argumentos
  por `QtCore.QCoreApplication.translate(context, text, disambig)`.
- Reemplazar `QtCore.QObject.connect(... SIGNAL(...))` por `.connect`.
- Reemplazar `layout.setMargin(n)` por `layout.setContentsMargins(n, n, n, n)`.

Riesgo: medio. Son muchos cambios, pero mecanicos si existen los `.ui`.

## Recursos generados por pyrcc4

Archivos:

- `src/buttons_rc.py`
- `src/Widgets/buttons_rc.py`
- `src/GUI/DrumBurp_rc.py`

Port necesario:

- Regenerar desde `.qrc` con `pyrcc5`.
- Si no se regeneran, conservar temporalmente la compatibilidad de
  `qRegisterResourceData` porque pyrc4 emitia cadenas estilo Python 2 y PyQt5
  espera bytes.

Riesgo: bajo-medio. Si fallan, se pierden iconos/imagenes.

## Capa temporal de compatibilidad

Archivos:

- `src/PyQt4/__init__.py`
- `src/PyQt4/QtCore.py`
- `src/PyQt4/QtGui.py`

Estado:

- Debe quedarse mientras haya imports `PyQt4`.
- Actualmente cubre `QVariant`, `QSettings`, `QFileDialog`, `QDesktopServices`,
  `QApplication.translate`, `setMargin`, hover events y recursos.
- No debe ser el destino final. Cuando todo use PyQt5 o `QtCompat`, esta carpeta
  debe eliminarse.

Riesgo: alto si se elimina temprano.

## Codigo de aplicacion

### `src/DrumBurp.py`

- `QApplication` debe importarse desde `PyQt5.QtWidgets`.
- Influye en arranque completo de la app.
- Riesgo bajo.

### `src/GUI/DBMainwindow.py`

- Es el archivo central y el mas delicado.
- Migrar imports: widgets a `QtWidgets`, `QFontDatabase/QFont/QColor` a
  `QtGui`, `QPrinter` a `QtPrintSupport`, timers/settings a `QtCore`.
- Reemplazar `QVariant` y lecturas `settings.value(...).toString()` etc.
- Reemplazar `QDesktopServices.storageLocation`.
- Quitar `pyqtSignature` o usar `pyqtSlot`.
- `QFileDialog.getOpenFileName/getSaveFileName` en PyQt5 devuelve tupla; ajustar.
- Influye en casi todos los dialogos, archivos recientes, colores, Lilypond,
  MIDI, guardado/exportacion.
- Riesgo alto.

### `src/GUI/QScore.py`

- Migrar `QGraphicsScene`, `QGraphicsItem`, `QTransform`, `QMessageBox`,
  `QUndoStack` segun modulo PyQt5 correcto.
- Revisar menus/dialogos abiertos desde la escena.
- Ya depende de `QStaff`, `QMeasure`, `QMeasureLine`, `QKitData`, etc.
- Riesgo alto por interacciones graficas.

### `src/GUI/QStaff.py`

- Ya no debe heredar de `QGraphicsItemGroup`; en Qt5 captura eventos de hijos.
- Estado actual corregido: hereda de `QGraphicsItem`, hijos con `setParentItem`.
- Riesgo alto si se revierte.

### `src/GUI/QMeasure.py`

- Migrar `QGraphicsItem`, `QFontMetrics`, `QPen`, `QRectF`, eventos de mouse.
- Cambiar `setAcceptsHoverEvents` por `setAcceptHoverEvents`.
- Revisar `QFontMetrics.width` -> `horizontalAdvance`.
- Influye en clic para agregar notas, seleccion, menus y doble clic.
- Riesgo alto.

### `src/GUI/QMeasureLine.py`

- Migrar `QGraphicsItem`, `QPen`, eventos de mouse y menu contextual.
- Influye en menus de barras de compas.
- Riesgo medio.

### `src/GUI/QLineLabel.py`

- Migrar `QGraphicsItem`, hover events y pintura.
- Influye en etiquetas/abreviaturas de bateria y resaltado de linea.
- Riesgo medio.

### `src/GUI/QGraphicsListData.py`

- Migrar `QGraphicsItem`, `QFontMetrics`, `QPen`, hover events.
- Riesgo medio.

### `src/GUI/QSection.py`

- `QGraphicsTextItem` queda en `QtWidgets`; `QTextCursor` queda en `QtGui`.
- Riesgo medio.

### `src/GUI/QNotationScene.py`

- `QGraphicsScene` pasa a `QtWidgets`; `QPixmap` queda en `QtGui`.
- Ya se corrigio division entera para Python 3.
- Riesgo medio.

### `src/GUI/QEditKitDialog.py`

- Migrar dialogo y widgets a `QtWidgets`; `QColor` a `QtGui`.
- Ya se corrigieron `QVariant`, `findData`, `toInt`, `setTextColor`.
- Reemplazar `QDesktopServices.storageLocation`.
- Influye en kits, heads MIDI y default kits.
- Riesgo alto.

### `src/GUI/QComplexCountDialog.py`

- Reemplazar `QVariant` en `QListWidgetItem.setData`.
- Reemplazar `item.data(...).toInt()[0]` por `int(item.data(...))`.
- Quitar `pyqtSignature`.
- Riesgo medio.

### `src/GUI/QNewScoreDialog.py`

- Reemplazar `QVariant(False/True)` por bool.
- Reemplazar `.toBool()` por `bool(...)`.
- Reemplazar `settings.value(...).toString()` por `settings.value(..., "", type=str)`.
- Riesgo medio.

### `src/GUI/QDefaultKitManager.py`

- Reemplazar `QtCore.QVariant` por bool.
- Reemplazar `.toBool()` por `bool(...)`.
- Reemplazar `settings.value(...).toString()` por str.
- Quitar `pyqtSignature`.
- Riesgo medio.

### `src/GUI/DBColourPicker.py`

- Widgets a `QtWidgets`; `QColor`, `QPen` a `QtGui`.
- `QColor.toString()` sigue existiendo.
- `QColorDialog` esta en `QtWidgets`.
- Riesgo medio.

### `src/GUI/DBMidi.py`

- `QThread`, `QObject`, `QTimer`, `pyqtSignal` pasan a `QtCore`.
- Revisar senales y thread lifetime.
- Riesgo alto por reproduccion MIDI.

### `src/GUI/LilypondExporter.py`

- `QThread` pasa a `QtCore`.
- Riesgo medio.

### `src/GUI/QLilypondPreview.py`

- `QMessageBox` y `QGraphicsScene` pasan a `QtWidgets`; `QPixmap` queda en
  `QtGui`; `QTimeLine` y `pyqtSignal` quedan en `QtCore`.
- Riesgo medio.

### `src/GUI/DBCommands.py`

- `QUndoCommand` pasa a `QtWidgets`.
- Riesgo medio-alto porque afecta undo/redo.

### `src/GUI/DBFonts.py`

- `QFontDatabase`, `QFont` pasan a `QtGui`.
- Riesgo bajo.

### `src/GUI/DBIcons.py`

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

Port necesario:

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

- `QGraphicsView` pasa a `QtWidgets`.
- `QTimeLine`, `QMutex`, `pyqtSlot`, `pyqtSignal` quedan en `QtCore`.
- Influye en scroll, zoom y navegacion visual.
- Riesgo medio.

### `src/Widgets/measureTabs.py`

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

- Cambiar hidden import de `PyQt4.QtGui` a los modulos PyQt5 usados:
  `PyQt5.QtWidgets`, `PyQt5.QtGui`, `PyQt5.QtCore`, `PyQt5.QtPrintSupport`.
- Revisar PyInstaller hooks para PyQt5.
- Riesgo medio.

### `build/install_pyqt.ps1`

- Es instalador historico de PyQt4 para Windows/Python 2.7.
- Debe sustituirse por instalacion PyQt5 via pip o eliminarse si no se soporta
  ese build.
- Riesgo bajo para Debian 12.

### `.github/workflows/build.yml`

- Actualizar acciones para Python 3.
- Eliminar cache/instalacion/import de PyQt4.
- Instalar `PyQt5`, `pygame` y dependencias del sistema.
- Riesgo medio.

### `pylintrc`

- Cambiar `extension-pkg-whitelist=PyQt4` por PyQt5, o eliminar si pylint ya no
  lo necesita.
- Riesgo bajo.

## Orden de implementacion propuesto

1. Corregir fallos runtime que aparezcan con la capa actual.
2. Regenerar recursos `*_rc.py` con `pyrcc5`.
3. Regenerar `ui_*.py` con `pyuic5`.
4. Migrar dialogos simples.
5. Migrar `QNewScoreDialog`, `QDefaultKitManager`, `QComplexCountDialog`.
6. Migrar `QEditKitDialog`.
7. Migrar `QScore`, `QStaff`, `QMeasure`, `QMeasureLine`, `QLineLabel`.
8. Migrar `DBMainwindow`.
9. Migrar build/CI.
10. Borrar `src/PyQt4` y verificar que no queden imports PyQt4.

## Comandos de verificacion

```bash
grep -R "from PyQt4\\|import PyQt4" -n src build .github pylintrc
python3 -m py_compile $(find src -name '*.py' -not -path '*/__pycache__/*')
python3 -m unittest discover -s src/test
./run-drumburp.sh
```

Nota: `testScore.py` aun contiene fallos de migracion Python 3 no relacionados
directamente con PyQt (`NotePosition` sin orden/equivalencia moderna y
comparaciones lista vs `range`). Conviene arreglarlos antes de usar toda la
suite como semaforo final.

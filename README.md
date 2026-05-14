# DrumBurp 1.1.2 actualizado para Debian 12

Esta copia fue modernizada para que el código antiguo de DrumBurp pueda ejecutarse con Python 3 y PyQt5 en Debian 12/MX Linux 23.

## Instalar dependencias

```bash
sudo apt update
sudo apt install python3-pyqt5 python3-pygame lilypond
```

`lilypond` es opcional, pero se recomienda si vas a usar exportación/preview con LilyPond.

## Ejecutar

Desde esta carpeta:

```bash
./run-drumburp.sh
```

O manualmente:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

## Qué se actualizó

- Conversión base de Python 2 a Python 3: `print`, `except`, `xrange`, `unicode`, `iteritems`, etc.
- Corrección de sintaxis incompatible con Python 3.
- Capa de compatibilidad `src/PyQt4/` para que el código antiguo que importa `PyQt4` funcione usando `PyQt5` en Debian 12.
- Compatibilidad para archivos `.ui` generados por `pyuic4`, incluyendo `QApplication.UnicodeUTF8`, `QString.fromUtf8` y `setMargin()`.
- Compatibilidad para recursos `.qrc` antiguos generados para Python 2.
- Script `run-drumburp.sh` para lanzar el programa sin instalarlo globalmente.

## Nota honesta

No pude abrir la interfaz gráfica dentro de este entorno porque aquí no están instalados PyQt5/pygame ni hay sesión gráfica real. Sí verifiqué que todo el código Python compila sin errores de sintaxis con Python 3.

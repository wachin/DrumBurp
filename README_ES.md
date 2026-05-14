# DrumBurp 1.1.3 — port a Python 3 / PyQt5

Fork de [DrumBurp](https://github.com/Whatang/DrumBurp) por Washington Indacochea Delgado.  
Port completo de PyQt4/Python 2 a PyQt5/Python 3, probado en Debian 12 / MX Linux 23 / UbuntuStudio.

## Instalar dependencias

```bash
sudo apt install python3-pyqt5 python3-pygame python3-pyqt5.qtmultimedia \
                 pyqt5-dev-tools lilypond fluid-soundfont-gm
```

- `python3-pyqt5.qtmultimedia` — necesario para reproduccion MIDI
- `pyqt5-dev-tools` — incluye `pyuic5` y `pyrcc5` (solo si se regeneran archivos UI/QRC)
- `lilypond` — opcional, para exportar/previsualizar partituras
- `fluid-soundfont-gm` — fuente de sonido General MIDI (necesaria para MIDI)

## Ejecutar

```bash
./run-drumburp.sh
```

O manualmente:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

## Reproduccion MIDI en Linux

Para que DrumBurp reproduzca sonido MIDI necesitas un sintetizador virtual activo.
La forma recomendada depende de tu sistema operativo.

### Opcion recomendada — Qsynth con JACK (UbuntuStudio / AV Linux)

La manera mas comoda es usar un sistema operativo orientado a audio como:

- **[Ubuntu Studio](https://ubuntustudio.org/)** — incluye JACK y Qsynth preconfigurados
- **[AV Linux](https://www.bandshed.net/)** — otra excelente opcion para audio profesional en Linux

En estos sistemas basta con:

1. Iniciar JACK (o que arranque automaticamente al login)
2. Abrir **Qsynth** y cargar la fuente de sonido `FluidR3_GM.sf2`
   (incluida en el paquete `fluid-soundfont-gm`, ruta tipica:
   `/usr/share/sounds/sf2/FluidR3_GM.sf2`)
3. Lanzar DrumBurp — detectara el sintetizador automaticamente

### Opcion alternativa — TiMidity (cualquier distro Debian/Ubuntu)

Si no tienes JACK disponible puedes usar TiMidity como sintetizador virtual:

**1. Instalar:**

```bash
sudo apt install timidity fluid-soundfont-gm alsa-utils
```

**2. Cargar el modulo de secuenciador MIDI:**

```bash
modprobe snd_seq
```

**3. Arrancar TiMidity en modo servidor:**

```bash
timidity -iA -Os -B2,8 &
```

Esto inicia TiMidity en segundo plano escuchando en los puertos ALSA (tipicamente `128:0`).
Puedes verificarlo con `aconnect -l`.

**4. Lanzar DrumBurp** — ya detectara los puertos MIDI activos.

**Para detener TiMidity cuando termines:**

```bash
killall timidity
```

> **Nota:** El comando `modprobe snd_seq` activa el secuenciador MIDI del kernel.
> Sin el, los programas no pueden conectarse entre si para enviar notas MIDI.
> En UbuntuStudio y AV Linux esto ya esta activo por defecto.

## Que se actualizo respecto al original

- Port completo de PyQt4 a PyQt5: todos los imports, senales, slots y recursos
- Port de Python 2 a Python 3: division entera, `base64`, comparaciones, `exec()`, etc.
- Archivos UI regenerados con `pyuic5`; recursos QRC regenerados con `pyrcc5`
- Eliminada la capa de compatibilidad temporal `src/PyQt4/`
- Exportacion a PDF via LilyPond 2.24 corregida
- Divisiones enteras en calculos MIDI y Lilypond corregidas
- Ventana "Acerca de" actualizada con creditos del port
- Version actualizada a 1.1.3

Ver `informe_migracion_pyqt5.md` para el detalle tecnico completo.

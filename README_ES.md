# DrumBurp

DrumBurp es una interfaz grafica simple para crear y editar notacion musical de bateria.

El objetivo de DrumBurp es hacer que la experiencia de escribir musica para bateria sea
lo mas rapida e intuitiva posible. La generalidad de muchos paquetes de notacion musical
existentes implica una complejidad innecesaria a la hora de escribir notacion para bateria.
Si bien estos paquetes pueden producir resultados hermosos y manejar todo lo que uno pudiera
querer notificar, pueden ser lentos y pesados de usar. Al dejar en claro que el objetivo de
DrumBurp se limita a escribir musica *unicamente* para bateria, se busca eliminar las
dificultades que impone esa generalidad.

DrumBurp nunca tendra un modo para gaitas.

La filosofia fundamental de DrumBurp es la siguiente: ante la disyuntiva entre agregar
funcionalidad/complejidad en un caso especifico, o mantener velocidad, simplicidad e
interaccion intuitiva en el caso general, el caso general siempre gana. Simple, rapido
y directo es mejor que complejo, lento e ingenioso.

DrumBurp se centra en una representacion simple de la musica para bateria. Para cada nota
que tocas, esencialmente le importa:

- **Cual** tambor golpeas
- **Cuando** lo golpeas
- **Como** lo golpeas

Estos tres datos son suficientes para escribir musica de bateria en notacion de tablatura.
DrumBurp busca que el baterista pueda ingresar esa informacion a la computadora de la
manera mas rapida y sencilla posible.

DrumBurp almacena esta informacion en su propio formato en los archivos de partitura
guardados. Sin embargo, puede exportar la tablatura como archivos de texto ASCII facilmente.
Un objetivo a largo plazo de DrumBurp es poder generar notacion "real" de bateria tan
estetica y legible como la producida por Lilypond o Nted.

Las estructuras de datos fundamentales de DrumBurp raramente, si acaso alguna vez,
cambiaran. La parte mas importante de DrumBurp es su interfaz con el usuario. Su objetivo
para el usuario es: menos tiempo escribiendo, mas tiempo tocando.

---

## Este fork — port a Python 3 / PyQt5 (version 1.1.3)

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

Ver `migration_report_pyqt5_ES.md` para el detalle tecnico completo.

## Licencia

DrumBurp es software libre: puedes redistribuirlo y/o modificarlo bajo los terminos
de la Licencia Publica General GNU publicada por la Free Software Foundation, ya sea
la version 3 de la Licencia, o (a tu eleccion) cualquier version posterior.

Este programa se distribuye con la esperanza de que sea util, pero SIN NINGUNA GARANTIA;
ni siquiera la garantia implicita de COMERCIABILIDAD o IDONEIDAD PARA UN PROPOSITO
PARTICULAR. Consulta la Licencia Publica General GNU para mas detalles.

Deberias haber recibido una copia de la Licencia Publica General GNU junto con este
programa. Si no es asi, visita <https://www.gnu.org/licenses/>.

Consulta el archivo `COPYING.txt` para el texto completo de la GPL.

**Autor original:** Michael Thomas — drumburp@whatang.org  
**Port a PyQt5:** Washington Indacochea Delgado — linuxfrontier@proton.me

---

## Internacionalizacion (i18n) — para desarrolladores

DrumBurp soporta multiples idiomas mediante Qt Linguist y archivos `.qm` de traduccion.

### Instalar las herramientas necesarias

```bash
sudo apt install pyqt5-dev-tools qttools5-dev-tools
# incluye: pylupdate5, lrelease, linguist
```

### Archivos de traduccion

```
drumburp.pro              Archivo de proyecto Qt — lista todos los archivos fuente
src/i18n/
  i18n.py                 Cargador de traducciones (se llama al iniciar)
  drumburp_en.ts          Referencia en ingles (fuente de verdad)
  drumburp_es.ts          Traduccion al espanol
  drumburp_en.qm          Binario compilado en ingles
  drumburp_es.qm          Binario compilado en espanol
```

### Actualizar cadenas despues de editar el codigo fuente

```bash
# Re-extraer todas las cadenas de los archivos Python y .ui
pylupdate5 drumburp.pro

# Recompilar despues de traducir
lrelease src/i18n/drumburp_en.ts -qm src/i18n/drumburp_en.qm
lrelease src/i18n/drumburp_es.ts -qm src/i18n/drumburp_es.qm
```

### Traducir usando la interfaz grafica de Qt Linguist

```bash
linguist src/i18n/drumburp_es.ts
```

### Probar en un idioma especifico

```bash
# Espanol
LANGUAGE=es ./run-drumburp.sh
./run-drumburp.sh --language es

# Ingles explicito
./run-drumburp.sh --language en

# Usar la configuracion regional del sistema
./run-drumburp.sh
```

### Agregar un nuevo idioma (ejemplo: frances)

1. Agregar `src/i18n/drumburp_fr.ts` a `drumburp.pro` bajo `TRANSLATIONS`
2. Ejecutar `pylupdate5 drumburp.pro` — crea el nuevo archivo `.ts`
3. Traducir con `linguist src/i18n/drumburp_fr.ts`
4. Ejecutar `lrelease src/i18n/drumburp_fr.ts -qm src/i18n/drumburp_fr.qm`
5. Probar con `LANGUAGE=fr ./run-drumburp.sh`

Consulte `ROADMAP_i18n.md` para el plan completo de i18n y el progreso.

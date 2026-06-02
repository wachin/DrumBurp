# DrumBurp

- Copyright (C) 2011-2019 Michael Thomas  
- Python 3 / PyQt5 fork and modifications (C) 2024-2026 Washington Indacochea Delgado  

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
Port completo de PyQt4/Python 2 a PyQt5/Python 3, probado en Debian 12 / MX Linux 23 / Ubuntu 26.04.

📖 **[Manual completo → GitHub Wiki](https://github.com/wachin/DrumBurp/wiki)**

## Ejecutar desde el codigo fuente, explicado simple

DrumBurp se puede usar con todas sus funciones directamente desde esta carpeta
de codigo fuente. No es necesario compilar el programa ni crear un instalador
antes de usarlo.

Esto es normal en muchos programas hechos en Python: Python lee los archivos del
programa y los ejecuta directamente. En la practica, cuando Python y las
dependencias necesarias ya estan instaladas, la carpeta de DrumBurp funciona de
forma parecida a un programa portable. Se puede iniciar desde la carpeta con
`./run-drumburp.sh` en Linux, con `run-drumburp.bat` en Windows, o con los
`run-drumburp.command` en macOS, o con los comandos de Python indicados mas
abajo.

Lo que hay que instalar depende del sistema operativo:

- **Linux:** Python 3 normalmente ya viene instalado, pero DrumBurp necesita los
  paquetes PyQt5 y pygame indicados abajo.
- **Windows:** primero hay que instalar Python, y despues instalar los paquetes
  de Python con `pip`.
- **macOS:** es mejor no depender del Python incluido por Apple; instala primero
  una version actual de Python, por ejemplo con Homebrew, y despues instala los
  paquetes de Python con `pip`.

## Instalar dependencias

```bash
sudo apt install python3-pyqt5 python3-pygame pyqt5-dev-tools lilypond
```

- `python3-pygame` — necesario para reproduccion MIDI
- `pyqt5-dev-tools` — incluye `pyuic5` y `pyrcc5` (solo si se regeneran archivos UI/QRC)
- `lilypond` — opcional, para exportar/previsualizar partituras

## Ejecutar

```bash
./run-drumburp.sh
```

O manualmente:

```bash
export PYTHONPATH="$PWD/src"
python3 src/DrumBurp.py
```

## Ejecutar en Windows

En primer lugar, necesitas instalar Python [Python](https://www.python.org/downloads/) y durante la instalación selecciona instalar en `PATH`.

. Abre **PowerShell** en la carpeta de DrumBurp e instala las
dependencias:

```powershell
py -m pip install --upgrade pip
py -m pip install PyQt5 PyQt5-sip pygame
```

En Windows, `pygame` queda como soporte de reserva, pero la reproduccion MIDI
principal usa el backend nativo WinMM de Windows.

Despues de instalar las dependencias, puedes iniciar DrumBurp haciendo doble clic
en `run-drumburp.bat`.

O manualmente desde PowerShell:

```powershell
$env:PYTHONPATH = "$PWD\src"
py .\src\DrumBurp.py
```

### Reproduccion MIDI en Windows con VirtualMIDISynth

Para obtener buen sonido MIDI en Windows, instala
[CoolSoft VirtualMIDISynth](https://coolsoft.altervista.org/en/virtualmidisynth).
VirtualMIDISynth crea una salida MIDI de Windows y se encarga de cargar los
SoundFonts fuera de DrumBurp.

Despues de instalar VirtualMIDISynth:

1. Descarga uno o mas SoundFonts recomendados desde la pagina de
   VirtualMIDISynth.
2. Abre la ventana de configuracion de VirtualMIDISynth.
3. En la pestana **Soundfonts**, haz clic en el boton **+**.
4. Busca el archivo SoundFont que descargaste y agregalo.
5. Activa solo el SoundFont que quieres usar. VirtualMIDISynth puede mostrar
   varios SoundFonts, pero para una reproduccion predecible conviene usar solo
   uno a la vez.

Inicia DrumBurp desde la carpeta del repositorio:

```powershell
$env:PYTHONPATH = "$PWD\src"
py .\src\DrumBurp.py
```

Luego elige:

```text
MIDI -> Select MIDI out -> VirtualMIDISynth #1
```

Con esta configuracion, DrumBurp reproduce correctamente la tablatura de
bateria usando VirtualMIDISynth. DrumBurp no carga SoundFonts internamente;
VirtualMIDISynth ya se encarga de eso.

## Ejecutar en macOS

Estas instrucciones son para probar DrumBurp desde el codigo fuente en macOS.
Instala primero Python, por ejemplo con Homebrew:

```bash
brew install python
```

Desde la carpeta de DrumBurp, crea un entorno virtual e instala las dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install PyQt5 PyQt5-sip pygame
```

Despues de instalar las dependencias, puedes iniciar DrumBurp haciendo doble clic
en `run-drumburp.command`.

Si macOS indica que el lanzador no es ejecutable, ejecuta esto una sola vez desde
Terminal:

```bash
chmod +x run-drumburp.command
```

O manualmente desde Terminal:

```bash
export PYTHONPATH="$PWD/src"
python src/DrumBurp.py
```

## Reproduccion MIDI

DrumBurp reproduce sonido MIDI usando el backend nativo WinMM de Windows en
Windows, y `pygame` en otros sistemas. En Windows, esto permite reproducir a
traves de dispositivos MIDI como VirtualMIDISynth, Microsoft GS Wavetable Synth
u otros puertos MIDI de Windows.

La exportacion a `.mid` usa el generador MIDI interno de DrumBurp, por lo que
puede probarse aunque la salida de audio del sistema este en silencio.

Si DrumBurp arranca pero no suena:

- Revisa que el sistema tenga una salida de audio/MIDI activa.
- En Windows, instala VirtualMIDISynth y agrega un SoundFont en la pestana
  **Soundfonts**.
- Usa **MIDI -> Refresh Device List** para volver a detectar dispositivos MIDI.
- En Windows, elige **MIDI -> Select MIDI out -> VirtualMIDISynth #1**.
- Prueba **File → Export MIDI** y abre el `.mid` resultante con otro reproductor
  para confirmar que la generacion MIDI funciona.
- JACK, Qsynth o TiMidity pueden servir como salidas MIDI adicionales en algunos
  sistemas, pero no son requisitos de DrumBurp para una instalacion normal.

## Que se actualizo respecto al original

- Port completo de PyQt4 a PyQt5: todos los imports, senales, slots y recursos
- Port de Python 2 a Python 3: division entera, `base64`, comparaciones, `exec()`, etc.
- Archivos UI regenerados con `pyuic5`; recursos QRC regenerados con `pyrcc5`
- Eliminada la capa de compatibilidad temporal `src/PyQt4/`
- Exportacion a PDF via LilyPond 2.24 corregida
- Reproduccion MIDI nativa en Windows mediante WinMM agregada, incluyendo
  seleccion de dispositivos como VirtualMIDISynth
- Divisiones enteras en calculos MIDI y Lilypond corregidas
- Ventana "Acerca de" actualizada con creditos del port
- Version actualizada a 1.1.3

Ver `migration_report_pyqt5_ES.md` para el detalle tecnico completo.

📖 **[Manual completo → GitHub Wiki](https://github.com/wachin/DrumBurp/wiki)**  
🐛 **[Reportar problemas](https://github.com/wachin/DrumBurp/issues)**

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

# Cómo publicar una Release en GitHub usando GitHub Actions

Este tutorial explica paso a paso cómo usar el sistema de CI/CD de DrumBurp
para compilar automáticamente los instaladores de Linux y Windows y publicarlos
como una Release oficial en GitHub.

**Repositorio:** https://github.com/wachin/DrumBurp  
**Autor del port PyQt5:** Washington Indacochea Delgado

---

## Índice

1. [Cómo funciona el sistema](#1-cómo-funciona-el-sistema)
2. [Requisito previo: permisos en GitHub](#2-requisito-previo-permisos-en-github)
3. [Flujo completo de trabajo](#3-flujo-completo-de-trabajo)
4. [Paso a paso para publicar una release](#4-paso-a-paso-para-publicar-una-release)
5. [Qué hace cada job del workflow](#5-qué-hace-cada-job-del-workflow)
6. [Cómo ver el progreso en GitHub](#6-cómo-ver-el-progreso-en-github)
7. [Qué archivos se publican](#7-qué-archivos-se-publican)
8. [Solución de problemas comunes](#8-solución-de-problemas-comunes)
9. [Referencia rápida de comandos](#9-referencia-rápida-de-comandos)

---

## 1. Cómo funciona el sistema

El archivo `.github/workflows/build.yml` define una serie de tareas automáticas
(llamadas **jobs**) que GitHub ejecuta en sus servidores cada vez que haces un
`git push`.

El comportamiento varía según lo que empujes:

| Qué empujas | Qué ocurre |
|---|---|
| Un commit a cualquier rama (excepto `master`) | Se compila y se prueban Linux y Windows |
| Un tag con formato `v1.2.3` | Se compila, se prueba **y se publica una Release** |
| Un commit directo a `master` | No se ejecuta nada (protección para no compilar en master) |

Los archivos que se publican automáticamente son:

- `DrumBurp-1.1.3.0-setup.exe` — instalador para Windows
- `DrumBurp` — binario ejecutable para Linux x64

---

## 2. Requisito previo: permisos en GitHub

Antes de que el workflow pueda crear Releases, necesitas activar los permisos
correctos en tu fork.

1. Ve a tu repositorio en GitHub: `https://github.com/wachin/DrumBurp`
2. Haz clic en **Settings** (pestaña superior derecha)
3. En el menú izquierdo, busca **Actions** → **General**
4. Baja hasta la sección **Workflow permissions**
5. Selecciona **Read and write permissions**
6. Haz clic en **Save**

![Workflow permissions](https://docs.github.com/assets/cb-17142/mw-1440/images/help/settings/actions-workflow-permissions.webp)

> **Por qué es necesario:** El workflow usa el token `GITHUB_TOKEN` para crear
> la Release y subir los archivos. Sin permisos de escritura, ese paso falla
> con un error 403.

---

## 3. Flujo completo de trabajo

```
Tu máquina local                    GitHub Actions (servidores de GitHub)
─────────────────                   ──────────────────────────────────────
1. Editas el código
2. Actualizas VERSION y DBVersionNum.py
3. git add + git commit
4. git tag v1.1.3
5. git push origin dev        ──►   build_linux  ──► test_linux  ──┐
   git push origin v1.1.3    ──►   build_windows ──► test_windows ──┤
                                                                     ▼
                                                               release job
                                                          (crea la Release
                                                           en GitHub y sube
                                                           los instaladores)
```

---

## 4. Paso a paso para publicar una release

### 4.1 Actualizar el número de versión

Hay dos archivos que deben tener el mismo número de versión:

**`VERSION`** (en la raíz del proyecto):
```
1.1.3
```

**`src/DBVersionNum.py`**:
```python
DB_VERSION_STRING = '1.1.3'
```

**`build/DrumBurp.nsi`** (instalador Windows, formato `X.Y.Z.0`):
```nsi
!define VERSION "1.1.3.0"
```

### 4.2 Confirmar los cambios

```bash
git add VERSION src/DBVersionNum.py build/DrumBurp.nsi
git commit -m "Bump version to 1.1.3"
```

### 4.3 Crear el tag de versión

El tag **debe** empezar con `v` minúscula seguido del número de versión.
Ese formato es lo que activa el job de release en el workflow.

```bash
git tag v1.1.3
```

Para ver los tags existentes:
```bash
git tag -l
```

### 4.4 Empujar la rama y el tag

Es importante empujar **ambos** por separado. Un `git push` normal no empuja
los tags.

```bash
# Empujar los commits de tu rama de desarrollo
git push origin dev

# Empujar el tag (esto dispara el workflow de release)
git push origin v1.1.3
```

O si quieres empujar todos los tags de una vez:
```bash
git push origin dev --tags
```

### 4.5 Verificar en GitHub

Ve a la pestaña **Actions** de tu repositorio:
```
https://github.com/wachin/DrumBurp/actions
```

Verás una ejecución nueva con el nombre del tag. Haz clic en ella para ver
el progreso en tiempo real.

Cuando todos los jobs terminen con ✅, ve a la pestaña **Releases**:
```
https://github.com/wachin/DrumBurp/releases
```

Ahí estará la nueva release con los dos archivos adjuntos.

---

## 5. Qué hace cada job del workflow

El workflow tiene 5 jobs que se ejecutan en este orden:

```
build_linux ──► test_linux ──┐
                              ├──► release
build_windows ──► test_windows ──┘
```

### `build_linux`

Se ejecuta en un servidor Ubuntu de GitHub.

1. Descarga el código del repositorio
2. Instala Python 3.11 y las dependencias de PyQt5
3. **Ejecuta los 373 tests unitarios** — si alguno falla, el build se detiene
4. Compila el binario con PyInstaller
5. Guarda el binario como artefacto temporal

### `test_linux`

1. Descarga el binario compilado
2. Lo ejecuta con `--pyinstaller-test` para verificar que arranca sin errores

### `build_windows`

Se ejecuta en un servidor Windows de GitHub.

1. Descarga el código
2. Instala Python 3.11, NSIS (creador de instaladores) y las dependencias
3. Compila el `.exe` con PyInstaller
4. Empaqueta el `.exe` en un instalador `.exe` con NSIS
5. Guarda el instalador como artefacto temporal

### `test_windows`

1. Instala el instalador en modo silencioso (`/S`)
2. Ejecuta `DrumBurp.exe --pyinstaller-test`

### `release`

Solo se ejecuta cuando el push es un tag que empieza por `v`.

1. Descarga los artefactos de los jobs de build
2. Crea una Release en GitHub con el nombre `DrumBurp 1.1.3`
3. Adjunta el instalador Windows y el binario Linux a la Release

---

## 6. Cómo ver el progreso en GitHub

1. Ve a `https://github.com/wachin/DrumBurp/actions`
2. Haz clic en la ejecución más reciente
3. Verás los jobs en el panel izquierdo con iconos de estado:
   - 🟡 Amarillo girando — en progreso
   - ✅ Verde — completado con éxito
   - ❌ Rojo — falló

4. Haz clic en cualquier job para ver los logs detallados paso a paso

Si un job falla, el log te mostrará exactamente qué comando falló y el
mensaje de error completo.

---

## 7. Qué archivos se publican

Cuando el workflow termina con éxito, la Release en GitHub contiene:

| Archivo | Descripción |
|---|---|
| `DrumBurp-1.1.3.0-setup.exe` | Instalador para Windows (creado con NSIS) |
| `DrumBurp` | Binario autocontenido para Linux x64 (creado con PyInstaller) |

El binario de Linux incluye Python, PyQt5 y todas las dependencias dentro
de un solo archivo ejecutable. No requiere instalación.

Para usarlo en Linux:
```bash
chmod +x DrumBurp
./DrumBurp
```

---

## 8. Solución de problemas comunes

### El job de release falla con error 403

**Causa:** Los permisos del workflow no tienen escritura.  
**Solución:** Ver la sección [2. Requisito previo: permisos en GitHub](#2-requisito-previo-permisos-en-github).

### El tag no dispara el workflow de release

**Causa:** El tag no empieza con `v` minúscula.  
**Solución:** El workflow solo reacciona a tags con formato `v1.2.3`.
Borra el tag incorrecto y crea uno nuevo:
```bash
git tag -d 1.1.3           # borra el tag local
git push origin :1.1.3     # borra el tag remoto
git tag v1.1.3             # crea el tag correcto
git push origin v1.1.3     # empuja el tag correcto
```

### Los tests unitarios fallan en el CI

**Causa:** Algún cambio en el código rompió un test.  
**Solución:** Ejecuta los tests localmente antes de hacer push:
```bash
PYTHONPATH=src python3 -m unittest discover -s src/test
```
Todos los 373 tests deben pasar antes de publicar.

### El binario de Linux no arranca en el smoke test

**Causa:** Falta alguna dependencia del sistema en el runner de GitHub.  
**Solución:** Revisa el log del job `build_linux` y verifica que el paso
"Install system Qt/audio deps" completó sin errores.

### El instalador de Windows no se genera

**Causa:** NSIS no está instalado o el script `.nsi` tiene un error.  
**Solución:** Verifica que el job `build_windows` incluye el paso
`choco install nsis` y que `build/DrumBurp.nsi` tiene la versión correcta.

---

## 9. Referencia rápida de comandos

```bash
# Ver la versión actual
cat VERSION

# Actualizar versión (editar manualmente VERSION y src/DBVersionNum.py)

# Ver tags existentes
git tag -l

# Crear un tag de versión
git tag v1.1.3

# Empujar rama y tag para disparar el release
git push origin dev
git push origin v1.1.3

# Empujar todos los tags de una vez
git push origin dev --tags

# Ejecutar tests localmente antes de publicar
PYTHONPATH=src python3 -m unittest discover -s src/test

# Ver el estado de los workflows en la terminal (requiere GitHub CLI)
gh run list
gh run watch
```

---

## Estructura de archivos relevantes

```
.github/
  workflows/
    build.yml              # Define todo el pipeline de CI/CD

build/
  build_linux.sh           # Script de compilación para Linux (PyInstaller)
  build_windows.ps1        # Script de compilación para Windows (PyInstaller + NSIS)
  DrumBurp.nsi             # Script del instalador Windows (NSIS)
  requirements-linux.txt   # Dependencias pip para el build de Linux
  requirements-windows.txt # Dependencias pip para el build de Windows
  install_linux.sh         # Instala dependencias del sistema en Linux
  install_windows.ps1      # Instala dependencias del sistema en Windows

VERSION                    # Número de versión (una línea: 1.1.3)
src/DBVersionNum.py        # Número de versión para el código Python
```

---

*Tutorial escrito para el fork de DrumBurp portado a Python 3 / PyQt5.*  
*Contacto: Washington Indacochea Delgado — linuxfrontier@proton.me*

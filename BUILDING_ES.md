# Compilar DrumBurp

Este documento explica como crear ejecutables de DrumBurp para Linux, Windows y
macOS usando GitHub Actions. Esta pensado para alguien que nunca ha usado GitHub
Actions.

## Resumen corto

Si el repositorio esta en GitHub, si tiene el archivo
`.github/workflows/build.yml`, y si GitHub Actions esta activado, GitHub puede
compilar DrumBurp automaticamente en sus propios servidores.

El workflow actual crea:

- **Linux:** un binario autocontenido llamado `DrumBurp`.
- **Windows:** un instalador `.exe` creado con NSIS.
- **macOS:** un archivo `.zip` que contiene `DrumBurp.app`.

No necesitas tener Linux, Windows y macOS instalados en tu computadora local para
crear esos archivos. GitHub usa maquinas virtuales llamadas **runners**:

- `ubuntu-latest` para Linux
- `windows-latest` para Windows
- `macos-15-intel` para macOS Intel/x64

Documentacion oficial de GitHub:

- GitHub-hosted runners: <https://docs.github.com/actions/reference/runners/github-hosted-runners>
- Permisos de `GITHUB_TOKEN`: <https://docs.github.com/actions/security-for-github-actions/security-guides/automatic-token-authentication>

## Que archivos participan

### `.github/workflows/build.yml`

Es la receta principal de GitHub Actions. Le dice a GitHub:

1. En que sistemas operativos compilar.
2. Que version de Python instalar.
3. Que dependencias instalar.
4. Que pruebas ejecutar.
5. Que scripts de `build/` ejecutar.
6. Que archivos guardar como artefactos.
7. Que archivos subir a una Release cuando se empuja un tag.

### `build/`

Contiene los scripts usados por el workflow:

- `build/build_linux.sh` crea el binario Linux con PyInstaller.
- `build/build_windows.ps1` crea la carpeta Windows con Nuitka y luego el
  instalador `.exe` con NSIS.
- `build/build_macos.sh` crea `DrumBurp.app` con PyInstaller y lo empaqueta en
  un `.zip`.
- `build/install_macos.sh` instala dependencias de build en macOS con Homebrew
  y `pip`.
- `build/requirements-linux.txt` lista paquetes Python para construir en Linux.
- `build/requirements-windows.txt` lista paquetes Python para construir en
  Windows.
- `build/requirements-macos.txt` lista paquetes Python para construir en macOS.
- `build/DrumBurp.nsi` es la receta del instalador Windows.

### `.versionflow`

Configura `versionflow`, la herramienta usada para mantener sincronizado el
numero de version en:

- `VERSION`
- `src/DBVersionNum.py`
- `build/DrumBurp.nsi`

El valor `current_version` debe coincidir con la version actual del proyecto.

## Que ocurre cuando haces push

El workflow se ejecuta con `on: push`, es decir, cada vez que subes commits o
tags al repositorio.

| Que subes a GitHub | Que hace Actions |
|---|---|
| Un commit a una rama normal, por ejemplo `dev` | Compila y prueba Linux, Windows y macOS. Guarda los resultados como artefactos temporales. |
| Un tag con formato `v1.1.3`, `v1.1.4`, etc. | Compila, prueba y crea una GitHub Release con los archivos adjuntos. |
| Un commit directo a `master` | El workflow esta configurado para no compilar commits directos a `master`. |

## Artefactos vs Releases

GitHub Actions usa dos conceptos parecidos pero distintos.

### Artefactos

Son archivos temporales generados por una ejecucion del workflow. Sirven para
probar o descargar una compilacion sin publicar una version oficial.

En este proyecto los artefactos se guardan durante 7 dias:

- `db_linux`
- `db_windows`
- `db_macos`

### Release

Una Release es una publicacion oficial del proyecto en GitHub. Solo se crea
cuando subes un tag que empieza con `v`, por ejemplo:

```bash
git tag v1.1.3
git push origin v1.1.3
```

La Release adjunta estos archivos:

- `DrumBurp-1.1.3.0-setup.exe`
- `DrumBurp`
- `DrumBurp-1.1.3-macOS-x64.zip`

El numero `1.1.3` cambia segun el contenido de `VERSION` o el tag publicado.

## Primer uso de GitHub Actions

### 1. Activar Actions en GitHub

En tu repositorio de GitHub:

1. Abre la pagina del repositorio.
2. Entra en **Actions**.
3. Si GitHub muestra un boton para activar workflows, aceptalo.

### 2. Dar permiso para crear Releases

El workflow ya incluye:

```yaml
permissions:
  contents: write
```

Eso permite que el token automatico de GitHub pueda crear Releases y subir
archivos. Si aun asi falla con error 403, revisa en GitHub:

1. **Settings**
2. **Actions**
3. **General**
4. **Workflow permissions**
5. Selecciona **Read and write permissions**
6. Guarda los cambios

### 3. Probar primero con una rama

Antes de crear una Release oficial, conviene probar que todo compile en una rama
normal:

```bash
git push origin dev
```

Luego abre:

```text
https://github.com/TU_USUARIO/DrumBurp/actions
```

Haz clic en la ejecucion nueva y revisa que los jobs terminen en verde.

## Publicar una Release

### 1. Actualizar la version

La version debe coincidir en estos archivos:

- `VERSION`
- `src/DBVersionNum.py`
- `build/DrumBurp.nsi`
- `.versionflow`

La forma preferida es usar `versionflow` desde un entorno de desarrollo donde
este instalado:

```bash
pip install -r requirements-dev.txt
```

Si actualizas manualmente, verifica que todos los archivos queden con el mismo
numero.

### 2. Confirmar los cambios

Ejemplo:

```bash
git add VERSION src/DBVersionNum.py build/DrumBurp.nsi .versionflow
git commit -m "Bump version to 1.1.4"
```

### 3. Crear el tag

El tag debe empezar con `v`:

```bash
git tag v1.1.4
```

### 4. Subir la rama y el tag

```bash
git push origin dev
git push origin v1.1.4
```

Cuando subes el tag, GitHub Actions compila Linux, Windows y macOS. Si las
pruebas pasan, crea la Release y adjunta los ejecutables.

## Que hace cada job

### `build_linux`

Se ejecuta en `ubuntu-latest`.

1. Descarga el codigo.
2. Instala Python 3.11.
3. Instala herramientas de Qt necesarias para compilar traducciones.
4. Instala dependencias Python desde `build/requirements-linux.txt`.
5. Compila traducciones `.qm`.
6. Ejecuta las pruebas unitarias.
7. Ejecuta `build/build_linux.sh`.
8. Sube el binario `build/dist/DrumBurp` como artefacto `db_linux`.

### `test_linux`

Descarga `db_linux` y ejecuta:

```bash
DrumBurp --smoke-test
```

Esto comprueba que el binario arranca lo suficiente como para importar sus
modulos principales.

### `build_windows`

Se ejecuta en `windows-latest`.

1. Descarga el codigo.
2. Instala Python 3.11 x64.
3. Instala NSIS.
4. Instala dependencias Python desde `build/requirements-windows.txt`.
5. Compila traducciones `.qm`.
6. Ejecuta `build/build_windows.ps1`.
7. Sube el instalador como artefacto `db_windows`.

### `test_windows`

Descarga el instalador, lo instala silenciosamente y ejecuta:

```cmd
DrumBurp.exe --smoke-test
```

### `build_macos`

Se ejecuta en `macos-15-intel`.

1. Descarga el codigo.
2. Instala Python 3.11 x64.
3. Instala `qt` con Homebrew para disponer de `lrelease`.
4. Instala dependencias Python desde `build/requirements-macos.txt`.
5. Compila traducciones `.qm`.
6. Ejecuta las pruebas unitarias.
7. Ejecuta `build/build_macos.sh`.
8. Sube `DrumBurp-VERSION-macOS-x64.zip` como artefacto `db_macos`.

### `test_macos`

Descarga el `.zip`, lo descomprime y ejecuta:

```bash
DrumBurp.app/Contents/MacOS/DrumBurp --smoke-test
```

### `release`

Solo se ejecuta cuando el push es un tag que empieza con `v`.

Descarga los tres artefactos y crea una Release con:

- el instalador Windows
- el binario Linux
- el `.zip` de macOS

## Limitaciones importantes

### macOS no esta firmado ni notarizado

El archivo `DrumBurp.app` generado por GitHub Actions no esta firmado con una
cuenta de Apple Developer y no esta notarizado por Apple.

Eso significa que macOS puede mostrar una advertencia de seguridad la primera
vez que el usuario intente abrirlo. Para una distribucion mas profesional en
macOS haria falta:

1. Una cuenta de Apple Developer.
2. Certificados de firma.
3. Guardar esos certificados como secretos de GitHub Actions.
4. Firmar la app.
5. Notarizarla con Apple.

Eso no es necesario para comprobar que el build funciona, pero si es importante
si quieres distribuir una app macOS con menos advertencias para usuarios finales.

### El build macOS actual es x64

El workflow usa `macos-15-intel`, por eso genera una app para macOS Intel/x64.
En Macs Apple Silicon puede funcionar mediante Rosetta, pero no es un binario
ARM nativo.

Se puede agregar otro job para Apple Silicon en el futuro usando un runner ARM
de macOS y publicando otro zip, por ejemplo `macOS-arm64`.

### Linux no genera un `.deb`

El build Linux actual genera un binario autocontenido de PyInstaller. No crea un
paquete `.deb`, `.rpm`, AppImage ni Flatpak.

### Windows genera un instalador

Windows usa Nuitka para crear la aplicacion y NSIS para crear un instalador
`.exe`. Ese instalador crea accesos directos y desinstalador.

## Construir localmente

GitHub Actions es lo recomendado para releases, pero tambien puedes construir en
tu maquina.

### Linux

```bash
bash build/install_linux.sh
bash build/build_linux.sh
```

Salida esperada:

```text
build/dist/DrumBurp
```

### Windows

En PowerShell:

```powershell
.\build\install_windows.ps1
.\build\build_windows.ps1
```

Salida esperada:

```text
build\output\DrumBurp-X.Y.Z.0-setup.exe
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
bash build/install_macos.sh
bash build/build_macos.sh
```

Salida esperada:

```text
build/output/DrumBurp-X.Y.Z-macOS-x64.zip
```

## Solucion de problemas

### No aparece la pestaña Actions

Revisa que el repositorio este en GitHub y que exista el archivo:

```text
.github/workflows/build.yml
```

### El workflow no crea Release

Comprueba que empujaste un tag que empieza con `v`:

```bash
git tag -l
git push origin v1.1.4
```

### Error 403 al crear la Release

Revisa los permisos de Actions en **Settings -> Actions -> General -> Workflow
permissions** y usa **Read and write permissions**.

### Falla `lrelease`

`lrelease` compila las traducciones de Qt (`.ts` a `.qm`).

- En Linux se instala con `qttools5-dev-tools`.
- En macOS se instala con `brew install qt`.
- En Windows normalmente viene disponible en el entorno preparado por PyQt5/Qt;
  si falla, instala las herramientas de Qt o revisa que `lrelease.exe` este en
  el `PATH`.

### Falla PyInstaller

Revisa el log del job que fallo. PyInstaller suele fallar por una dependencia no
incluida, un archivo de datos faltante o un import oculto. Los scripts de
`build/` son el primer lugar donde ajustar esos detalles.

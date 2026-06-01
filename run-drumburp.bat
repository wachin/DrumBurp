@echo off
setlocal

set "ROOT=%~dp0"
cd /d "%ROOT%"
set "PYTHONPATH=%ROOT%src;%PYTHONPATH%"

if exist "%ROOT%.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%ROOT%.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_EXE=py -3"
    ) else (
        where python >nul 2>nul
        if errorlevel 1 (
            echo Python 3 was not found.
            echo.
            echo Install Python for Windows first, then install DrumBurp dependencies:
            echo py -m pip install PyQt5 PyQt5-sip pygame
            echo.
            pause
            exit /b 1
        )
        set "PYTHON_EXE=python"
    )
)

%PYTHON_EXE% "%ROOT%src\DrumBurp.py" %*
set "STATUS=%ERRORLEVEL%"

if not "%STATUS%"=="0" (
    echo.
    echo DrumBurp closed with error code %STATUS%.
    echo.
    echo Make sure the required Python packages are installed:
    echo py -m pip install PyQt5 PyQt5-sip pygame
    echo.
    pause
)

exit /b %STATUS%

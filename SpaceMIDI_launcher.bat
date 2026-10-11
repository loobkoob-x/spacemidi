@echo off
title SpaceMIDI Master Launcher
setlocal enabledelayedexpansion

:: Check if the local easyhid manual folder dependency is missing
if not exist easyhid (
    echo =======================================================
    echo          CRITICAL ACCESSIBILITY ERROR
    echo =======================================================
    echo [!] Local dependency directory 'easyhid' is missing.
    echo Opening target source repository for archive download...
    echo.
    echo ACTION REQUIRED: 
    echo 1. Download the ZIP file from the browser page.
    echo 2. Extract and place the 'easyhid' folder inside this folder layout.
    echo.
    start https://github.com
    pause
    exit
)

:: AUTOMATED BACKGROUND LAUNCH FOR LOOPMIDI
echo Checking loopMIDI background status...
tasklist /FI "IMAGENAME eq loopmidi.exe" 2>NUL | find /I /N "loopmidi.exe">NUL
if "%errorlevel%"=="1" (
    echo [!] loopMIDI is not running. Initiating auto-launch...
    
    :: Search standard installation paths for loopMIDI
    if exist "%ProgramFiles(x86)%\Tobias Erichsen\loopMIDI\loopmidi.exe" (
        start "" "%ProgramFiles(x86)%\Tobias Erichsen\loopMIDI\loopmidi.exe"
        timeout /t 2 >nul
    ) else if exist "%ProgramFiles%\Tobias Erichsen\loopMIDI\loopmidi.exe" (
        start "" "%ProgramFiles%\Tobias Erichsen\loopMIDI\loopmidi.exe"
        timeout /t 2 >nul
    ) else (
        echo [!] WARNING: loopMIDI.exe could not be located in standard paths.
        echo Please ensure loopMIDI is installed and open manually.
    )
) else (
    echo [^+] loopMIDI background engine verified active.
)

:: Determine if a first-time installation environment is required on this PC
if not exist venv (
    echo =======================================================
    echo          FIRST-TIME SYSTEM ENV SETUP DETECTED
    echo =======================================================
    
    :: Check if Python is installed on the computer system path
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo [!] WARNING: Python is not detected on this system.
        echo Opening the official download portal...
        echo CRITICAL: Ensure you check "Add python.exe to PATH" during setup.
        echo.
        start https://python.org
        pause
        goto start_venv_build
    )
    
    :start_venv_build
    echo [^+] Python Installation Detected.
    
    echo -------------------------------------------------------
    echo loopMIDI verification required. 
    echo If loopMIDI is not installed, press [Y] to fetch it.
    echo If it is already installed, press [N] to continue setup.
    echo -------------------------------------------------------
    set /p choice="Launch loopMIDI download portal? (Y/N): "
    if /i "!choice!"=="Y" (
        start https://tobias-erichsen.de
        echo.
        echo [!] Install loopMIDI, create a port named 'SpaceMIDI', then return here.
        pause
    )

    echo.
    echo Building clean environment matrix...
    py -3.13 -m venv venv
    
    echo Activating environment and fetching libraries...
    call venv\Scripts\activate
    pip install mido pygame keyboard cffi
    
    echo.
    if exist hidapi.dll (
        echo Injecting driver hooks...
        copy hidapi.dll venv\Scripts\ >nul
        echo [^+] Driver deployment successful.
    ) else (
        echo [!] CRITICAL ERROR: hidapi.dll missing from root directory.
        echo Opening libusb binary driver hub for download...
        echo.
        echo ACTION REQUIRED: Download 'hidapi-win.zip', extract 'x64/hidapi.dll',
        echo and drop it right into this main folder layout.
        start https://github.com
        pause
        exit
    )
    echo =======================================================
    echo            SETUP COMPLETE - INITIALISING APP
    echo =======================================================
    timeout /t 3 >nul
)

:: If the environment matrix is present, execute the controller interface instantly
cls
call venv\Scripts\activate
python spacemidi.py
pause

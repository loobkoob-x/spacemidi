@echo off
title SpaceMIDI Master Launcher
setlocal enabledelayedexpansion

:: 1. check easyhid dependency
if not exist easyhid (
    echo =======================================================
    echo          INSTALLING EASYHID LOCAL DEPENDENCY
    echo =======================================================
    echo [!] 'easyhid' folder is missing from the directory.
    echo Downloading from repository...
    echo.
    
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com' -OutFile 'easyhid.zip'"
    powershell -Command "Expand-Archive -Path 'easyhid.zip' -DestinationPath '.'"
    
    move python-easyhid-master\easyhid . >nul
    rmdir /s /q python-easyhid-master
    del easyhid.zip
    echo [^+] 'easyhid' installed.
    timeout /t 2 >nul
    cls
)

:: 2. check hidapi driver
if not exist hidapi.dll (
    echo =======================================================
    echo          INSTALLING HIDAPI WINDOWS DRIVER
    echo =======================================================
    echo [!] 'hidapi.dll' driver is missing from the directory.
    echo Downloading x64 binary from libusb release assets...
    echo.
    
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com' -OutFile 'hidapi_download.zip'"
    powershell -Command "Expand-Archive -Path 'hidapi_download.zip' -DestinationPath 'hidapi_extracted'"
    
    move hidapi_extracted\hidapi-win\x64\hidapi.dll . >nul
    rmdir /s /q hidapi_extracted
    del hidapi_download.zip
    echo [^+] 'hidapi.dll' driver installed.
    timeout /t 2 >nul
    cls
)

:: 3. check loopMIDI process status
echo Checking loopMIDI background status...
tasklist /FI "IMAGENAME eq loopmidi.exe" 2>NUL | find /I /N "loopmidi.exe">NUL
if "%errorlevel%"=="1" (
    echo [!] loopMIDI is not running. Initiating auto-launch...
    if exist "%ProgramFiles(x86)%\Tobias Erichsen\loopMIDI\loopmidi.exe" (
        start "" "%ProgramFiles(x86)%\Tobias Erichsen\loopMIDI\loopmidi.exe"
        timeout /t 2 >nul
    ) else if exist "%ProgramFiles%\Tobias Erichsen\loopMIDI\loopmidi.exe" (
        start "" "%ProgramFiles%\Tobias Erichsen\loopMIDI\loopmidi.exe"
        timeout /t 2 >nul
    ) else (
        echo [!] WARNING: loopMIDI.exe could not be located in standard paths.
        echo Opening download portal for manual installation setup...
        start https://tobias-erichsen.de/software/loopmidi.html
        pause
    )
) else (
    echo [^+] loopMIDI background engine verified active.
)

:: 4. check python virtual environment
if not exist venv (
    echo =======================================================
    echo          INITIALIZING PYTHON VIRTUAL ENVIRONMENT
    echo =======================================================
    
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
    echo Building clean environment matrix...
    py -3.13 -m venv venv
    
    echo Activating environment and fetching libraries...
    call venv\Scripts\activate
    pip install mido pygame keyboard cffi
    
    echo Injecting driver hooks into target environment execution path...
    copy hidapi.dll venv\Scripts\ >nul
    
    echo =======================================================
    echo            SETUP COMPLETE - INITIALISING APP
    echo =======================================================
    timeout /t 3 >nul
)

:: 5. start interface application
cls
call venv\Scripts\activate
python spacemidi.py
pause

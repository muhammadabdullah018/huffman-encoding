@echo off
echo ===========================================
echo      Huffman Project Build Script
echo ===========================================
echo.

echo [1/2] Checking for main.exe...
if exist main.exe (
    echo main.exe already exists. Skipping compilation.
) else (
    echo main.exe not found. Attempting to compile...
    
    where g++ >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo Found g++. Compiling...
        g++ main.cpp -o main.exe
    ) else (
        echo g++ not found.
        echo.
        echo CRITICAL: You must compile 'main.cpp' to 'main.exe' manually!
        echo If you have MinGW, add it to your PATH.
        echo If you have Visual Studio, run this script from the Developer Command Prompt.
        echo.
        pause
        exit /b 1
    )
)

if exist main.exe (
    echo.
    echo [2/2] Starting Web Interface...
    python app.py
) else (
    echo Compilation failed. main.exe was not created.
)

pause

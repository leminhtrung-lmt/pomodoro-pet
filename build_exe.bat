@echo off
cd /d "%~dp0"
set PY=python
where python >nul 2>nul || set PY=py
where %PY% >nul 2>nul
if errorlevel 1 (
  echo May nay chua co Python. Hay cai Python tu python.org roi chay lai file nay.
  start https://www.python.org/downloads/
  pause
  exit /b
)
%PY% -m pip install --upgrade pyinstaller
if errorlevel 1 goto failed
%PY% -m PyInstaller --onefile --windowed --name PomodoroPet pomodoro_pet.pyw
if errorlevel 1 goto failed
if not exist "dist\PomodoroPet.exe" goto failed
echo.
echo XONG! File PomodoroPet.exe nam trong thu muc "dist".
explorer dist
pause
exit /b 0

:failed
echo.
echo BUILD THAT BAI. Hay xem loi phia tren va thu lai.
pause
exit /b 1

@echo off
set "GIT_PATH=C:\Program Files (x86)\Git\cmd"

:: Проверяем, есть ли уже путь в PATH
echo %PATH% | find /I "%GIT_PATH%" >nul

if %errorlevel%==0 (
    echo Already in PATH.
) else (
    setx PATH "%PATH%;%GIT_PATH%" /M
)

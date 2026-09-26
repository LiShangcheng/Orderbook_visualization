@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 start_server.py
    goto :end
)

where python >nul 2>nul
if %errorlevel%==0 (
    python start_server.py
    goto :end
)

echo Python 3 was not found. Please install Python 3 and try again.
pause

:end

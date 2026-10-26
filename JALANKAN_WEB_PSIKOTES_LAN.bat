@echo off
cd /d "%~dp0"
set PSIKOTES_ADMIN_PIN=123456
"%LocalAppData%\Programs\Python\Python312\python.exe" app.py --host 0.0.0.0 --port 8000
if errorlevel 1 python app.py --host 0.0.0.0 --port 8000
pause


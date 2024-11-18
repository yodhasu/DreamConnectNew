@echo off
start open_serve.bat
call start_backend.bat
start chrome http://localhost:8000

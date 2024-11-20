@echo off
start open_serve.bat
call start_backend.bat
start msedge http://localhost:8000

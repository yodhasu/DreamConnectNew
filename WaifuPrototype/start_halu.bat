@echo off

call packagedownload.bat

cd ./Backend

start "" python backflask.py
cls
npm start
pause
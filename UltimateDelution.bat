@echo off

:: Step 1: Activate virtual environment
call venv\Scripts\activate

:: Step 2: Navigate to chatbot directory and start its script
cd ./chatbot/
start "" cmd /c start.bat

:: Step 3: Navigate to pixi_live2d_project directory and start its script
cd ..
cd ./pixi_live2d_project/
start "" cmd /c start_halu.bat

:: Step 4: Pause the script to prevent the window from closing
pause

@echo off
setlocal enabledelayedexpansion

echo Setting up your Python environment with pipenv...

:: Step 1: Set Python command explicitly for Python 3.10
set PYTHON_COMMAND=python

:: Step 2: Check if Python command is pointing to Python 3.10
for /f "tokens=* delims=" %%p in ('%PYTHON_COMMAND% --version 2^>nul') do (
    echo %%p | findstr "3.10" >nul
    if errorlevel 1 (
        echo The command '%PYTHON_COMMAND%' is not pointing to Python 3.10.
        echo Please verify your Python installation or update the PYTHON_COMMAND variable.
        exit /b
    )
)

echo Using Python executable: %PYTHON_COMMAND%

:: Step 3: Install pipenv if it's not already installed
echo Installing pipenv...
python -m pip install --upgrade pip
python -m pip install pipenv

:: Step 4: Set environment variable to create venv inside the project folder
set PIPENV_VENV_IN_PROJECT=1

:: Step 5: Create and activate virtual environment using pipenv
echo Creating a virtual environment using pipenv in the project directory...
pipenv install

:: Step 6: Upgrade pip inside the pipenv environment
echo Upgrading pip inside pipenv environment...
pipenv run python -m pip install pip==23.0.1

:: Step 7: Install dependencies using pipenv
echo Installing dependencies...
for %%p in (
    flask
    flask-socketio
    flask-cors
    transformers
    nltk
    requests
    pygame
    keyboard
    python-dotenv
    speechrecognition
    ollama
    langchain
    langchain_ollama
    openai
    tensorflow
    tf-keras
    elevenlabs
    coqui-tts
    tqdm
    urlextract
    gensim
    jokeapi
    omegaconf==2.0.6
    rvc-python
    numpy==1.26.0
) do (
    echo Installing %%p...
    pipenv install %%p
)

:: Step 8: Install torch and torchaudio with CUDA support
echo Installing torch and torchaudio with CUDA support...
pipenv install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo Setup complete! To activate the virtual environment, run "pipenv shell".
echo To run your programs, use "pipenv run python main.py" or "pipenv run python backflask.py".
pause

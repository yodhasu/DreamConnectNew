@echo off
setlocal enabledelayedexpansion

echo Setting up your Python environment...

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

:: Step 3: Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    %PYTHON_COMMAND% -m venv venv
) else (
    echo Virtual environment already exists. Skipping creation.
)

:: Step 4: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Step 5: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Step 6: Define and install dependencies
echo Installing dependencies...
(
    echo flask
    echo flask-socketio
    echo flask-cors
    echo transformers
    echo nltk
    echo requests
    echo pygame
    echo keyboard
    echo python-dotenv
    echo speechrecognition
    echo ollama
    echo langchain
    echo langchain_ollama
    echo g4f
    echo openai
    echo tensorflow
    echo tf-keras
    echo elevenlabs
    echo coqui-tts
    echo tqdm
    echo urlextract
    echo gensim
) > temp_requirements.txt

:: Step 7: Install packages except torch and torchaudio
for /f "delims=" %%p in (temp_requirements.txt) do (
    echo Checking package: %%p
    python -c "import %%p" 2>nul
    if errorlevel 1 (
        echo Package %%p not found. Installing...
        pip install %%p
    ) else (
        echo Package %%p is already installed. Skipping...
    )
)

:: Step 8: Install torch and torchaudio with CUDA support
echo Installing torch and torchaudio with CUDA support...
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html

:: Remove the temporary file
del temp_requirements.txt

:: Step 9: Install NLTK data
echo Downloading NLTK data...
python -m nltk.downloader punkt

echo Setup complete! To activate the virtual environment, run "venv\Scripts\activate".
echo To run your programs, use "python main.py" or "python backflask.py".
pause

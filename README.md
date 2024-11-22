
# DreamConnect

DreamConnect is a project by **Sigmalogy** that allows users to connect with their own personalized waifu. Choose to interact with your waifu using either **GPT-4** (if you have an API key) or **Ollama** for a customizable experience.

## Authors

- [@yodhasu](https://github.com/yodhasu)
- Add later...

## Features

- Live2D character viewer
- Customized chatbot with interactive AI personality
- Voice cloning and text-to-speech (TTS) support (using ElevenLabs; local TTS in development)
- And more features to come!

## Requirements

To run DreamConnect locally, you'll need the following:

- **Python 3.10** (make sure it's installed correctly)
- **Ollama** (for chat model integration)
- **Models** (e.g., `llama3`, `gpt2`, etc.) if you're using Ollama
- **CUDA-enabled GPU** (optional, for improved performance)
  
### Checking Python Version

If you have multiple Python versions installed, use the following commands to check your Python version:

```bash
python --version
```

or

```bash
py --version
```

In some cases, `python` might refer to a different version (e.g., Python 3.10), while `py` could point to a newer version (e.g., Python 3.12). Adjust the `install-all.bat` file to match your Python version:

```bash
set PYTHON_COMMAND=python
```

Change `python` to `py` if necessary, based on the version shown by `py --version`.

---

## Installation

### 1. Clone the Project

Clone the repository to your local machine using Git:

```bash
git clone https://github.com/yodhasu/DreamConnect.git
```

### 2. Go to the Project Directory

Navigate into the project folder:

```bash
cd DreamConnect
```

### 3. Run the Setup Script

Run the setup script (`install-all.bat`) to install dependencies and set up the environment:

```bash
install-all.bat
```

This script will ensure that the required dependencies are installed and ready for use. You can modify the `setup.bat` script if needed, particularly the Python command (`set PYTHON_COMMAND=python`) to match your system configuration.

### 4. Start the Program

Run the setup script (`UltimateDelution.bat`) to start:

```bash
UltimateDelution.bat
```
---

## Add and Change Live2D Models

1. **Navigate to the Models Directory**:

```bash
cd DreamConnect/pixi_live2d_project/models
```

2. **Add Your Model**:
   - Add your desired Live2D model files to the `models` directory.

3. **Update the Model Directory in the Code**:
   - Go to the `DreamConnect/pixi_live2d_project/js` directory.
   - Modify the `modeldir` variable in the JavaScript code to point to your newly added model directory:

```javascript
const modeldir = "your_model_directory";
```
## Chat Guide

In DreamConnect, special characters are used to mark **conditions**, **situations**, and **actions** in dialogues. Here’s a quick guide to help you navigate the chat:

- **Asterisk (`*`)**: Marks a special condition, situation, or action in the dialogue.
- Use `*emotion*`, `*action*`, or `*situation detail*` to make your conversations more dynamic.

### Examples:

- **User specifies emotion:**

```bash
User: *angry* Why did you do that?!
Character: *angry* I didn't mean to upset you. I'm sorry.
```

- **User specifies action:**

```bash
User: *gives a gift* I got this for you!
Character: *surprised* Oh, thank you! It's beautiful!
```

- **User adds context with situation:**

```bash
User: *sitting by the window* It's such a lovely evening.
Character: *looking out the window* I agree, the sunset is beautiful tonight.
```

---
## TTS Interaction
Currently, DreamConnect utilizes ElevenLabs for Text-to-Speech (TTS) functionality. While the TTS code isn't directly integrated into the main script, we've created a custom elevenlabs library that is already imported and utilized in the main chatbot.

How to Use TTS
To interact with the TTS system, the ElevenLabs functionality is encapsulated in the `chatbot/voiceCloner/elevenlabs.py` file. This module contains all necessary functions for text-to-speech conversion.

If you'd like to explore or modify the TTS functionality, you can find the relevant code and functions in this file.
Feel free to contribute and make improvements to the project. Enjoy your journey with your waifu!

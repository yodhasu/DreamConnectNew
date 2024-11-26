
# DreamConnect

**DreamConnect** is an interactive platform by **Sigmalogy** that lets you connect with your own personalized waifu. Choose between **GPT-4** (via OpenAI API) or **Ollama** for a custom chatbot experience. DreamConnect includes features such as a Live2D character viewer, customizable AI personalities, and more!

## Authors

- [@yodhasu](https://github.com/yodhasu)
- [@Shearenity](https://github.com/Shearenity)

## Features

- **Live2D character viewer**: Immerse yourself in a 3D virtual environment with interactive characters.
- **AI Personality Chatbot**: Enjoy conversations with a customizable AI character based on your preferences.
- **Voice Cloning & Text-to-Speech (TTS)**: Communicate using synthesized voices (currently in maintenance).
- **More to Come**: New features are continuously added to enhance your experience.

## Requirements

To run **DreamConnect** locally, make sure you have the following:

- **Python 3.10+** (Ensure it's properly installed)
- **API Key** (Required for Groq or OpenAI integration)
- **Ollama** (For chat model integration with models like `llama3`, `gpt2`, etc.)
- **CUDA-enabled GPU** (Optional, for improved performance with large models)

### Checking Python Version

Run the following command to check your Python version:

```bash
python --version
```

Or, if you use multiple Python versions:

```bash
py --version
```

If needed, adjust the `install-all.bat` script to match your Python version:

```bash
set PYTHON_COMMAND=python
```

Modify this to `py` if the output of `py --version` matches the Python version you're using.

---

## Installation

Follow these steps to set up **DreamConnect** on your local machine:

### 1. Clone the Repository

Clone the project to your local machine using Git:

```bash
git clone https://github.com/yodhasu/DreamConnect.git
```

### 2. Navigate to the Project Directory

Change to the project folder:

```bash
cd DreamConnect
```

### 3. Run the Setup Script

Execute the `install-all.bat` script to install dependencies:

```bash
install-all.bat
```

This script will automatically set up the necessary environment for you. If needed, adjust the Python command in the script to match your system configuration.

---

## Adding and Changing Live2D Models

### Prerequisite: Install Electron

Ensure **Electron** is installed to manage Live2D models.

### Steps:

1. **Navigate to the Models Directory**:

   ```bash
   cd DreamConnect/live2dviewer-build/models
   ```

2. **Add Your Model**:

   Place your desired Live2D model files (e.g., `model3.json`) into the `models` directory.

3. **Update the Model Directory in Code**:

   - Go to the `DreamConnect/live2dviewer-build/js` directory.
   - Update the `modeldir` variable in the `js` code to point to your new model directory:

   ```javascript
   const modeldir = "path_to_your_model_directory";
   ```

4. **Build the Electron App**:

   In the `live2dviewer-build` folder, run:

   ```bash
   npm start
   ```

   This will launch a local server to test if the model works. Once confirmed, build the final app:

   ```bash
   npm run build
   ```

5. **Final Steps**:

   - Navigate to the `dist` folder inside the build directory.
   - Rename the `.exe` if desired and move it into the `live2dviewer` folder.

---

## Chat Guide

DreamConnect uses special characters to handle **conditions**, **emotions**, and **actions** in conversations. Here's how to use them:

- **Asterisk (`*`)**: Indicates special conditions or actions in the dialogue.
  - Example: `*angry*` to set the character's emotion.
  - Example: `*gives a gift*` for a specific action.

### Example Interactions:

- **User specifies emotion**:

```bash
User: *angry* Why did you do that?!
Character: *apologetic* I'm really sorry, I didn't mean to upset you.
```

- **User specifies an action**:

```bash
User: *gives a gift* I got this for you!
Character: *surprised* Wow, thank you so much! It's beautiful!
```

- **User adds context to the situation**:

```bash
User: *sitting by the window* It's such a peaceful evening.
Character: *gazing outside* The stars are so bright tonight, aren't they?
```

---

## Text-to-Speech (TTS) Interaction

DreamConnect uses **ElevenLabs** for Text-to-Speech (TTS) functionality. The TTS integration is handled in the `chatbot/voiceCloner/elevenlabs.py` module.

### How to Use TTS:

1. **Locate the ElevenLabs TTS Functions**: The relevant code for TTS functionality is within the `elevenlabs.py` file.
2. **TTS Integration**: This module can be used to convert text to speech, allowing your waifu to speak back to you.

Feel free to contribute by exploring or improving the TTS features as part of the project!

---

## Contributing

We welcome contributions to improve **DreamConnect**! If you have suggestions, bug fixes, or new features, feel free to fork the project and submit a pull request.

---

**Enjoy your personalized waifu experience with DreamConnect!** 🎉

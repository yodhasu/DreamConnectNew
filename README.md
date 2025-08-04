
# DreamConnect

**DreamConnect** is an interactive platform by **Sigmalogy** that lets you connect with your own personalized waifu. Choose between **GPT-4** (via OpenAI API) or **Ollama** for a custom chatbot experience. DreamConnect includes features such as a Live2D character viewer, customizable AI personalities, and more!

# Beta showcase of the product
[![DreamConnect early version showcase](https://media.licdn.com/dms/image/sync/v2/D5627AQHa-X4ajfybNw/articleshare-shrink_800/B56ZY1WdZCHQAM-/0/1744651802706?e=1754906400&v=beta&t=JfoNqILlp2PjDIFiVvVu6YP0-QXRf2nyA70Qwm8egxs)](https://www.youtube.com/watch?v=MSv4Ru_MNN8)

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
---

## Installation

Follow these steps to set up **DreamConnect** on your local machine:

### 1. Clone the Repository

Clone the project to your local machine using Git:

```bash
git clone https://github.com/yodhasu/DreamConnectNew.git
```

### 2. Navigate to the Project Directory

Change to the project folder:

```bash
cd DreamConnectNew
```

### 3. Set Up Virtual Environment with Pipenv

Ensure Pipenv is installed, then install dependencies:

```bash
pip install pipenv  # Install Pipenv if not already installed
pipenv install      # Install dependencies inside a virtual environment
```
To activate the virtual environment, use:

```bash
pipenv shell
```

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

DreamConnect uses Microsoft Edge TTS for Text-to-Speech (TTS) functionality. The TTS integration is handled in the `SimpleTTS` class within `chatbot/voiceCloner/tts.py`.  

### How It Works  

1. **Language Detection**:  
   - The system detects the language of the input text using `langdetect`.  
   - Supported voices include:  
     - English (US) → en-US-MichelleNeural  
     - Spanish (Spain) → es-ES-ElviraNeural  
     - French (France) → fr-FR-DeniseNeural  
     - German (Germany) → de-DE-KatjaNeural  
     - Japanese → ja-JP-NanamiNeural  
     - Chinese (Simplified) → zh-CN-XiaoxiaoNeural  
   - If the language is not supported, the system defaults to English (US).  

2. **Generating Speech**:  
   - The input text is converted into speech using `edge_tts`.  
   - The output is saved as a `.wav` file.  

3. **Playing the Audio**:  
   - The system converts the audio to PCM format using `pydub` for better compatibility.  
   - The generated voice is played using `pygame`.  
   - The system waits until the audio finishes playing before unloading the file.  

### Example Usage  

from chatbot.voiceCloner.tts import SimpleTTS  
import asyncio  

tts = SimpleTTS()  
asyncio.run(tts.createTTS("Hello, how are you?"))  

This will generate speech in English and play it automatically.

---

## Contributing

We welcome contributions to improve **DreamConnect**! If you have suggestions, bug fixes, or new features, feel free to fork the project and submit a pull request.

---

**Enjoy your personalized waifu experience with DreamConnect!** 🎉

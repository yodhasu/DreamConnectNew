
# DreamConnect

DreamConnect is a project from Sigmalogy that allows everyone to finally connect with their own waifu.
We are planning to use OpenAI GPT-4 in the future but for now we use a library called [g4f](https://github.com/techwithanirudh/g4f)


## Authors

- [@yodhasu](https://github.com/yodhasu)
- Add later


## Features

- Live2D viewer
- Customized character chatbot
- voice clone and tts (in development)
- Idk, add later.


## Run Locally
To run this you need Python 3.10 and CUDA GPU (optional)

Clone the project.

```bash
  git clone https://github.com/yodhasu/DreamConnect.git
```

Go to the project directory.

```bash
  cd DreamConnect
```

Run the .bat file.

```bash
  UltimateDelution
```

I think I haven't make any version control, etc. If there's some python package u need just install it la
## Add and Change Live2D models

Go to the live2D model directory.

```bash
  cd DreamConnect/pixi_live2d_project/models
```
Add your desired model there.

To use/change the model got to DreamConnect/pixi_live2d_project/js and modify the model directory

```javascript
const modeldir = "your_model_dirrectory";
```

## Customize Character
To customize the Character simply just playaround with the chatbot's prompt and parameters

## Chat Guide

Asterisk (*) are used to mark condition, situation, action, basically for narrative function. Use it for better experience

```bash
  User: *emotion* Dialogue
  Character: *emotion* Dialogue
```

```bash
  User: *action* Dialogue
  Character: *action* Dialogue
```

```bash
  User: *situation detail* Dialogue
  Character: *situation detail* Dialogue
```

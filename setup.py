from setuptools import setup, find_packages

setup(
    name="InteractiveChatApp",
    version="1.0.0",
    description="An interactive chatbot with emotion classification and backend Flask integration",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "transformers",
        "nltk",
        "openai",
        "python-dotenv",
        "speechrecognition",
        "keyboard",
        "pygame",
        "requests",
        "flask",
        "flask-socketio",
        "flask-cors",
        "langchain",
        "g4f",  # Update or verify compatibility for your environment
        "tensorflow>=2.10.0",
        "torch>=2.0.0+cu118; platform_system=='Windows'",  # Adjust CUDA version based on your system
        "torchaudio>=2.0.0+cu118; platform_system=='Windows'",
        "elevenlabs",
        "coqui-tts",
    ],
    entry_points={
        "console_scripts": [
            "start_chat=main:interactive_chat",
            "start_server=backflask:app.run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.10",
)

from setuptools import setup, find_packages

setup(
    name="chatbot-cli",
    version="0.5",
    py_modules=["main"],
    install_requires=[
        "typer",
        "langchain-ollama",
        "transformers",
        "scikit-learn",
        "pandas",
        "flask",
        "g4f",
        "keyboard",
        "coqui-tts",
        "tensorflow" # Add other dependencies here
    ],
    python_requires="==3.10.*",
    # entry_points={
    #     "console_scripts": [
    #         "roleplay=main:app",  # 'roleplay' will be the command name
    #     ],
    # },
)

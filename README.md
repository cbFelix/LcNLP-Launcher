# LcNLP Launcher

**LcNLP Launcher** (Local Natural Language Processing Launcher) is a powerful and intuitive tool designed for managing, configuring, and launching various NLP models locally. This launcher simplifies the process of working with state-of-the-art text generation models, making it accessible for both beginners and advanced users.

## Description

LcNLP Launcher provides a user-friendly interface for setting up and running NLP models such as gpt2, gpt2-XL, and more. With LcNLP Launcher, you can:

- Easily configure model parameters and settings.
- Launch and monitor NLP models locally.
- Manage multiple models and their configurations.
- View real-time logs and outputs.

## Features

- **GUI User Interface**: GUI powered by PySide6 for easy interaction and configuration.
- **Model Management**: Support for multiple NLP models.

## Changelogs

- Model Selection: Choose from various pre-trained models (GPT-2, GPT-2 Medium, GPT-2 Large, GPT-2 XL).
- Device Configuration: Run models on CPU or GPU.
- Text Generation: Generate text based on user prompts with adjustable parameters (max length, temperature, top-k, top-p, repetition penalty).
- Interactive Chat Interface: Dark-themed chat interface for real-time interaction with AI.
- Library and Model Management: Checks for and installs required libraries, offers model downloads from Hugging Face.
- Multithreading: Ensures responsive UI during text generation.

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux.
- **Python Version**: Python 3.8 or higher.
- **Hardware**: 
  - Minimum: 8 GB RAM, Dual-core CPU.
  - Recommended: 32 GB RAM, powerful CPU like AMD Ryzen 9 5950X, Intel Core i9-12900K , GPU for model acceleration (NVIDIA CUDA supported) like NVIDIA RTX 2080 TI and NVIDIA RTX 3070.

## Installation

1. **Clone the repository**:
   'git clone https://github.com/cbFelix/LcNLP-Launcher.git'

2. **Navigate to the project directory**:
   ```commandline
   cd LcNLP-Launcher
   ```

3. **Create a virtual environment**:
   ```commandline
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   - On Windows: 
     ```commandline
     venv\Scripts\activate
     ```
     - On macOS/Linux:
     ```commandline
     source venv/bin/activate
     ```

5. **Install the required packages**:
   ```commandline
   pip install -r requirements.txt
   ```

## Usage

**Run the "app.py" file**
```commandline
python app.py
```

## License

LcNLP Launcher is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For further inquiries, please contact us at onerun325@gmail.com

# LcNLP Launcher

**LcNLP Launcher** (Local Natural Language Processing Launcher) is a powerful and intuitive tool designed for managing, configuring, and launching various NLP models locally. This launcher simplifies the process of working with state-of-the-art text generation models, making it accessible for both beginners and advanced users.

---

## Description

LcNLP Launcher provides a user-friendly interface for setting up and running NLP models such as gpt2, gpt2-XL, and more. With LcNLP Launcher, you can:

- Easily configure model parameters and settings.
- Launch and monitor NLP models locally.
- Manage multiple models and their configurations.
- View real-time logs and outputs.

---

## Features

- **GUI User Interface**: GUI powered by PySide6 for easy interaction and configuration.
- **Model Management**: Support for multiple NLP models.
- **You can** use a specific processor, CPU/CUDA.
- **You can fine-tune the model generation parameters**: 
1. **Temperature:** Controls the creativity of the output. A low value (e.g. 0.2) makes the text more predictable and less diverse. A high value (e.g. 1.0 or higher) makes the text more diverse but less predictable.

2. **Top-k:** Limits the number of highest probabilities for the next word. If top_k = 50, the model will only select the next word from the 50 most likely options, making the text more diverse.

3. **Top-p (nucleus sampling):** Limits the selection of words by cumulative probability. For example, if top_p = 0.9, the model selects words until their cumulative probability reaches 90%, which balances between predictability and diversity.

4. **Repetition Penalty:** Penalizes repeated words. A value > 1.0 reduces the likelihood of re-selecting already used words, which reduces the likelihood of repetitions in the text. 

5. **Max Length:** Specifies the maximum number of tokens (words or characters) in the generated text. For example, if max_length = 50, the model will generate text until it reaches 50 tokens or encounters an ending token. This parameter helps control the length of the response, ensuring that it meets the specified limits. 

---

## Changelogs

## v1.1.0

---

### Creating a modal settings window (ConfigDialog):

- A new window for configuring text generation parameters (selecting a model, device, max_length, temperature, top_k, top_p, repetition_penalty) has been added.
- The window is called by the "Settings" button.
### Moving settings from the main window to the modal window:

- Text generation settings have been moved to ConfigDialog.
- Settings are called from the main ChatWindow window via a modal window.
### Saving parameters after closing the dialog:

- After closing the dialog, the settings are saved in the attributes of the ChatWindow object.
- Parameters are updated in the open_settings method of the main window.
### Simplifying the main interface:

- Removed QGridLayout with settings from the main window, leaving only the main elements (chat field, input field and send button).

---

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux.
- **Python Version**: Python 3.8 or higher.
- **Hardware**: 
  - Minimum: 8 GB RAM, CPU like Intel Core i5 and Ryzen 7 for models with up to 1 billion parameters.
  - Recommended: 32 GB RAM, powerful CPU like AMD Ryzen 7 3700k, Intel Core i7-8700 or GPU for model acceleration (NVIDIA CUDA supported) like NVIDIA RTX 1080 TI and NVIDIA RTX 2060 for models with up to 8 billion parameters.
  - Recommendations for large models: 64 GB RAM, powerful GPU like NVIDIA RTX 4090 or NVIDIA Quadro RTX 8000 for large models.

---

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
   
---

## Usage

**Run the "app.py" file**
```commandline
python app.py
```

---

## License

LcNLP Launcher is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contact

For further inquiries, please contact us at onerun325@gmail.com

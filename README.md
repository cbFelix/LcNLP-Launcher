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

## Preview

[review1](launcher/assets/preview/120/p1.png)

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

## v1.2.0

---

### Optimization:

- Now you can use the half-precision model to save RAM and time for generating an answer at the expense of the accuracy and quality of the result
### MInterface redesign:

- Completely redesigned UI and UX
### Button to clear chat:

- Added a button to clear chat history
---

## System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux.
- **Python Version**: Python 3.8 or higher.
- **Hardware**: 
  - Minimum: 8 GB RAM, Dual-core CPU.
  - Recommended: 32 GB RAM, powerful CPU like AMD Ryzen 9 5950X, Intel Core i9-12900K , GPU for model acceleration (NVIDIA CUDA supported) like NVIDIA RTX 2080 TI and NVIDIA RTX 3070.

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

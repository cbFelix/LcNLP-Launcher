from transformers import AutoTokenizer, AutoModelForCausalLM
from launcher.utils.devices.device_manager import DeviceManager
import torch

class AdvancedTextGenerator:
    def __init__(self, model_name='gpt2', device_id='cpu'):
        self.device_manager = DeviceManager()
        self.set_device(device_id)
        self.load_model(model_name)

    def set_device(self, device_id):
        self.device_manager.set_device(device_id)
        self.device = self.device_manager.get_device()

    def load_model(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def generate_text(self, prompt, max_length=50, temperature=1.0, top_k=50, top_p=0.95, repetition_penalty=1.0):
        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        input_ids = inputs['input_ids']
        attention_mask = inputs.get('attention_mask')

        outputs = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=max_length + len(input_ids[0]),
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            do_sample=True
        )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text



if __name__ == '__main__':
    # Initialize device manager and set device
    dm = DeviceManager()
    dm.print_available_devices()

    # Example device choice
    device_id = 'cpu'  # or 'cpu', 'cuda:1', etc.

    generator = AdvancedTextGenerator(model_name='gpt2-large', device_id=device_id)
    prompt = "What is quasar?"

    generated_text = generator.generate_text(
        prompt,
        max_length=100,  # Adjust as needed
        temperature=0.7,
        top_k=50,
        top_p=0.9,
        repetition_penalty=1.2
    )

    print(f"\nFinal Generated Text:\n{generated_text}")

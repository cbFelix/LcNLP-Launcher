import torch
import GPUtil
import psutil


class DeviceManager:
    def __init__(self):
        self.device = None
        self.available_devices = self._get_available_devices()

    def _get_available_devices(self):
        """
        Returns a list of available devices (GPUs) and CPU.
        """
        devices = []
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                devices.append(f'cuda:{i}')
        devices.append('cpu')
        return devices

    def set_device(self, device_id):
        """
        Set the device based on the provided device_id.

        :param device_id: ID of the device to use (e.g., 'cuda:0', 'cpu').
        """
        if device_id in self.available_devices:
            self.device = torch.device(device_id)
        else:
            raise ValueError(f"Device '{device_id}' is not available. Available devices: {self.available_devices}")

    def get_device(self):
        """
        Returns the currently set device.
        """
        return self.device

    def print_available_devices(self):
        """
        Print available devices.
        """
        print("Available devices:")
        for device in self.available_devices:
            print(f" - {device}")

    def get_device_info(self):
        """
        Print detailed information about the selected device.
        """
        if self.device is None:
            raise ValueError("No device selected. Use 'set_device' to select a device.")

        device_info = {}
        if self.device.type == 'cuda':
            device_id = int(self.device.index)
            device_properties = torch.cuda.get_device_properties(device_id)

            device_info['Device ID'] = device_id
            device_info['Device Name'] = device_properties.name
            device_info['Memory Allocated (MB)'] = torch.cuda.memory_allocated(device_id) / (1024 ** 2)
            device_info['Memory Cached (MB)'] = torch.cuda.memory_reserved(device_id) / (1024 ** 2)
            device_info['Total Memory (MB)'] = device_properties.total_memory / (1024 ** 2)
            device_info['Driver Version'] = device_properties.driver_version
            device_info['Compute Capability'] = f"{device_properties.major}.{device_properties.minor}"

            # Additional details from GPUtil
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                if gpu.id == device_id:
                    device_info['Manufacturer'] = gpu.name.split()[0]  # Extracting manufacturer from the name
                    device_info['Model'] = gpu.name  # Full model name
                    break
        else:
            # For CPU
            device_info['Device Name'] = 'CPU'
            device_info['CPU Cores'] = psutil.cpu_count(logical=False)
            device_info['CPU Threads'] = psutil.cpu_count(logical=True)
            device_info['CPU Frequency (MHz)'] = psutil.cpu_freq().current

        print("Device Information:")
        for key, value in device_info.items():
            print(f"{key}: {value}")


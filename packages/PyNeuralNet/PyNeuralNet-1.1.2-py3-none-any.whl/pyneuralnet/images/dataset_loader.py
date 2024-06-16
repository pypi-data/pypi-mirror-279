import os
import requests
from io import BytesIO
from PIL import Image
from torch.utils.data import Dataset


class DatasetLoader(Dataset):
    def __init__(self, metadata_file, root_dir, transform=None):
        with open(metadata_file, 'r') as file:
            self.image_paths = file.readlines()
        self.image_paths = [os.path.join(root_dir, path.strip()) for path in self.image_paths]
        self.transform = transform
        print(f"Loaded {len(self.image_paths)} images")
        print(f"Example path: {self.image_paths[0]}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"File not found: {img_path}")
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img

class DatasetLoaderfromInternet(Dataset):
    def __init__(self, metadata_url, root_url, transform=None):
        response = requests.get(metadata_url)
        self.image_paths = response.text.strip().split('\n')
        # Replace backslashes with forward slashes and ensure proper URL format
        self.image_paths = [root_url + path.strip().replace("\\", "/") for path in self.image_paths]
        self.transform = transform
        print(f"Loaded {len(self.image_paths)} images")
        print(f"Example URL: {self.image_paths[0]}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_url = self.image_paths[idx]
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img

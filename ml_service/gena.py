import torch
from transformers import CLIPTokenizer, CLIPTextModel
import json
import base64
from io import BytesIO
from torchvision.utils import make_grid
from torchvision.transforms.functional import to_pil_image
from torch import nn

class Generator(nn.Module):
    def __init__(self, noise_dim=100, text_dim=512, out_channels=3):
        super().__init__()
        self.projection = nn.Linear(text_dim, 256)
        self.fc = nn.Linear(noise_dim + 256, 512 * 4 * 4)

        self.net = nn.Sequential(
            nn.BatchNorm2d(512),
            nn.ConvTranspose2d(512, 256, 4, 2, 1),  # 8x8
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, 4, 2, 1),  # 16x16
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1),   # 32x32
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, out_channels, 4, 2, 1),  # 64x64
            nn.Tanh()
        )

    def forward(self, noise, text_emb):
        projected_text = self.projection(text_emb)
        x = torch.cat([noise, projected_text], dim=1)
        x = self.fc(x).view(-1, 512, 4, 4)
        return self.net(x)

class Gena:
    def __init__(self):
        self.tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
        self.text_encoder = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32")
        self.generator = Generator()

    def encode_text(self, captions):
        inputs = self.tokenizer(captions, padding=True, return_tensors="pt", truncation=True)
        with torch.no_grad():
            text_features = self.text_encoder(**inputs).last_hidden_state[:, 0, :]
        return text_features
    
    def to_base64(self, generated):
        base64_images = []

        for img_tensor in generated:
            img = to_pil_image(img_tensor.clamp(0, 1))  # тензор в [0,1] -> PIL
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            base64_images.append(img_str)

        return base64_images
    
    def generate_from_text(self, prompt, num_images=1):
        self.generator.load_state_dict(torch.load('./Generator_70.pt', map_location=torch.device('cpu')))
        self.generator.eval()
        with torch.no_grad():
            text_emb = self.encode_text([prompt]*num_images).to('cpu')
            noise = torch.randn(num_images, 100).to('cpu')
            generated = self.generator(noise, text_emb).cpu()
        
        generated = self.to_base64(generated)
        return generated
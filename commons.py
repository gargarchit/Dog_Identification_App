import io
import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms
def get_model():
	checkpoint_path = 'model_transfer.pt'
	model = models.resnet50(pretrained=True)
	model.fc = nn.Linear(2048, 133, bias=True)
	for param in model.parameters():
		param.requires_grad = False
	model.load_state_dict(torch.load(checkpoint_path, map_location='cpu'), strict=False)
	model.eval()
	return model

def get_tensor(image_bytes):
	my_transforms = transforms.Compose([transforms.Resize(224),
        								transforms.CenterCrop(224),
        								transforms.ToTensor(),
        								transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
	image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
	return my_transforms(image)[:3,:,:].unsqueeze(0)
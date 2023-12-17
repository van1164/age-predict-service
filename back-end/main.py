from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms
import torch
import timm
import torch.nn as nn
import torchvision
from sampleCNN import SampleCNN
from EnsembleModel import EnsembleModel
origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



model1 = SampleCNN()
model2=torchvision.models.resnet18(torchvision.models.ResNet18_Weights)
model2.fc = nn.Sequential(
    nn.Linear(512,512),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(512,70),
    nn.Softmax()
)

model = EnsembleModel(model1,model2,70)

@app.post("/upload")
async def upload_photo(file: UploadFile):
    image= await file.read()
    image = Image.open(BytesIO(image))
    
    # transform = transforms.Compose([
    #     transforms.Resize((256)),
    #     transforms.CenterCrop((224,224)),
    #     transforms.ToTensor(),
    #     #transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    # ])

    transform = transforms.Compose([
   transforms.Resize((128, 128)),
   #transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2, hue=0.2),
   transforms.ToTensor(),
])

    tensor_image = transform(image)
    print(tensor_image.shape)
    #model = timm.create_model("efficientvit_b0",pretrained=False, num_classes=70)

    #loaded_model = torch.load('face_model.pth', map_location=torch.device('cpu'))
    #loaded_model = torch.load('resnet18.pth', map_location=torch.device('cpu'))
    loaded_model = torch.load('ensamble.pth', map_location=torch.device('cpu'))
    model.load_state_dict(loaded_model)
    model.eval()
    #loaded_model.eval()
    print(model)

    output = model(tensor_image.unsqueeze(0))
    print(output.argmax(-1))
    return {"age":int(output.argmax(-1)) }
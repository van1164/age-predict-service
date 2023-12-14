from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import torchvision.transforms as transforms
import torch
import timm
origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_photo(file: UploadFile):
    image= await file.read()
    image = Image.open(BytesIO(image))
    
    # 이미지를 텐서로 변환합니다.
    transform = transforms.Compose([
        transforms.Resize((256)),
        transforms.CenterCrop((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    tensor_image = transform(image)
    print(tensor_image.shape)
    model = timm.create_model("efficientvit_b0",pretrained=False, num_classes=70)

    loaded_model = torch.load('face_model.pth', map_location=torch.device('cpu'))
    model.load_state_dict(loaded_model)
    #loaded_model.eval()
    print(model)

    output = model(tensor_image.unsqueeze(0))
    print(output.argmax(-1))
    return {"age":int(output.argmax(-1)) }
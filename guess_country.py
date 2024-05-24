import os
import csv
import torch
from torchvision.transforms import v2
from model import CNN
import sys
from PIL import Image
from config import NUM_CLASSES, WIDTH, HEIGTH

device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))


# Inference pipeline

# CHECK IF THERES TRAINED MODEL ALREADY
# model will always use the latest checkpoint
model_trained = True
checkpoints=[]
if os.path.exists("./checkpoints"):
    for file in os.listdir("./checkpoints"):
        checkpoints.append(file)

    if len(checkpoints)==0:
        model_trained=False
else:
    model_trained=False

if model_trained:
    model = CNN(NUM_CLASSES).to(device)
    checkpoints.sort()
    checkpoint = torch.load(f"./checkpoints/{checkpoints[-1]}")
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    print(f"Using model: {checkpoints[-1]}")

    # class_to_idx binds name to index, we want to flip it
    classes ={value:key for key, value in checkpoint['class_to_idx'].items()}

    preprocess = v2.Compose([
        v2.ToPILImage(),  # Convert to PIL Image first
        v2.ConvertImageDtype(torch.float32),  # Ensure the image is float32
        v2.Resize((WIDTH, HEIGTH)),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale=True),
    ])

    while True:
        input_image_path = input("Paste path to image or press 0 to quit: ")
        if input_image_path=="0":
            sys.exit()
        else:
            try:
                input_image = Image.open(input_image_path).convert("RGB").resize((WIDTH, HEIGTH))
                input_tensor = preprocess(input_image)
                input_batch = input_tensor.unsqueeze(0)

                input_batch = input_batch.to(device)

                with torch.no_grad():
                    output = model(input_batch)

                # Get the class with highest probability
                _, predicted_class = torch.max(output, 1)
                print(f"Predicted class: {classes[predicted_class.item()]}")
            except Exception as e:
                print(f"Error processing image: {e}")

else:
    print("No trained model found, you need to train a model first, use run_training.py script.")

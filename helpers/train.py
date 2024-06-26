import torch
import torch.optim as optim
import matplotlib.pyplot as plt
import torch.nn as nn
import wandb
import os
from datetime import datetime
from torchvision.transforms import v2
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from helpers.config import WIDTH, HEIGTH
from model import CNN

# Training hyperparameters
NUM_EPOCHS = 10
BATCH_SIZE = 32
LR = 1e-4

def run_training():
    # current date/time for wandb and checkpoint
    now  = datetime.now().strftime("%d_%m_%m_%H_%M_%S")

    #create checkpoint directory
    if not os.path.exists('./checkpoints'):
        os.makedirs('./checkpoints')

    # Model can be trained with CPU, CUDA or M series Apple gpu
    device = torch.device("cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu"))
    print(f"Training on: {device}")

    transforms = v2.Compose([
        v2.ToPILImage(),  # Convert to PIL Image first
        v2.ConvertImageDtype(torch.float32),  # Ensure the image is float32
        v2.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale=True),
    ])

    train_set = ImageFolder(root='./Data/Train', transform=transforms)
    test_set = ImageFolder(root='./Data/Test', transform=transforms)
    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=False)

    model = CNN(num_classes=len(train_set.classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR, weight_decay=1e-5)

    # wandb.init(
    #     # set the wandb project where this run will be logged
    #     project="flags-classification",
    #     # track hyperparameters and run metadata
    #     name = f"run_{now}",
    #     config = {
    #         "learning_rate": LR,
    #         "architecture": "CNN",
    #         "dataset": "Flags",
    #         "epochs": NUM_EPOCHS,
    #         "batch_size": BATCH_SIZE
    #     }
    # )

    # Training loop
    for epoch in range(NUM_EPOCHS):
        for batch_idx, (data, targets) in enumerate(train_loader):
            data = data.to(device)
            targets = targets.to(device)

            scores = model(data)
            loss = criterion(scores, targets)
            optimizer.zero_grad()
            loss.backward()

            optimizer.step()

            if batch_idx % 100 == 0:
                # wandb.log({"loss": loss.item()})
                print(f"Epoch {epoch+1}/{NUM_EPOCHS}, Batch:{batch_idx} loss: {loss.item()}")

    # Print model's state_dict
    print("Model's state_dict:")
    for param_tensor in model.state_dict():
        print(param_tensor, "\t", model.state_dict()[param_tensor].size())

    # Print optimizer's state_dict
    print("Optimizer's state_dict:")
    for var_name in optimizer.state_dict():
        print(var_name, "\t", optimizer.state_dict()[var_name])

    # Save model for later inference

    # Since this is a quite simple model we're only doing saving post-training, with the more complex model
    # we could be saving every x  epochs in the training loop
    torch.save(
        {
            'epoch': NUM_EPOCHS,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'class_to_idx': train_set.class_to_idx
        },
        f"./checkpoints/chckpt_{now}"
    )

    # Test loop
    model.eval()
    with torch.no_grad():
        correct = 0
        total = 0
        for data, targets in test_loader:
            data = data.to(device)
            targets = targets.to(device)

            scores = model(data)
            _, predictions = scores.max(1)
            correct += (predictions == targets).sum()
            total += predictions.size(0)
            accuracy = correct / total
            # wandb.log({"accuracy": accuracy})
        accuracy = correct / total
        print(f"Accuracy: {accuracy}")

if __name__ == "__main__":
    run_training()

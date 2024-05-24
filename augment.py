import os
import cv2
import numpy as np
import random
from config import HEIGTH, WIDTH

# Function to perform augmentation, resize, and save images
def augment_and_save(target_count=50, input_dir='./Flags', output_dir='./AugmentedFlagsResized', prefix=''):
    # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # List all subdirectories (each subdirectory is a class folder)
        classes = os.listdir(input_dir)

        for class_name in classes:
            class_dir = os.path.join(input_dir, class_name)
            if not os.path.isdir(class_dir):
                continue

            # List all files in the class directory
            files = os.listdir(class_dir)
            existing_count = len(files)  # Count existing images

            # Calculate how many augmentations are needed
            needed_count = max(0, target_count - existing_count)

            for file in files:
                # Read the image
                img_path = os.path.join(class_dir, file)
                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

                # Perform augmentation
                for i in range(needed_count):
                    augmented_img = augment_image(img)

                    # Resize augmented image
                    resized_img = cv2.resize(augmented_img, (WIDTH, HEIGTH))

                    # Construct new file name
                    new_filename = f"{prefix}{i + 1}.jpg"
                    # Save resized and augmented image to output directory
                    output_class_dir = os.path.join(output_dir, class_name)
                    os.makedirs(output_class_dir, exist_ok=True)
                    cv2.imwrite(os.path.join(output_class_dir, new_filename), cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))  # Convert RGB to BGR for saving

def augment_image(img):
    # Initialize augmented image as the original image
    augmented_img = img.copy()

    # Randomly select augmentations to apply
    # augmentations = ['flip_horizontal', 'flip_vertical', 'brightness', 'contrast', 'rotate']
    augmentations = ['brightness', 'rotate']
    for augmentation in augmentations:
        if augmentation == 'flip_horizontal' and random.random() > 0.5:
            augmented_img = cv2.flip(augmented_img, 1)  # Flip horizontally (50% chance)

        elif augmentation == 'flip_vertical' and random.random() > 0.5:
            augmented_img = cv2.flip(augmented_img, 0)  # Flip vertically (50% chance)

        elif augmentation == 'brightness':
            # Change brightness (factor randomly chosen between 0.5 and 1.5)
            brightness_factor = random.uniform(0.8, 1.2)
            augmented_img = cv2.convertScaleAbs(augmented_img, alpha=brightness_factor, beta=0)

        elif augmentation == 'contrast':
            # Change contrast (factor randomly chosen between 0.7 and 1.5)
            contrast_factor = random.uniform(0.8, 1.2)
            mean_value = np.mean(augmented_img)
            augmented_img = cv2.convertScaleAbs(augmented_img, alpha=contrast_factor, beta=-contrast_factor * mean_value)

        elif augmentation == 'rotate':
            # Rotate the image (angle randomly chosen between -10 and 10 degrees)
            angle = random.randint(-10, 10)
            height, width = augmented_img.shape[:2]
            rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
            augmented_img = cv2.warpAffine(augmented_img, rotation_matrix, (width, height))

    return augmented_img

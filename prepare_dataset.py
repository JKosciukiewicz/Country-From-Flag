from config import HEIGTH, WIDTH
from scrap_data import get_flags
from augment import augment_and_save
import os
import shutil
from sklearn.model_selection import train_test_split
import csv


def prepare_dataset():
    # Downloads flags and prepare dataset
    input_dir = './Data/Flags'
    train_dir = './Data/Train'
    test_dir = './Data/Test'

    #remove old dataset
    if os.path.exists('./Data'):
        shutil.rmtree('./Data')

    # Download images if necessary
    if not os.path.exists('./Flags'):
        print("Downloading images ...")
        get_flags(output_dir='./Flags')

    # Augment images
    print("Augmenting images ...")
    augment_and_save(target_count=50, input_dir='./Flags', output_dir='./Data/Flags', prefix='')

    # Create 80/10/10 test/train/val split
    print("Creating train/test/val split ...")
    # Create output directories if they don't exist

    # Define input and output directories
    input_dir = './Data/Flags'
    train_dir = './Data/Train'
    test_dir = './Data/Test'

    # Create output directories if they don't exist
    # Create output directories if they don't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # List to hold CSV data
    csv_data = []
    country_indices = {}
    # Traverse each country directory
    for idx, country in enumerate(os.listdir(input_dir)):
        country_path = os.path.join(input_dir, country)
        if os.path.isdir(country_path):
            # Create corresponding train/test country directories
            train_country_dir = os.path.join(train_dir, country)
            test_country_dir = os.path.join(test_dir, country)
            os.makedirs(train_country_dir, exist_ok=True)
            os.makedirs(test_country_dir, exist_ok=True)

            # List all files in the country directory
            all_files = [f for f in os.listdir(country_path) if os.path.isfile(os.path.join(country_path, f))]

            # Split the files into train and test sets
            train_files, test_files = train_test_split(all_files, test_size=0.2, random_state=42)

            country_indices[idx] = country

            # Function to copy files to their respective directories and collect CSV data
            def copy_files_and_collect_csv_data(files, source_dir, destination_dir, split):
                for file in files:
                    shutil.copy(os.path.join(source_dir, file), os.path.join(destination_dir, file))
                    csv_data.append([country, file, split])

            # Copy train and test files to their respective directories and collect CSV data
            copy_files_and_collect_csv_data(train_files, country_path, train_country_dir, 'train')
            copy_files_and_collect_csv_data(test_files, country_path, test_country_dir, 'test')


    # Write CSV data to file
    csv_file_path = './Data/split_data.csv'
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['class', 'img', 'split'])  # Write header
        csv_writer.writerows(csv_data)

    print("Dataset complete")

if __name__ == "__main__":
    prepare_dataset()

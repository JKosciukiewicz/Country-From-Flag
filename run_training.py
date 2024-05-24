import os
import csv

from train import run_training
from prepare_dataset import prepare_dataset

def verify_datset():
    print("Checking dataset...")
    dataset_valid = True
    if os.path.exists('./Data/Train') and os.path.exists('./Data/Test') and os.path.isfile("./Data/split_data.csv"):
        with open('./Data/split_data.csv', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None) # skip headers
            for row in csv_reader:
                filename=f"{row[2].capitalize()}/{row[0]}/{row[1]}"
                if not os.path.exists(f"./Data/{filename}"):
                    dataset_valid = False
                    break
    else:
        dataset_valid = False

    return dataset_valid

if __name__ == "__main__":
    datset_valid = verify_datset()
    if datset_valid:
        print("Dataset valid and verified, starting training ...")
        run_training()
    else:
        print("Dataset invalid or missing, preparing dataset ...")
        prepare_dataset()
        datset_valid = verify_datset()
        if datset_valid:
            print("Dataset valid and verified, starting training ...")
            run_training()
            print("Model has been trained, use guess_country.py for inference")
        else:
            print("Something went very wrong, clean the directory and run this script again")

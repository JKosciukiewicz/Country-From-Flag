import requests
import re
import csv
from bs4 import BeautifulSoup
import shutil
import os


# This file contains methods used to gathering data to prepare the dataset
# Scrapeper is only onfigured for specific wikipedia page

URL ='https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags'
IMAGE_DIR='./Flags'
DRY_RUN=False # DRY_RUN=TRUE won't download data, only create folders and csv files

def parse_img_url(scrcset: str):
    pattern = re.compile(r'upload\.wikimedia\.org/.*?\.png')
    urls = scrcset.split(',')
    links=[]
    for url in urls:
        links.append(pattern.search(url).group())
    return links

def scrap_images():
    # get html and
    page = requests.get(URL)
    parsed = BeautifulSoup(page.content, "html.parser")

    # images are grouped in galleries
    galleries = parsed.find_all("ul", {"class":"gallery"})

    # get all images from each gallery
    image_links={}
    for gallery in galleries:
        images = gallery.find_all("img", {"class":"mw-file-element"})
        for img in images:
            # get class name
            alt = img.attrs.get('alt')
            # get image urls
            urls = parse_img_url(img.attrs.get('srcset'))
            #only get the highest resolution image (last one)
            image_links[alt]=urls[-1]
    return image_links

def download_images(image_links: dict):
    # Create target directory if necessary
    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)
    # Create csv file
    # csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Download images
    for country, flag_url in image_links.items():
        country=country.replace(" ","_")
        print(country, flag_url)
        # Add image to CSV (country, ./Flags/Country/001.jpg)
        # csv_writer.writerow([country, IMAGE_DIR+'/'+country+'/001.jpg'])
        # Create directory if necessary
        if not os.path.exists(IMAGE_DIR+'/'+country):
            os.makedirs(IMAGE_DIR+'/'+country)
        else:
            shutil.rmtree(IMAGE_DIR+'/'+country)
            os.makedirs(IMAGE_DIR+'/'+country)
        if not DRY_RUN:
            img_download = requests.get("https://" + flag_url, stream = True)
            if img_download.status_code == 200:
                with open(IMAGE_DIR+'/'+country+'/001.jpg', 'wb') as f:
                    img_download.raw.decode_content = True
                    shutil.copyfileobj(img_download.raw, f)
            else:
                print('Failed to download:', country, flag_url)


    # Verify if all images are saved (compare directory vs CSV)
def get_flags():
    image_links = scrap_images()
    download_images(image_links)

get_flags()

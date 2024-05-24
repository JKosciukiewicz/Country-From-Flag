import requests
import re
import csv
from bs4 import BeautifulSoup
import shutil
import os
import time

# This file contains methods used to gathering data to prepare the dataset
# Scrapeper is only onfigured for specific wikipedia page

URL ='https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags'
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

def download_images(image_links: dict, output_dir: str):
    # Create target directory if necessary
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download images
    missing_images = {}
    for country, flag_url in image_links.items():
        country=country.replace(" ","_")
        # Create directory if necessary
        if not os.path.exists(output_dir+'/'+country):
            os.makedirs(output_dir+'/'+country)
        else:
            shutil.rmtree(output_dir+'/'+country)
            os.makedirs(output_dir+'/'+country)
        if not DRY_RUN:
            img_download = requests.get("https://" + flag_url, stream = True)
            if img_download.status_code == 200:
                with open(output_dir+'/'+country+'/001.jpg', 'wb') as f:
                    img_download.raw.decode_content = True
                    shutil.copyfileobj(img_download.raw, f)
            else:
                print(f"Error downloading image: {country}")
                missing_images[country]=flag_url

        # handle missing images
        if len(missing_images)>0:
            print("Retrying downloading missing images:")
            for country, url in missing_images.items():
                max_retries=3
                for retry in range(max_retries):
                    img_download = requests.get("https://" + url, stream = True)
                    if img_download.status_code == 200:
                        with open(output_dir+'/'+country+'/001.jpg', 'wb') as f:
                            img_download.raw.decode_content = True
                            shutil.copyfileobj(img_download.raw, f)
                            break
                    else:
                        # wait 1 second before retrying
                        time.sleep(1)
                        if retry == max_retries - 1:
                            print(f"Couldn't download image for: {country}, try adding it manually to the dataset from this URL: {url}")
                            break

def get_flags(output_dir):
    image_links = scrap_images()
    download_images(image_links, output_dir)

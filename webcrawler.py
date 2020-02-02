import argparse
import os
from parsel import Selector
import requests
import subprocess
import sys
from PIL import Image
import time

HEADER = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0"}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_arguments():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument('-s', help="Search key", type=str, required=True)
    parser.add_argument('-d', help="Folder to save images", type=str,
                        required=True)
    return parser.parse_args()

def save_image(name, link):
    img_data = requests.get(link, headers = HEADER)
    if img_data.status_code == 200:
        img_data = img_data.content
        with open(name, 'wb') as f:
            f.write(img_data)
            return True
    else:
        return False

def get_shutter_images(search, dir):
    print("Searching for images...", end='', flush=True)
    response = requests.get("https://www.shutterstock.com/search/"+search,
                headers = HEADER)
    if response.status_code == 200:
        print(bcolors.OKGREEN+"Done"+bcolors.ENDC)
        selector = Selector(response.text)
        image_links = selector.xpath('//img/@src').getall()
        ts = int(time.time())
        i = 0
        files = []
        print("Downloading Images...", end='', flush=True)
        for link in image_links:
            ext = "."+link.split('.')[-1]
            i += 1
            name = "{}_{}".format(i,ts)+ext
            outfilename = os.path.join(dir,name)
            if save_image(outfilename, link):
                files.append(outfilename)
        if len(files)>0:
            print(bcolors.OKGREEN+"Done"+bcolors.ENDC)
        else:
            print(bcolors.FAIL+"Fail"+bcolors.ENDC)
        return files
    else:
        print(bcolors.FAIL+"Fail"+bcolors.ENDC)
        print("Error getting images")
        print(response.status_code)
        return None

def augment_image(img, path, name, ext):
    img_aux = img.transpose(Image.FLIP_LEFT_RIGHT)
    p = os.path.join(path,name+"_flr"+ext)
    img_aux.save(p)
    for an in [45,90,135,180,225,270,315]:
        img_aux = img.rotate(an)
        p = os.path.join(path,name+"_"+str(an)+ext)
        img_aux.save(p)
        img_aux = img_aux.transpose(Image.FLIP_LEFT_RIGHT)
        p = os.path.join(path,name+"_"+str(an)+"_flr"+ext)
        img_aux.save(p)
    

def augment_data(files, path):
    print("Augmenting images...", end='', flush=True)
    for file in files:
        name = os.path.basename(file)
        sp = os.path.splitext(name)
        name = sp[0]
        ext = sp[1]
        img = Image.open(file)
        augment_image(img, path, name, ext)
    print(bcolors.OKGREEN+"Done"+bcolors.ENDC)

def main():
    args = parse_arguments()
    subprocess.call('', shell=True)
    files = get_shutter_images(args.s, args.d)
    augment_data(files, args.d)


if __name__ == "__main__":
    main()
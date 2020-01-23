#!/usr/bin/python
from os import listdir
from PIL import Image as PImage
import argparse
import os
from parsel import Selector
import requests
import subprocess
import sys
from PIL import Image
import time

def loadImages(path):
    # return array of images

    imagesList = listdir(path)
    loadedImages = []
    for image in imagesList:
        img = PImage.open(path + image)
        loadedImages.append(img)

    return loadedImages
path = "/Users/Finlay/Desktop/EES/Train/dataset/mug/"

# your images in an array
imgs = loadImages(path)

for img in imgs:
    x = 0
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    for an in [45,90,135,180,225,270,315]:
       img2 = img.rotate(an)
       img2.save("/Users/Finlay/Desktop/EES/Train/dataset/mug" + x + str(an) + ".png")
    x = x + 1
    # you can show every image
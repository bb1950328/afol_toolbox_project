# coding=utf-8

"""
This script should be executed in a folder with several XXXXp subfolders.
It reads all images from the highest XXXXp folder and scales it down to the other folders.
It replaces existing images and works only for images with 1:1 aspect ratio.
"""
import os
import re
from pprint import pprint

from PIL import Image

if __name__ == '__main__':
    xxxp_pattern = re.compile("\\d+p")
    xxxp_dirs = list(filter(lambda di: xxxp_pattern.fullmatch(di), os.listdir(".")))
    xxxp_dirs.sort(key=lambda di: int(di[:-1]), reverse=True)
    print("Found the following directories: ", end="")
    pprint(xxxp_dirs)

    img_names = os.listdir(os.path.join(".", xxxp_dirs[0]))
    print("Found the following images to scale: ", end="")
    pprint(img_names)

    target_scales = [int(di[:-1]) for di in xxxp_dirs[1:]]

    for img_file in img_names:
        img_path = os.path.join(".", xxxp_dirs[0], img_file)
        print("Resizing ", img_path, end=" ")
        img = Image.open(img_path)
        for tscale in target_scales:
            print(f"to {tscale}p", end=" ")
            target_path = os.path.join(".", f"{tscale}p", img_file)
            img.resize((tscale, tscale), Image.BICUBIC).save(target_path)
        print()
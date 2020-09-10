# coding=utf-8

"""
This script should be executed in a folder with a subfolder called "original" which contains the original images.
It reads all images from there and scales it to all the target folders with the given nouber of pixels
It replaces existing images
"""
import math
import os
import shutil

from PIL import Image

from afol_toolbox_app.model import util, logger

IMG_EXTENSIONS = ["jpg", "jpeg", "bmp", "png", ]


if __name__ == '__main__':
    if os.path.split(os.getcwd())[1] == "afol_toolbox_project":  # running from repo root
        os.chdir("./afol_toolbox_app/static/img/")
        logger.log.info(f"cd to {os.getcwd()}")
        cd_called = True
    else:
        cd_called = False

    MP = 2 ** 20  # how many pixels are 1 megapixel
    target_folders = ["1mp", "2mp", "6mp"]
    target_pixels = [MP, 2 * MP, 6 * MP]
    originals = util.get_all_files_in_directory("./original/", absolute=False)

    for t_folder in target_folders:
        t_path = os.path.abspath(os.path.join(".", t_folder))
        logger.log.info(f"Clearing {t_path}")
        util.clear_folder_content(t_path)

    for orig_path in originals:
        if orig_path.rsplit(".", 1) not in IMG_EXTENSIONS:
            parts = orig_path.replace("\\", "/").split("/")
            for t_folder in target_folders:
                target_path = orig_path.replace("original", t_folder)
                target_abs_path = os.path.abspath(target_path)
                util.create_containing_folders_if_necessary(target_abs_path)
                logger.log.debug("copy " + orig_path + " -> " + target_abs_path)
                shutil.copyfile(orig_path, target_abs_path)
            logger.log.info(f"copied {orig_path} because it's not a pixel-based image.")
        else:
            msg = f"Resizing {orig_path} "
            orig_img = Image.open(orig_path)
            orig_x, orig_y = orig_img.size
            orig_pixels = orig_x * orig_y
            msg += f"from {orig_x}x{orig_y}"
            for i_target, tpixels in enumerate(target_pixels):
                scale = math.sqrt(orig_pixels / tpixels)
                t_x = int(orig_x / scale)
                t_y = int(orig_y / scale)
                msg += f" to {t_x}x{t_y}"
                target_path = orig_path.replace("original", target_folders[i_target])
                util.create_containing_folders_if_necessary(target_path)
                orig_img.resize((t_x, t_y), Image.BICUBIC).save(target_path)
            logger.log.info(msg)
    if cd_called:
        os.chdir("../../..")
        logger.log.info(f"cd back to {os.getcwd()}")
else:
    raise Exception("Do not import this file!!!")

import os
import subprocess
from PIL import Image

from src.preprocessing.config import TARGET_WIDTH, TARGET_HEIGHT


def resize(folder_path, target_width=TARGET_WIDTH, target_height=TARGET_HEIGHT):
    subdirs = [
        d
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    ]

    for subdir in subdirs:
        subdir_path = os.path.join(folder_path, subdir)

        for filename in os.listdir(subdir_path):
            if filename.lower().endswith((".jpg")):
                img_path = os.path.join(subdir_path, filename)

                # First, resize the image such that the smaller dimension becomes 224 pixels
                subprocess.run(
                    [
                        "magick",
                        "convert",
                        img_path,
                        "-resize",
                        f"{target_width}x{target_height}^",
                        img_path,
                    ]
                )

                # Then, center-crop the image to target_width x target_height
                subprocess.run(
                    [
                        "magick",
                        "convert",
                        img_path,
                        "-gravity",
                        "center",
                        "-crop",
                        f"{target_width}x{target_height}+0+0",
                        "+repage",
                        img_path,
                    ]
                )


def new_resize(
    folder_path: str,
    target_width=TARGET_WIDTH,
    target_height=TARGET_HEIGHT,
    format="jpg",
):
    subdirs = [
        d
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    ]

    for subdir in subdirs:
        subdir_path = os.path.join(folder_path, subdir)

        for filename in os.listdir(subdir_path):
            if filename.lower().endswith((format)):
                img_path = os.path.join(subdir_path, filename)

                with Image.open(img_path) as img:
                    # First, resize the image such that the smaller dimension becomes target pixels
                    img.thumbnail((target_width, target_height), Image.ANTIALIAS)

                    # Center-crop to the target dimensions
                    width, height = img.size
                    left = (width - target_width) / 2
                    top = (height - target_height) / 2
                    right = (width + target_width) / 2
                    bottom = (height + target_height) / 2

                    img = img.crop((left, top, right, bottom))

                    img.save(img_path)

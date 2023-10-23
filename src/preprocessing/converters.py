import os
from PIL import Image


def convert(input_dir: str, source_format: str, target_format: str):
    for filename in os.listdir(input_dir):
        if filename.lower().endswith("." + source_format):
            input_filepath = os.path.join(input_dir, filename)
            output_filepath = os.path.join(
                input_dir, filename.replace(f".{source_format}", f".{target_format}")
            )

            with Image.open(input_filepath) as img:
                img.save(output_filepath)

            os.remove(input_filepath)


def rename_all_files(input_dir: str, prefix: str = "IMG", suffix: str = ""):
    files = [
        f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))
    ]

    # Sort the files, you can customize this if needed
    files.sort()

    for idx, file_name in enumerate(files, start=1):
        base, ext = os.path.splitext(file_name)
        new_name = f"{prefix}_{idx}{ext}_{suffix}"
        os.rename(os.path.join(input_dir, file_name), os.path.join(input_dir, new_name))


# Converts all HEIC files in a directory to JPG
def convert_heic_to_jpg(input_dir: str):
    convert(input_dir, "heic", "jpg")


# Converts all PNG files in a directory to JPG
def convert_png_to_jpg(input_dir):
    convert(input_dir, "png", "jpg")

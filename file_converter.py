import os
import rawpy
from PIL import Image
import imageio
import numpy as np


def calculate_image_dimension(dimension, resolution):
    if "%" in resolution:
        factor = float(resolution.strip("%").strip()) / 100.0
        result = int(dimension * factor)
    else:
        result = int(resolution)
    return result


def convert_cr2_to_jpg(input_folder, output_folder, resolution=("80%", "80%")):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".CR2") or filename.endswith(".cr2"):
            # Construct the input and output file paths
            input_file_path = os.path.join(input_folder, filename)
            output_filename = filename[:-4] + ".jpg"  # Change extension to .jpg
            output_file_path = os.path.join(output_folder, output_filename)

            # Use rawpy to read the CR2 file
            with rawpy.imread(input_file_path) as raw:
                # Convert to RGB image
                rgb = raw.postprocess(use_auto_wb=True, no_auto_bright=True)
            if resolution:
                pil_image = Image.fromarray(rgb)

                # Resize the image
                width = calculate_image_dimension(pil_image.width, resolution[0])
                height = calculate_image_dimension(pil_image.height, resolution[1])
                pil_image = pil_image.resize((width, height))

                rgb = np.array(pil_image)

            # Save the RGB image as JPEG
            imageio.imsave(output_file_path, rgb)
            print(f"Converted: {filename} -> {output_filename}")


# Example usage
input_folder = "./old"
output_folder = "./new"
convert_cr2_to_jpg(input_folder, output_folder)

from PIL import Image
import os


from PIL import Image
import os


def crop_images_to_16_9(input_folder, valid_extensions):
    # Walk through all files and subdirectories in the input folder
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(tuple(valid_extensions)):
                # Load the image
                image_path = os.path.join(root, filename)
                img = Image.open(image_path)

                # Get the bounding box of non-zero pixels
                bbox = img.getbbox()

                if bbox:  # Ensure there's a valid bounding box
                    # Crop the image using the bounding box
                    cropped_img = img.crop(bbox)

                    # Determine dimensions for 16:9 aspect ratio
                    cropped_width, cropped_height = cropped_img.size
                    target_width, target_height = cropped_width, cropped_height

                    # Calculate new dimensions based on the aspect ratio
                    if cropped_width / cropped_height > 16 / 9:
                        # Width exceeds 16:9 ratio; adjust height
                        target_height = int(cropped_width / (16 / 9))
                    else:
                        # Height exceeds 16:9 ratio; adjust width
                        target_width = int(cropped_height * (16 / 9))

                    # Create a new transparent image with the target dimensions
                    new_img = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
                    paste_x = (target_width - cropped_width) // 2
                    paste_y = (target_height - cropped_height) // 2

                    #



if __name__ == "__main__":
    input_folder = r"C:\Users\bokch\PyCharm\W1\images"
    valid_extensions = ('.png', '.jpg', '.jpeg')

    crop_images_to_16_9(input_folder, valid_extensions)

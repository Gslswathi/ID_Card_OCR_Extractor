import base64
import os

# This function reads an image file and converts it to a base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# This function saves the base64 string into a .txt file
def save_base64_to_file(base64_str, output_path):
    with open(output_path, "w") as f:
        f.write(base64_str)

# This function clears the output folder before each run
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"🧹 Cleared folder: {folder_path}")
    else:
        os.makedirs(folder_path)
        print(f"📁 Created folder: {folder_path}")

# This function reads all images from the input folder,
# converts them to base64, and saves them into .txt files
def convert_images_in_folder(input_folder, output_folder):
    clear_folder(output_folder)  # Clear the output folder before saving new files

    # Loop through all image files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            src = os.path.join(input_folder, filename)  # Full path of the image

            # Convert image to base64 string
            b64 = image_to_base64(src)

            # Create output file name with .txt extension
            txt = os.path.splitext(filename)[0] + ".txt"
            out = os.path.join(output_folder, txt)

            # Save the base64 string to the output file
            save_base64_to_file(b64, out)

            print(f"✅ Saved base64 ➜ {out}")

# This is the main entry point of the script
if __name__ == "__main__":
    convert_images_in_folder("test_images", "generated_base64")
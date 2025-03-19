from PIL import Image
import requests
from io import BytesIO

# URLs of large images
image_urls = [
    "https://raw.githubusercontent.com/ymalegao/AutoLanding/main/RealLifeScenario/output_7/rgb_labeled.png",
    "https://raw.githubusercontent.com/ymalegao/AutoLanding/main/RealLifeScenario/output_7/color_depth_labeled.png",
    "https://raw.githubusercontent.com/ymalegao/AutoLanding/main/RealLifeScenario/output_7/segmentation_labeled.png"
]

def compress_image(url, output_path, max_size_kb=500):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    img.save(output_path, format="PNG", optimize=True, quality=85)  # Adjust quality for smaller size
    print(f"Compressed image saved: {output_path}")


# Function to download, resize, and save images
def resize_and_save(url, save_path, new_size=(1024, 1024)):  # Resize to 1024x1024
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    # Resize the image
    img = img.resize(new_size, Image.LANCZOS)
    
    # Save the new image (overwrite or save in a new directory)
    img.save(save_path, format="PNG", optimize=True)

# # Resize and save all images
# resize_and_save(image_urls[0], "rgb_labeled_resized.png")
# resize_and_save(image_urls[1], "color_depth_labeled_resized.png")
# resize_and_save(image_urls[2], "segmentation_labeled_resized.png")

#compress ikmages
compress_image(image_urls[0], "rgb_labeled_compressed.png")
compress_image(image_urls[1], "color_depth_labeled_compressed.png")
compress_image(image_urls[2], "segmentation_labeled_compressed.png")

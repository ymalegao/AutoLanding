import cv2
import numpy as np
import os
import json
from itertools import product

GRID_SIZE = 7
ROWS = "ABCDEFG"
COLS = "1234567"
GRID_LABELS = [f"{row}{col}" for row, col in product(ROWS, COLS)]

print(GRID_LABELS)

def load_image(image_path):
    return cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

def split_image_into_grid(image, grid_size):
    """Splits an image into a grid without saving individual patches."""
    h, w = image.shape[:2]
    patch_h, patch_w = h // grid_size, w // grid_size
    grid_data = {}

    for i, (row, col) in enumerate(product(range(grid_size), range(grid_size))):
        x_start, y_start = col * patch_w, row * patch_h
        x_end, y_end = x_start + patch_w, y_start + patch_h
        patch = image[y_start:y_end, x_start:x_end]
        grid_data[GRID_LABELS[i]] = patch
    
    return grid_data

def overlay_grid_labels(image, grid_size, imageName):
    """Adds A1-E5 labels to the image for LLM reference."""
    labeled_image = image.copy()
    
    color = (0, 0, 0)
    if "depth" in imageName:
        color = (255, 255, 255)
    if "segmentation" in imageName:
        color = (255, 255, 255)
    if "rgb" in imageName:
        color = (255, 255, 255)

    h, w = image.shape[:2]
    patch_h, patch_w = h // grid_size, w // grid_size

    for i, (row, col) in enumerate(product(range(grid_size), range(grid_size))):
        x, y = col * patch_w + patch_w // 3, row * patch_h + patch_h // 2
        #black text for RBG and segmentation, white text for depth
        segment_text_size = 3
        rgb_text_size = 3
        depth_text_size = 1
        if "depth" in imageName:
            cv2.putText(labeled_image, GRID_LABELS[i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, depth_text_size, color, 2, cv2.LINE_AA)
        if "segmentation" in imageName:
            #bold text for segmentation
            cv2.putText(labeled_image, GRID_LABELS[i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, segment_text_size, color, 6, cv2.LINE_AA)
        if "rgb" in imageName:
            cv2.putText(labeled_image, GRID_LABELS[i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, rgb_text_size, color, 6, cv2.LINE_AA)
        #cv2.putText(labeled_image, GRID_LABELS[i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    
    return labeled_image

def save_labeled_images(rgb, depth, segmentation, output_dir):
    """Saves images with grid overlays for LLM reference."""
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, "rgb_labeled.png"), rgb)
    cv2.imwrite(os.path.join(output_dir, "depth_labeled.png"), depth)
    cv2.imwrite(os.path.join(output_dir, "segmentation_labeled.png"), segmentation)


def main(rgb_path, depth_path, segmentation_path, output_dir):
    # Load images
    rgb = load_image(rgb_path)
    print(rgb.shape)
    depth = load_image(depth_path)
    print(depth.shape)
    segmentation = load_image(segmentation_path)
    print(segmentation.shape)

    # Split into grid
    grid_rgb = split_image_into_grid(rgb, GRID_SIZE)
    grid_depth = split_image_into_grid(depth, GRID_SIZE)
    grid_segmentation = split_image_into_grid(segmentation, GRID_SIZE)

    # Overlay labels
    labeled_rgb = overlay_grid_labels(rgb, GRID_SIZE, "rgb")
    print(labeled_rgb.shape)
    labeled_depth = overlay_grid_labels(depth, GRID_SIZE, "depth")
    labeled_segmentation = overlay_grid_labels(segmentation, GRID_SIZE, "segmentation")
    
    # Save labeled images
    save_labeled_images(labeled_rgb, labeled_depth, labeled_segmentation, output_dir)

    # Generate LLM input JSON
    
    print(f"Processing complete! Outputs saved in {output_dir}")

def make_grid_for_colored_depth_map(colored_path, output_dir):
    colored_depth_map = cv2.imread(colored_path)
    grid_colored_depth_map = overlay_grid_labels(colored_depth_map, GRID_SIZE, "depth")
    cv2.imwrite(os.path.join(output_dir, "color_depth_labeled.png"), grid_colored_depth_map)

# Example Usage
# main("scene.png", "depth_map1.png", "segmentation.png", "output")

#open scenarios folder
#for each folder in scenarios, open the folder, get the rgb, depth, and segmentation images, and run the main function, save the output in the output folder in the same scenario folder

# for scenario in os.listdir("scenarios"):
#     scenario_dir = os.path.join("scenarios", scenario)
#     if os.path.isdir(scenario_dir):
#         rgb_path = os.path.join(scenario_dir, "rgb.png")
#         depth_path = os.path.join(scenario_dir, "depth.png")
#         segmentation_path = os.path.join(scenario_dir, "segmentation.png")
#         output_dir = os.path.join(scenario_dir, "output_7")
#         # main(rgb_path, depth_path, segmentation_path, output_dir)
#         colored_depth_path = os.path.join(scenario_dir, "depth_map_colored.png")
#         make_grid_for_colored_depth_map(colored_depth_path, output_dir)
    

dir_path = "RealLifeScenario"
rgb_path = os.path.join(dir_path, "rgb.png")
print(rgb_path)
depth_path = os.path.join(dir_path, "depth_map_colored.png")
segmentation_path = os.path.join(dir_path, "segmentation.png")
output_dir = os.path.join(dir_path, "output_7")
main(rgb_path, depth_path, segmentation_path, output_dir)
make_grid_for_colored_depth_map(depth_path, output_dir)


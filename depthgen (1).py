"""depthgen.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y88Lmmnfxl2JVCiIvq3a7jfC9U3jU7uT
"""
import torch
import urllib
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os



from torchvision.transforms import Compose, Resize, ToTensor

model_type = "DPT_Large"
model = torch.hub.load("intel-isl/MiDaS", model_type)

model.eval()
transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform

# for scenario in os.listdir("scenarios"):
#     scenario_dir = os.path.join("scenarios", scenario)
#     if os.path.isdir(scenario_dir):
#         rgb_path = os.path.join(scenario_dir, "rgb.png")
#         img = cv2.imread(rgb_path)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         input_batch = transform(img).unsqueeze(0).squeeze(0)
#         with torch.no_grad():
#             prediction = model(input_batch)
#         depth_map = prediction.squeeze().cpu().numpy()
#         depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
#         depth_map_normalized = depth_map_normalized.astype(np.uint8)
#         colormap = cv2.applyColorMap(depth_map_normalized, cv2.COLORMAP_PLASMA)
#         cv2.imwrite(os.path.join(scenario_dir, "depth_map_colored.png"), colormap)

img = cv2.imread("./RealLifeScenario/realLife.JPG")
if img is None:
  print("Image not loaded")
else:
  print("Image loaded")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


input_batch = transform(img).unsqueeze(0).squeeze(0)

print(input_batch.shape)

with torch.no_grad():
  prediction = model(input_batch)

depth_map = prediction.squeeze().cpu().numpy()

import matplotlib.pyplot as plt

plt.imshow(depth_map, cmap="plasma")
plt.colorbar()
plt.show()

depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
depth_map_normalized = depth_map_normalized.astype(np.uint8)

# Apply a colormap (this adds color instead of grayscale)
colormap = cv2.applyColorMap(depth_map_normalized, cv2.COLORMAP_PLASMA)  # You can also try COLORMAP_JET

# Save the heatmap depth map as a colored image
cv2.imwrite("depth_map_colored.png", colormap)

# Display it to confirm
plt.imshow(cv2.cvtColor(colormap, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for Matplotlib
plt.axis("off")
plt.show()
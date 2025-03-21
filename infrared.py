import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the RGB image
image = cv2.imread("./RealLifeScenario/rgb.png")  # Change to your image path
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB (OpenCV loads in BGR)

# Convert to grayscale (simulating IR detection of intensity)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# Apply a colormap (mimicking infrared heat vision)
infrared_image = cv2.applyColorMap(gray, cv2.COLORMAP_JET)

# Display the original and infrared images
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("Original RGB Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(infrared_image)
plt.title("Simulated Infrared Image")
plt.axis("off")

plt.show()

# Save the infrared image
cv2.imwrite("infrared_output.png", infrared_image)

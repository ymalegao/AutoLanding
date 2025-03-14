from openai import OpenAI
import base64
import cv2
import os


client= OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)
# Function to encode image to base64 and convert to Data URL
def encode_image_to_data_url(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    # Determine the image's MIME type
    mime_type = "image/jpeg" if image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg") else "image/png"
    return f"data:{mime_type};base64,{encoded_string}"

# Function to resize image to reduce token usage
def resize_image(image_path, new_size=(512, 512)):
    image = cv2.imread(image_path)
    resized = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    cv2.imwrite(image_path, resized)

# Resize images before processing to save tokens
resize_image("output/rgb_labeled.png")
resize_image("output/depth_labeled.png")
resize_image("output/segmentation_labeled.png")

# Sensor-specific prompts (concise)
RGB_PROMPT = """A quadcopter needs to perform an emergency landing.
The image is divided into a 5×5 grid (A1 to E5).
**Your Task:**
- Identify hazards (fire, debris, people) in each section.
- Rank the safest landing zones.
**Output Format:**
["Best", "Second Best", ..., "Worst"]
"""

OVER_ALL_PROMPT = """"A quadcopter needs to perform an emergency landing. You are provided three images - one Depth map, one camera image, and one infrared/segmentation. 

The images are all of the same scene and camera angle divided into a 5×5 grid (A1 to E5).
**Your Task:**
- Identify hazards (fire, debris, people) in each section.
- Rank the safest landing zones.
**Output Format:**
["Best", "Second Best", ..., "Worst"]

Choose the safest rooftop to land on. You should not land on the ground"""

print(OVER_ALL_PROMPT)


# SEGMENTATION_PROMPT = """A quadcopter is analyzing a segmentation map where **each color represents a different object**.

# 🚀 **Your Task:**
# - Identify landing surfaces.
# - Rank zones based on safety.

# 🔹 **Output Format:**
# ["Best", "Second Best", ..., "Worst"]
# """

# Encode images to Data URLs
rgb_data_url = encode_image_to_data_url("output/rgb_labeled.png")
depth_data_url = encode_image_to_data_url("output/depth_labeled.png")
segmentation_data_url = encode_image_to_data_url("output/segmentation_labeled.png")


def get_analysis(prompt, image_data_url):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": image_data_url}
        ]
    )
    return response.choices[0].message.content.strip()

# Batch API call to analyze all three images in one request
# response = client.chat.completions.create(
#     model="gpt-4-turbo",
#     messages=[
#         {"role": "system", "content": RGB_PROMPT},
#         {"role": "user", "content": [{"type": "image_url", "image_url": {"url": rgb_data_url}}]},
#         {"role": "system", "content": DEPTH_PROMPT},
#         {"role": "user", "content": [{"type": "image_url", "image_url": {"url": depth_data_url}}]},
#         {"role": "system", "content": SEGMENTATION_PROMPT},
#         {"role": "user", "content": [{"type": "image_url", "image_url": {"url": segmentation_data_url}}]}
#     ],
# # )
all_sensor_ranking = get_analysis(OVER_ALL_PROMPT, rgb_data_url)
# depth_ranking = get_analysis(DEPTH_PROMPT, depth_data_url)
# segmentation_ranking = get_analysis(SEGMENTATION_PROMPT, segmentation_data_url)

# print("RGB Analysis Ranking:", rgb_ranking)
# print("Depth Analysis Ranking:", depth_ranking)
# print("Segmentation Analysis Ranking:", segmentation_ranking)
# # Extract sensor rankings
# rgb_ranking = response["choices"][0]["message"]["content"]
# depth_ranking = response["choices"][1]["message"]["content"]
# segmentation_ranking = response["choices"][2]["message"]["content"]

# Judge LLM Prompt (More detailed)
# JUDGE_PROMPT = f"""You are an AI responsible for selecting the safest landing spot for a drone.
# You receive data from three expert models:
# - 📷 **RGB Model**: {rgb_ranking}
# - 📏 **Depth Model**: {depth_ranking}
# - 🏷 **Segmentation Model**: {segmentation_ranking}

# 🚀 **Your Task:**
# - **Combine** insights from all models.
# - **Resolve conflicts** (e.g., if one model says "safe" but another says "steep drop").
# - **Prioritize landing zones that are both safe and close.**
# - **Justify your decision with a clear explanation.

# 🔹 **Output Format:**
# 1. **Final Safe Landing Zone:** [Best grid location]
# 2. **Justification:** Explain why this location is optimal, considering all sensor inputs.
# """

# Run Judge LLM
# final_decision = client.chat.completions.create(
#     model="gpt-4-turbo",
#     messages=[
#         {"role": "system", "content": JUDGE_PROMPT}
#     ],
# )

# Print results
# print("RGB Analysis Ranking:", rgb_ranking)
# print("Depth Analysis Ranking:", depth_ranking)
# print("Segmentation Analysis Ranking:", segmentation_ranking)
# print("\nFinal Decision:")
# print(final_decision.choices[0].message.content.strip())
from openai import OpenAI
import os
import csv
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Scenario Names
rural_scenario_names = [
    "Rural1-AfricaNoAnimals", "Rural2-AfricaWithAnimals", "Rural3-AfricaTrees",
    "Rural4-CoastlineRoundAbout", "Rural5-CoastlineBridge"
]
urban_scenario_names = [
    "Urban1- 4 Empty Rooftops", "Urban2 - FireOnRoof", "Urban3 - PeopleonRoof",
    "Urban3.5-PeopleonRooftops", "Urban4-BurningWrittenOnRoof",
    "Urban5-NPeopleWrittenOnRoof", "Urban6-MiscTextWrittenOnRoof", "Urban7-Intersection"
]

# Function to generate raw image URLs
def raw_url_generator(scenario_name):
    scen_name_with_space = scenario_name.replace(" ", "%20")
    urls = [
        f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output_7/rgb_labeled.png",
        f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output_7/depth_labeled.png",
        f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output_7/segmentation_labeled.png"
    ]
    return urls

# Organize URLs
urban_urls = [raw_url_generator(scenario) for scenario in urban_scenario_names]
rural_urls = [raw_url_generator(scenario) for scenario in rural_scenario_names]

# LLM Prompts
URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
You are provided three images - a Segmentation Map, Camera Image, and a Depth Map.
The images are divided into a **7×7 grid (A1 to G7)**.
- Use the segmentation map to identify buildings that are suitable for landing.
- Use the camera image to detect obstacles or hazards.
- Use the depth map to prioritize **closer rooftops**.
- **ONLY rooftops are valid** landing spots.
- **If no safe rooftops exist, return "NO SAFE LANDING SPOT".**

**Output Format:**
[
    {"position": "Best", "grid": "B3", "type": "ROOFTOP", "reason": "Flat and clear rooftop."},
    {"position": "Second Best", "grid": "C2", "type": "ROOFTOP", "reason": "Mostly clear rooftop."},
    {"position": "Third Best", "grid": "D1", "type": "ROOFTOP", "reason": "Accessible with minor debris."}
]
"""

RURAL_PROMPT = """A quadcopter needs to perform an emergency landing in a rural environment.
You are provided three images - a Segmentation Map, Camera Image, and a Depth Map.
The images are divided into a **7×7 grid (A1 to G7)**.
- Use the segmentation map to identify safe ground.
- Use the camera image to detect hazards (water, cliffs, trees, animals).
- Use the depth map to prioritize **closer ground**.
- **If no safe landing zones exist, return "NO SAFE LANDING SPOT".**

**Output Format:**
[
    {"position": "Best", "grid": "B3", "type": "Flat Ground", "reason": "Flat open ground with no obstacles."},
    {"position": "Second Best", "grid": "G3", "type": "Flat Ground", "reason": "Mostly clear area."},
    {"position": "Third Best", "grid": "D1", "type": "Road", "reason": "Accessible but less ideal."}
]
"""

# Function to extract grid locations from the LLM response
def extract_grid_locations(response_text):
    pattern = r'"grid":\s*"([A-G][1-7])"'  # Matches grid format (e.g., "C3", "D2")
    return re.findall(pattern, response_text)

# Create CSV file
csv_filename = "landing_zone_results.csv"
with open(csv_filename, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Scenario", "Best Spot", "Second Best", "Third Best", "Full Response"])  # CSV Header

    # Process Urban Scenarios
    for i, urls in enumerate(urban_urls):
        scenario_name = urban_scenario_names[i]
        print(f"Processing: {scenario_name}")

        # OpenAI API Call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": URBAN_PROMPT},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": urls[2]}},  # Segmentation
                    {"type": "image_url", "image_url": {"url": urls[0]}},  # RGB
                    {"type": "image_url", "image_url": {"url": urls[1]}}   # Depth
                ]}
            ]
        )
        ranking_text = response.choices[0].message.content.strip()
        best_spots = extract_grid_locations(ranking_text)

        # Fallback: Save full response if extraction fails
        if not best_spots:
            csv_writer.writerow([scenario_name, "EXTRACTION FAILED", "", "", ranking_text])
        else:
            csv_writer.writerow([scenario_name] + best_spots[:3] + [""])  # Take up to 3 rankings

    # Process Rural Scenarios
    for i, urls in enumerate(rural_urls):
        scenario_name = rural_scenario_names[i]
        print(f"Processing: {scenario_name}")

        # OpenAI API Call
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": RURAL_PROMPT},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": urls[2]}},  # Segmentation
                    {"type": "image_url", "image_url": {"url": urls[0]}},  # RGB
                    {"type": "image_url", "image_url": {"url": urls[1]}}   # Depth
                ]}
            ]
        )
        ranking_text = response.choices[0].message.content.strip()
        best_spots = extract_grid_locations(ranking_text)

        # Fallback: Save full response if extraction fails
        if not best_spots:
            csv_writer.writerow([scenario_name, "EXTRACTION FAILED", "", "", ranking_text])
        else:
            csv_writer.writerow([scenario_name] + best_spots[:3] + [""])  # Take up to 3 rankings

print(f"✅ Results saved to {csv_filename}")



URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
You are provided one Camera Image.
The image is divided into a **7×7 grid (A1 to G7)**.

- Use the camera image to detect obstacles or hazards and the safest landing zone.
- **ONLY rooftops are valid** landing spots.
- **If no safe rooftops exist, return "NO SAFE LANDING SPOT".**

**Output Format:**
[
    {"position": "Best", "grid": "B3", "type": "ROOFTOP", "reason": "Flat and clear rooftop."},
    {"position": "Second Best", "grid": "C2", "type": "ROOFTOP", "reason": "Mostly clear rooftop."},
    {"position": "Third Best", "grid": "D1", "type": "ROOFTOP", "reason": "Accessible with minor debris."}
]
"""

RURAL_PROMPT = """A quadcopter needs to perform an emergency landing in a rural environment.
You are provided one Camera image. 
The images are divided into a **7×7 grid (A1 to G7)**.

- Use the camera image to detect hazards (water, cliffs, trees, animals) and the safest landing zone.
- **If no safe landing zones exist, return "NO SAFE LANDING SPOT".**

**Output Format:**
[
    {"position": "Best", "grid": "B3", "type": "Flat Ground", "reason": "Flat open ground with no obstacles."},
    {"position": "Second Best", "grid": "G3", "type": "Flat Ground", "reason": "Mostly clear area."},
    {"position": "Third Best", "grid": "D1", "type": "Road", "reason": "Accessible but less ideal."}
]
"""

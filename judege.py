from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


rural_Scenario_names = ["Rural1-AfricaNoAnimals", "Rural2-AfricaWithAnimals", "Rural3-AfricaTrees","Rural4-CoastlineRoundAbout", "Rural5-CoastlineBridge" ] #4

urban_scenario_names = ["Urban1- 4 Empty Rooftops", "Urban2 - FireOnRoof", "Urban3 - PeopleonRoof", "Urban3.5-PeopleonRooftops","Urban4-BurningWrittenOnRoof", "Urban5-NPeopleWrittenOnRoof", "Urban6-MiscTextWrittenOnRoof", "Urban7-Intersection"] #7

currIndex = 0
def raw_url_generator(scenario_name):
    #make sure to add %20 for spaces in the scenario name
    scen_name_with_space = scenario_name.replace(" ", "%20")
    urls =[f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output_7/rgb_labeled.png", f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output_7/color_depth_labeled.png", f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output_7/segmentation_labeled.png"]
    return urls


URL_arr = []

R_URL_arr = []

for scenario in urban_scenario_names:
    URL_arr.append(raw_url_generator(scenario))

for scenario in rural_Scenario_names:
    R_URL_arr.append(raw_url_generator(scenario))

# print(URL_arr[0])   



# Optimized prompt that accounts for all three images at once
# URBAN_PROMPT = """A quadcopter needs to perform an emergency landing.
# You are provided three images - one Depth map, one camera image, and one infrared/segmentation.

# The images are divided into a 5×5 grid (A1 to E5).
# **Your Task:**
# - Identify hazards (fire, debris, people) in each section.
# - Rank the safest landing zones, prioritizing rooftops.
# - **Do NOT land on the ground unless no rooftops are available.**
# - **If an area has any obstacles (fire, people, debris), it is completely unsafe.**
# - **Do NOT rank unsafe locations.** Instead, mention "NO SAFE LANDING SPOT" if all rooftops are obstructed.
# - **Only rank completely clear zones** with a wide enough landing area.
# - If the coordinate is between two safe zones, say "Rooftop between A1 and A2".

# **Output Format:**
# ["Best", "Second Best", ..., "NO SAFE LANDING SPOT" (if applicable)]
# """
# URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
# You are provided three images - one camera image, one Depth map, and one infrared/segmentation.

# The images are divided into a 5×5 grid (A1 to E5).
# **Your Task:**
# - Identify hazards (fire, debris, people) in each section.
# - Rank the safest landing zones, prioritizing **ONLY rooftops**.
# - **DO NOT land on the ground or any space that is not explicitly a rooftop.**
# - **Ignore all streets, parking lots, open plazas, or any area at ground level.**
# - If no safe rooftops exist, return **"NO SAFE LANDING SPOT"** instead of choosing a ground location.
# - If the coordinate is between two safe rooftops, say **"Rooftop between A1 and A2"**.
# - **For each ranking, provide a reason for selection.**

# **Output Format:**
# [
#     {"position": "Best", "grid": "C3", "reason": "Clear, flat rooftop with no obstacles."},
#     {"position": "Second Best", "grid": "D2", "reason": "Rooftop near C3, mostly clear."},
#     {"position": "NO SAFE LANDING SPOT", "reason": "All rooftops have fire, debris, or people."}
# ]
    

# """
# URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
# You are provided three images - a Depth Map, a Camera Image, and a Segmentation Map.

# The images are divided into a 5×5 grid (A1 to E5).

# ### **Decision Process (MUST FOLLOW THIS ORDER)**:
# 1. **Segmentation Map (Identify Buildings & Rooftops)**  
#    - First, use the segmentation map to identify **all buildings with flat rooftops**.  
#    - Ignore all non-building areas (streets, open spaces, parking lots, and the ground).  

# 2. **Depth Map (Prioritize Closest Rooftops)**  
#    -Black and white image with white being closer and black being farther away
#    - Among the identified rooftops, use the depth map to prioritize **closer rooftops** (lower depth values).  
#    - A rooftop that is closer is **better** than one that is farther away.

# 3. **Camera Image (Check for Fire, Debris, People)**  
#    - Finally, check the RGB image for **fire, debris, or people**.  
#    - **Only eliminate rooftops where fire fully covers the surface.**  
#    - If a rooftop has **only partial fire coverage**, rank the **clear section of that rooftop** instead.

# ### **Rules**:
# - **DO NOT land on the ground or open spaces.** Only rooftops are valid.
# - **DO NOT eliminate all rooftops unless every single one is fully obstructed.**
# - **If no safe rooftops exist at all, return "NO SAFE LANDING SPOT".**
# - If a rooftop is between two sections, say **"Rooftop between A1 and A2"**.

# ### **Output Format (Follow This Exactly)**:
# [
#     {"position": "Best", "grid": "C3", "reason": "Closest rooftop with no hazards."},
#     {"position": "Second Best", "grid": "D2", "reason": "Rooftop near C3, mostly clear."},
#     {"position": "Third Best", "grid": "A2", "reason": "Partially safe rooftop, fire in one section."},
#     {"position": "NO SAFE LANDING SPOT", "reason": "All rooftops are fully covered with fire, debris, or people."}
# ]
# """


URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
You are provided three images - a Segmentation Map, Camera Image, and a Depth Map.
The images are divided into a **7×7 grid (A1 to G7)**.
- Use the segmentation map to identify buildings that are suitable for landing.
- Use the camera image to detect obstacles or hazards.
- Use the depth map to prioritize **closer rooftops**.
- **ONLY rooftops are valid** landing spots
- **If no safe rooftops exist, return "NO SAFE LANDING SPOT".**
**Output Format:**
[
    {"position": "Best", "grid": "B3", "type": "ROOFTOP", "reason": "Flat and clear rooftop."},
    {"position": "Second Best", "grid": "C2", "type": "ROOFTOP", "reason": "Mostly clear rooftop."},
    {"position": "Third Best", "grid": "D1", "type": "ROOFTOP", "reason": "Accessible with minor debris."}
]
"""



SINGLE_CAM_URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
You are provided one Camera Image.
The image is divided into a **7×7 grid (A1 to G7)**.

- Use the camera image to detect obstacles or hazards and the safest landing zone.
- **ONLY rooftops are valid** landing spots.
- **If no safe rooftops exist, return "NO SAFE LANDING SPOT".**
- **You CAN select multiple coordinates on the same rooftop IF AND ONLY IF all selected areas are completely clear.**

**Output Format:**
[
    {"position": "Best", "grid": "B3", "type": "ROOFTOP", "reason": "Flat and clear rooftop."},
    {"position": "Second Best", "grid": "C2", "type": "ROOFTOP", "reason": "Mostly clear rooftop."},
    {"position": "Third Best", "grid": "D1", "type": "ROOFTOP", "reason": "Accessible with minor debris."}
]
"""

# URBAN_PROMPT = """A quadcopter needs to perform an emergency landing in an urban environment.
# You are provided three images - a Segmentation Map, Camera Image, and a Depth Map.
# The images are divided into a 7×7 grid (A1 to G7).

# Strict Landing Rules (Follow EXACTLY):
# You MUST land on a rooftop. No exceptions.  
# You CANNOT land in open areas, streets, plazas, parks, or the ground. 
# If no safe rooftops exist, return ONLY "NO SAFE LANDING SPOT".

# How to Rank Landing Zones:
# Use the segmentation map to identify **buildings with flat rooftops. Ignore non-building areas.
# Use the camera image to check for hazards like fire, debris, or people.
# Use the depth map to prioritize rooftops that are closer for faster & safer landing.

# Strict Output Format:
# [
#     {"position": "Best", "grid": "B3", "type": "ROOFTOP", "reason": "Flat and clear rooftop, no obstacles."},
#     {"position": "Second Best", "grid": "C2", "type": "ROOFTOP", "reason": "Mostly clear rooftop, minor debris."},
#     {"position": "Third Best", "grid": "D1", "type": "ROOFTOP", "reason": "Accessible rooftop, some minor obstructions."}
# ]

# If no valid rooftops exist, return ONLY this exact response:
# ["NO SAFE LANDING SPOT"]
# """




RURAL_PROMPT = """A quadcopter needs to perform an emergency landing in a rural environment.
You are provided three images -  one camera image,one Depth map, and one infrared/segmentation.

The images are divided into a 5×5 grid (A1 to E5).
**Your Task:**
- Identify hazards (water, cliffs, trees, dense vegetation, rocks, or animals) in each section.
- Rank the safest landing zones, prioritizing **flat, open ground** with **minimal obstacles**.
- **Avoid landing near bodies of water, cliffs, roads, or dense vegetation.**
- **Do NOT land on roads unless they are the only safe option.**
- If the coordinate is between two safe zones, say **"Open ground near A1 and A2"**.
- **If no safe landing spots exist, return "NO SAFE LANDING SPOT".**
- **For each ranking, provide a reason for selection.**

**Output Format:**
[
    {"position": "Best", "grid": "C3", "reason": "Flat open ground with no obstacles."},
    {"position": "Second Best", "grid": "D2", "reason": "Mostly clear ground, small rocks nearby but still safe."},
    {"position": "Third Best", "grid": "E1", "reason": "Open area, minor vegetation nearby."},
    {"position": "NO SAFE LANDING SPOT", "reason": "All locations have water, cliffs, or dense trees."}
]
"""


# Make API call with all three images at once


    
# # Extract and print results
if __name__ == "__main__":
    rgb_url, depth_url, segmentation_url = URL_arr[2]
    # rgb_url, depth_url, segmentation_url = R_URL_arr[0]
    print(rgb_url)
    print(depth_url)
    print(segmentation_url)
    response = client.chat.completions.create(
    model="gpt-4o",  # Supports vision
    messages=[
        {"role": "system", "content": URBAN_PROMPT},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": segmentation_url}},
            {"type": "image_url", "image_url": {"url": rgb_url}},
            {"type": "image_url", "image_url": {"url": depth_url}}
            ]}
    ]
    )
    ranking = response.choices[0].message.content.strip()
    print(ranking)
    open("ranking.txt", "w").write(ranking) # Save results to a file
    

    
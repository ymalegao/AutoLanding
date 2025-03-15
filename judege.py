from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


rural_Scenario_names = ["Rural1-AfricaNoAnimals", "Rural2-AfricaWithAnimals", "Rural3-AfricaTrees","Rural4-CoastlineRoundAbout", "Rural5-CoastlineBridge" ] #4

urban_scenario_names = ["Urban1- 4 Empty Rooftops", "Urban2 - FireOnRoof", "Urban3 - PeopleonRoof", "Urban3.5-PeopleonRooftops","Urban4-BurningWrittenOnRoof", "Urban5-NPeopleWrittenOnRoof", "Urban6-MiscTextWrittenOnRoof", "Urban7-Intersection"] #7

currIndex = 0
def raw_url_generator(scenario_name):
    #make sure to add %20 for spaces in the scenario name
    scen_name_with_space = scenario_name.replace(" ", "%20")
    urls =[f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output/rgb_labeled.png", f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output/depth_labeled.png", f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output/segmentation_labeled.png"]
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
You are provided three images - a Depth Map, a Camera Image, and a Segmentation Map.

The images are divided into a **5×5 grid (A1 to E5)**.

### **Decision Process (MUST FOLLOW THIS ORDER)**:
1. **Camera Image (Identify Rooftops)**
   - **The camera image is the ONLY source used to identify rooftops.**
   - Look for **flat, unobstructed surfaces on top of buildings.**
   - **DO NOT use the depth map or segmentation map to assume a location is a rooftop.**
   - If a location is inside a building or on its vertical walls, **ignore it**.

2. **Segmentation Map (Confirm Building Areas)**
   - Use the segmentation map to **confirm** that a selected rooftop belongs to a building.
   - **DO NOT assume all parts of a building are rooftops.** Only those confirmed by the camera image should be considered.

3. **Depth Map (Prioritize Closest Rooftops)**
   - Once rooftops are identified using the camera, use the depth map to prioritize **closer rooftops**.
   - **Ignore depth for any locations that are not already verified as rooftops.**

4. **Hazard Check (Camera Image)**
   - Use the **camera image** to check for **fire, debris, or people.**
   - **If a rooftop has a safe section, rank that section instead of eliminating the whole rooftop.**

### **Rules**:
- **DO NOT assume a location is a rooftop just because it is part of a building.**
- **DO NOT land on the ground or open spaces.** Only rooftops are valid.
- **If no safe rooftops exist, return "NO SAFE LANDING SPOT".**
- **If a safe rooftop exists, say "the rooftop of the B3 building" instead of just "B3".**

### **Output Format (Follow This Exactly)**:
[
    {"position": "Best", "grid": "B3", "type": "ROOFTOP", "reason": "The rooftop of the B3 building, no hazards."},
    {"position": "Second Best", "grid": "C2", "type": "ROOFTOP", "reason": "The rooftop of the C2 building, partially clear."},
    {"position": "Third Best", "grid": "D1", "type": "ROOFTOP", "reason": "Flat, accessible rooftop with minor debris."}
]
"""

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
    rgb_url, depth_url, segmentation_url = URL_arr[1]
    # rgb_url, depth_url, segmentation_url = R_URL_arr[1]
    print(rgb_url)
    print(depth_url)
    print(segmentation_url)
    response = client.chat.completions.create(
    model="gpt-4o",  # Supports vision
    messages=[
        {"role": "system", "content": URBAN_PROMPT},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": segmentation_url}},
            {"type": "image_url", "image_url": {"url": depth_url}},
            {"type": "image_url", "image_url": {"url": rgb_url}}
            ]}
    ]
    )
    ranking = response.choices[0].message.content.strip()
    print(ranking)
    open("ranking.txt", "w").write(ranking) # Save results to a file
    

    
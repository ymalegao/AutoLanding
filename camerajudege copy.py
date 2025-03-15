from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


rural_Scenario_names = ["Rural1-AfricaNoAnimals", "Rural2-AfricaWithAnimals", "Rural3-AfricaTrees","Rural4-CoastlineRoundAbout", "Rural5-CoastlineBridge" ] #4

urban_scenario_names = ["Urban1- 4 Empty Rooftops", "Urban2 - FireOnRoof", "Urban3 - PeopleonRoof", "Urban3.5-PeopleonRooftops","Urban4-BurningWrittenOnRoof", "Urban5-NPeopleWrittenOnRoof", "Urban6-MiscTextWrittenOnRoof", "Urban7-Intersection"] #7

def raw_url_generator(scenario_name):
    #make sure to add %20 for spaces in the scenario name
    scen_name_with_space = scenario_name.replace(" ", "%20")
    url = f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/Scenarios/{scen_name_with_space}/output/rgb_labeled.png"
    return url


URL_arr = []

R_URL_arr = []

for scenario in urban_scenario_names:
    URL_arr.append(raw_url_generator(scenario))

for scenario in rural_Scenario_names:
    R_URL_arr.append(raw_url_generator(scenario))

# print(URL_arr[0])   



# Optimized prompt that accounts for all three images at once
# URBAN_PROMPT = """A quadcopter needs to perform an emergency landing.
# You are provided one camera image

# The image is divided into a 5×5 grid (A1 to E5).
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
    
URBAN_PROMPT = """A quadcopter needs to perform an emergency landing.
You are provided one camera image. 

The image is divided into a 5×5 grid (A1 to E5).
**Your Task:**
- Identify hazards (fire, debris, people) in each section.
- Rank the safest landing zones, prioritizing rooftops.
- **Do NOT land on the ground unless no rooftops are available.**
- **If an area has any obstacles (fire, people, debris), it is completely unsafe.**
- **Do NOT rank unsafe locations.** Instead, mention "NO SAFE LANDING SPOT" if all rooftops are obstructed.
- **Only rank completely clear zones** with a wide enough landing area.
- If the coordinate is between two safe zones, say "Rooftop between A1 and A2".
- **For each ranking, explain why it was chosen, using the format below.**

**Output Format:**
[
    {"position": "Best", "grid": "B1", "reason": "Large, clear rooftop with no obstacles."},
    {"position": "Second Best", "grid": "C1", "reason": "Same rooftop as B1, equally clear."},
    {"position": "Third Best", "grid": "D1", "reason": "Same rooftop as B1 and C1, but slightly smaller space."},
    {"position": "Fourth Best", "grid": "A1", "reason": "Clear rooftop but slightly closer to obstacles."},
    {"position": "NO SAFE LANDING SPOT", "reason": "All other areas have fire, people, or debris."}
]
"""

RURAL_PROMPT = """A quadcopter needs to perform an emergency landing in a rural environment.
You are provided one camera image.

The image is divided into a 5×5 grid (A1 to E5).
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
    # rgb_url = URL_arr[7]
    rgb_url = R_URL_arr[4]
    print(rgb_url)
  
    response = client.chat.completions.create(
    model="gpt-4o",  # Supports vision
    messages=[
        {"role": "system", "content": RURAL_PROMPT},
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": rgb_url}}
            ]}
    ]
    )
    ranking = response.choices[0].message.content.strip()
    print(ranking)
    open("ranking.txt", "w").write(ranking) # Save results to a file
    

    
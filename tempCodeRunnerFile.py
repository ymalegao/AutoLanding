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

def real_life_raw_url_generator(scenario_name):
    #make sure to add %20 for spaces in the scenario name
    scen_name_with_space = scenario_name.replace(" ", "%20")
    urls =[f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/RealLifeScenario/output_7/rgb_labeled.png", f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/RealLifeScenario/output_7/color_depth_labeled.png", f"https://raw.githubusercontent.com/ymalegao/AutoLanding/main/RealLifeScenario/output_7/segmentation_labeled.png"]
    return urls


URL_arr = []

R_URL_arr = []

RL_URL_arr = []

for scenario in urban_scenario_names:
    URL_arr.append(raw_url_generator(scenario))

for scenario in rural_Scenario_names:
    R_URL_arr.append(raw_url_generator(scenario))

RL_URL_arr.append(real_life_raw_url_generator("RealLifeScenario"))

print(RL_URL_arr[0][0])
print(RL_URL_arr[0][1])
print(RL_URL_arr[0][2])
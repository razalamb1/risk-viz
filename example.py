"""Example utilizing source code.

Utilizes source code to graph heat maps for Hypertension, Smoking, and
Obesity in Montgomery County, Maryland. Uses three distinct color maps,
and images are saved into the images folder.
"""

from src.heat_maps import full_process
from dotenv import load_dotenv
import os

load_dotenv()
token = os.environ.get("TOKEN")


columns = [
    "BPHIGH_CrudePrev",
    "CSMOKING_CrudePrev",
    "OBESITY_CrudePrev",
    "DIABETES_CrudePrev",
    "LPA_CrudePrev",
    "SLEEP_CrudePrev",
]
names = [
    "Hypertension",
    "Current Smokers",
    "Obesity",
    "Diabetes",
    "Physical Inactivity",
    "Less than 7 Hours of Sleep",
]
cmaps = ["Purples", "Blues", "Greens", "Reds", "YlOrBr", "Oranges"]

states = [
    # "Alaska",
    "Alabama",
    "Arkansas",
    "Arizona",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Iowa",
    "Idaho",
    "Illinois",
    "Indiana",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Massachusetts",
    "Maryland",
    "Maine",
    "Michigan",
    "Minnesota",
    "Missouri",
    "Mississippi",
    "Montana",
    "North Carolina",
    "North Dakota",
    "Nebraska",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "Nevada",
    "New York",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Virginia",
    "Vermont",
    "Washington",
    "Wisconsin",
    "West Virginia",
    "Wyoming",
]

for i in states:
    full_process(
        columns,
        names,
        state=i,
        cmaps=cmaps,
        token=token,
        tract=False,
    )

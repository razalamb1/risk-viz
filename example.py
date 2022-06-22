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
]
names = [
    "Hypertension",
    "Current Smokers",
    "Obesity",
]
cmaps = ["Purples", "Blues", "Reds"]
full_process(
    columns,
    names,
    "Maryland",
    "Montgomery",
    cmaps=cmaps,
    token=token,
)

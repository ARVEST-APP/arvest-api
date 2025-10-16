"""
Export to csv an annotation list
"""

import arvestapi
from utils import read_login, write_csv
import os
import re

PROJECT_NAME = "meta projet"
OUTPUT_DEST = os.path.join(os.getcwd(), f"{PROJECT_NAME}_annotation-list.csv")

# Login
EMAIL, PASSWORD = read_login("examples/login/jh-perso.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

annos = [['type', 'label', 'creator', 'date', 'dims', 'target']]

def parse_svg_string(input):
    coords = re.findall(r"[-+]?[0-9]*\.?[0-9]+", input)
    return [(float(coords[i]), float(coords[i+1])) for i in range(0, len(coords)-1, 2)]

# Get project:
projects = ar.get_projects()
for project in projects:
    if project.title == PROJECT_NAME:

        annotation_list = project.user_workspace.get_annotations()
        for an in annotation_list:
            if an.annotation_type == "server":
                annos.append([
                    's', 
                    an.body[0]["value"], 
                    an.creator,
                    an.creation_date,
                    parse_svg_string(an.target["selector"][0]["value"]),
                    an.target["selector"][1]["value"]
                ])
        for an in annotation_list:
            if an.annotation_type == "manifest":
                annos.append([
                    'm', 
                    an.body["value"], 
                    "-",
                    "-",
                    "-",
                    an.target
                ])

write_csv(OUTPUT_DEST, annos)
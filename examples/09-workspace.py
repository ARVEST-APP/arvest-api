import arvestapi
import os
from utils import read_login, write_json

ar = arvestapi.Arvest("arvestuser@gmail.com", "arvestworkshop000")

# Get a list of all of your projets using the get_projects() method:
my_projects = ar.get_projects()

for project in my_projects:
    if project.title == "Pina Bausch's Café Müller":
        write_json(os.path.join(os.getcwd(), "WORSPACE.json"), project.user_workspace.to_dict())

import arvestapi
from utils import read_login

PROJECT_NAME = "meta projet"

# Login
EMAIL, PASSWORD = read_login("examples/login/jh-perso.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Get project:
projects = ar.get_projects()
for project in projects:
    if project.title == PROJECT_NAME:
        annotations = project.get_annotations()
        print(len(annotations))

        for annotation in annotations:
            print(annotation.id)
            print(annotation.body)
            print()
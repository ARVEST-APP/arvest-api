import arvestapi
from utils import read_login, write_json
import os

PROJECT_NAME = "Elevage 2"

# Login
EMAIL, PASSWORD = read_login("examples/login/jh-fac.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Get project:
projects = ar.get_projects()
for project in projects:
    if project.title == PROJECT_NAME:
        print(f"Found \"{project.title}\" (project id: {project.id}). Extracting annotations...\n")

        # Save all annotations as json:
        project_annotations = project.user_workspace.annotations
        write_json(os.path.join(os.getcwd(), f"{project.title}_{project.id}_workspace.json"), project.user_workspace.to_dict())

        # # Parse annotations:
        # annotation_list = project.user_workspace.get_annotations()
        # print(f"Found {len(annotation_list)} annotations.")
        # for an in annotation_list:
        #     print(an.id)
        # print()

        # # Or you can always do it manually:
        # server_count = 0
        # manifest_count = 0
        # for canvas_id in project_annotations.items:
        #     for annotation_page_id in project_annotations.items[canvas_id]:
        #         for annotation in project_annotations.items[canvas_id][annotation_page_id].json["items"]:
        #             print(annotation.id)
        #             if annotation.annotation_type == "server":
        #                 server_count = server_count + 1
        #             else:
        #                 manifest_count = manifest_count + 1
        # print(f"\nFound {server_count} server annotations and {manifest_count} manifest annotations.")
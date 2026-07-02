from .utils import debug_print_response_body
from .user_workspace import UserWorkspace, Annotation
import requests
from typing import List
import os
import urllib.parse

class Project:
    def __init__(self, **kwargs) -> None:
        """Represents an Arvest project."""
        
        self.debug = kwargs.get("debug", False)
        
        self.arvest_version = kwargs.get("arvest_version", None)
        self.id = kwargs.get("id", None)
        self.title = kwargs.get("title", None)
        self.owner_id = kwargs.get("owner_id", None)
        self.thumbnail_url = kwargs.get("thumbnail_url", None)
        self.description = kwargs.get("description", None)
        self.user_workspace = kwargs.get("user_workspace", None)
        self.metadata = kwargs.get("metadata", None)
        self.created_at = kwargs.get("created_at", None)
        self.snapshot_hash = kwargs.get("snapshot_hash", None)
        self.locked_by_user_id = kwargs.get("locked_by_user_id", None)
        self.locked_at = kwargs.get("locked_at", None)
        self._arvest_instance = kwargs.get("arvest_instance", None)

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the project properties with a request response."""

        debug_print_response_body(response_body, self)

        self.id = response_body["project"]["id"]
        self.arvest_version = response_body["project"]["arvestVersion"]
        self.title = response_body["project"]["title"]
        self.description = response_body["project"]["description"]
        self.thumbnail_url = response_body["project"]["thumbnailUrl"]
        self.owner_id = response_body["project"]["ownerId"]
        # self.user_workspace = UserWorkspace(response_body = response_body["project"]["userWorkspace"])
        self.user_workspace = response_body["project"]["userWorkspace"]
        self.metadata = response_body["project"]["metadata"]
        self.created_at = response_body["project"]["created_at"]
        self.snapshot_hash = response_body["project"]["snapShotHash"]
        self.locked_by_user_id = response_body["project"]["lockedByUserId"]
        self.locked_at = response_body["project"]["lockedAt"]

    def to_dict(self) -> dict:
        return {
            "project" : {
                "arvestVersion" : self.arvest_version,
                "id" : self.id,
                "title" : self.title,
                "description" : self.description,
                "thumbnailUrl" : self.thumbnail_url,
                "ownerId" : self.owner_id,
                "userWorkspace" : self.user_workspace,
                "metadata" : self.metadata,
                "created_at" : self.created_at,
                "snapShotHash" : self.snapshot_hash,
                "lockedByUserId" : self.locked_by_user_id,
                "lockedAt" : self.locked_at
            },
            "group" : self._arvest_instance._personal_group.to_dict()
        }

    def _update_distant_from_self(self) -> None:
        """Update the object on the server from current python object."""

        # TODO Add updated at parsing to this!

        if self._arvest_instance != None:
                
            url = f"{self._arvest_instance._arvest_prefix}/link-group-project/updateProject"
            payload = self.to_dict()

            response = requests.patch(url, headers = self._arvest_instance._auth_header, json = payload)

            if response.status_code == 200:
                pass
            else:
                print("Unable to update manifest.")
                print(f"Status code: {response.status_code}. Response: {response.json()}")
                return None
        else:
            print("Unable to update Manifest as there is no known Arvest instance context.")

    def update_title(self, new_title : str) -> None:
        """Update the title of the Manifest object."""
        self.title = new_title
        self._update_distant_from_self()

    def update_description(self, new_description : str) -> None:
        """Update the desciption of the Media object."""
        self.description = new_description
        self._update_distant_from_self()

    def update_thumbnail_url(self, new_thumbnail : str) -> None:
        """Update the thumbnail url of the Manifest object."""
        self.thumbnail_url = new_thumbnail
        self._update_distant_from_self()

    def update_workspace(self, new_workspace : str) -> None:
        """Update the workspace of the Manifest object."""
        self.arvest_version = 2
        self.user_workspace = new_workspace
        self._update_distant_from_self()

    def remove(self):
        url = f"{self._arvest_instance._arvest_prefix}/link-group-project/delete/project/{self.id}"  
        response = requests.delete(url, headers = self._arvest_instance._auth_header)

        if response.status_code == 200:
            pass
        else:
            print("Unable to delete manifest.")
            return None
        
    def get_metadata(self):
        """Return the project's metadata."""

        url = f"{self._arvest_instance._arvest_prefix}/metadata/project/{self.id}"
        response = requests.get(url, headers = self._arvest_instance._auth_header)

        if response.status_code == 200:
            if len(response.json()) > 0:
                return response.json()[0]["metadata"]
            else:
                return self._arvest_instance.get_metadata_formats()[0].to_setter_dict()["metadata"]
            
            #return Profile(response_body = response.json(), debug = self.debug)
        else:
            print("Unable to get project metadata.")
            return None
        
    def update_metadata(self, fields : dict = {}, **kwargs):
        """Update the project's metadata."""

        metadata_format = kwargs.get("metadata_format", self._arvest_instance.get_metadata_formats()[0])
        setter_dict = metadata_format.to_setter_dict(fields)
        setter_dict["objectId"] = self.id
        setter_dict["objectTypes"] = "project"

        url = f"{self._arvest_instance._arvest_prefix}/metadata"
        response = requests.post(url, json = setter_dict, headers = self._arvest_instance._auth_header)
        
        if response.status_code == 201:
            pass
        else:
            print("Unable to update metadata.")
            return None
        
    def get_annotations(self) -> List[Annotation]:
        """Return a list of all Annotations for all canvases for all of the manifests in the projects catalog."""

        manifest_list = []
        for item in self.user_workspace.catalog:
            manifest_list.append(item["manifestId"])

        canvas_list = []
        for manifest_id in manifest_list:
            man = self.user_workspace.manifests[manifest_id]["json"]
            api_ver = 3 
            if "@context" in man:
                if man["@context"] != None:
                    if "2" in man["@context"]:
                        api_ver = 2
            elif "context" in man:
                if man["context"] != None:
                    if "2" in man["context"]:
                        api_ver = 2
            
            if api_ver == 3:
                for item in man["items"]:
                    canvas_list.append(item["id"])
            else:
                for item in man["sequences"][0]["canvases"]:
                    canvas_list.append(item["@id"])

        annotation_list = []
        for canvas_id in canvas_list:
            canvas_id_sanitized = os.path.join(canvas_id, "annotationPage")
            canvas_id_sanitized = urllib.parse.quote(canvas_id_sanitized, safe='')
            url = f"{self._arvest_instance._arvest_prefix}/annotation-page/{canvas_id_sanitized}/{self.id}"  
            response = requests.get(url, headers = self._arvest_instance._auth_header)
            if response.status_code == 200:
                if response.json() != []:
                    for item in response.json()[0]['content']['items']:
                        annotation_list.append(Annotation(response_body = item))
            
        return annotation_list

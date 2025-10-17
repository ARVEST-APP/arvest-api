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
        self.id = kwargs.get("id", None)
        self.title = kwargs.get("title", None)
        self.owner_id = kwargs.get("owner_id", None)
        self.thumbnail_url = kwargs.get("thumbnail_url", None)
        self.description = kwargs.get("description", None)
        self.user_workspace = kwargs.get("user_workspace", UserWorkspace())
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
        self.title = response_body["project"]["title"]
        self.description = response_body["project"]["description"]
        self.thumbnail_url = response_body["project"]["thumbnailUrl"]
        self.owner_id = response_body["project"]["ownerId"]
        self.user_workspace = UserWorkspace(response_body = response_body["project"]["userWorkspace"])
        self.metadata = response_body["project"]["metadata"]
        self.created_at = response_body["project"]["created_at"]
        self.snapshot_hash = response_body["project"]["snapShotHash"]
        self.locked_by_user_id = response_body["project"]["lockedByUserId"]
        self.locked_at = response_body["project"]["lockedAt"]

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
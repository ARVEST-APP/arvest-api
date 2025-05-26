from .utils import debug_print_response_body
import requests
import os

class Manifest:
    def __init__(self, **kwargs) -> None:
        """Represents an Arvest project."""
        
        self.debug = kwargs.get("debug", False)
        self.id = kwargs.get("id", None)
        self.url = kwargs.get("url", None)
        self.path = kwargs.get("path", None)
        self.thumbnail_url = kwargs.get("thumbnail_url", None)
        self.hash = kwargs.get("hash", None)
        self.title = kwargs.get("title", None)
        self.metadata = kwargs.get("metadata", None)
        self.origin = kwargs.get("origin", None)
        self.description = kwargs.get("description", None)
        self.id_creator = kwargs.get("id_creator", None)
        self.created_at = kwargs.get("created_at", None)
        self.updated_at = kwargs.get("origin", None)
        self._arvest_resource_prefix = kwargs.get("arvest_resource_prefix", "https://resource.arvest.app")
        self._arvest_instance = kwargs.get("arvest_instance", None)
        self._arvest_workspace_prefix = kwargs.get("arvest_workspace_prefix", "https://workspace.arvest.app")

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "url" : self.url,
            "path" : self.path,
            "thumbnailUrl" : self.thumbnail_url,
            "hash" : self.hash,
            "title" : self.title,
            "metadata" : self.metadata,
            "origin" : self.origin,
            "description" : self.description,
            "idCreator" : self.id_creator,
            "created_at" : self.created_at,
            "updated_at" : self.updated_at
        }

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the project properties with a request response."""

        debug_print_response_body(response_body, self)

        self.id = response_body["id"]
        self.url = response_body["url"]
        self.path = response_body["path"]
        self.thumbnail_url = response_body["thumbnailUrl"]
        self.hash = response_body["hash"]
        self.title = response_body["title"]
        self.metadata = response_body["metadata"]
        self.origin = response_body["origin"]
        self.description = response_body["description"]
        self.id_creator = response_body["idCreator"]
        self.created_at = response_body["created_at"]
        self.updated_at = response_body["updated_at"]

    def get_full_url(self) -> str:
        """Get the full url to where a Manifest is stored online."""
        if self.origin == "upload" or self.origin == "create":
            return f"{self._arvest_resource_prefix}/{self.hash}/{self.path}"
        elif self.origin == "link":
            return self.url
    
    def get_content(self) -> dict:
        """Return the IIIF Manifest content as a python dict."""

        response = requests.get(self.get_full_url())

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Unable to retrieve Manifest content at url \"{self.get_full_url()}\".")
            return None
        
    def update_content(self, content : dict, **kwargs) -> None:
        """
        Update the a created or uploaded Manifest's content.
        
        kwargs
        - update_id (bool) : default False, set to True to update all ids.
        """

        if self.origin == "upload" or self.origin == "create":
            if self._arvest_instance != None:
                
                url = f"{self._arvest_instance._arvest_prefix}/link-manifest-group/manifest/updateJson"
                payload = {
                    "json" : content,
                    "manifestId" : self.id,
                    "origin" : self.origin,
                    "path" : self.path,
                    "hash" : self.hash
                }

                response = requests.patch(url, headers = self._arvest_instance._auth_header, json = payload)

                if response.status_code == 200:
                    if kwargs.get("update_id", False):
                        self.update_id(self.get_full_url())
                        return self
                    else:
                        return self
                else:
                    print(f"Status code: {response.status_code}. Response: {response.json()}")
                    print("Unable to update json data.")
                    return None
            else:
                print("Unable to update Manifest as there is no known Arvest instance context.")
        elif self.origin == "link":
            print("Cannot update a linked Manifest.")

    def _update_distant_from_self(self) -> None:
        """Update the object on the server from current python object."""

        # TODO Add updated at parsing to this!

        if self._arvest_instance != None:
                
            url = f"{self._arvest_instance._arvest_prefix}/link-manifest-group/manifest"
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

    def get_preview_url(self) -> str:
        """Return a url that allows you to consult the Manifest directly in a Mirador winbdow."""
        if self.origin == "upload" or self.origin == "create":
            return f"{self._arvest_workspace_prefix}/manifest/{self.hash}/{self.path}"
        elif self.origin == "link":
            return f"{self._arvest_workspace_prefix}/manifest/{self.url}"

    def get_metadata(self):
        """Return the manifest's metadata."""

        url = f"{self._arvest_instance._arvest_prefix}/metadata/manifest/{self.id}"
        response = requests.get(url, headers = self._arvest_instance._auth_header)

        if response.status_code == 200:
            if len(response.json()) > 0:
                return response.json()[0]["metadata"]
            else:
                return self._arvest_instance.get_metadata_formats()[0].to_setter_dict()["metadata"]
            
            #return Profile(response_body = response.json(), debug = self.debug)
        else:
            print("Unable to get manifest metadata.")
            return None
        
    def update_metadata(self, fields : dict = {}, **kwargs):
        """Update the manifest's metadata."""

        metadata_format = kwargs.get("metadata_format", self._arvest_instance.get_metadata_formats()[0])
        setter_dict = metadata_format.to_setter_dict(fields)
        setter_dict["objectId"] = self.id
        setter_dict["objectTypes"] = "manifest"

        url = f"{self._arvest_instance._arvest_prefix}/metadata"
        response = requests.post(url, json = setter_dict, headers = self._arvest_instance._auth_header)
        
        if response.status_code == 201:
            pass
        else:
            print("Unable to update metadata.")
            return None
        
    def update_id(self, new_id):
        """
        This will do two things:
        - Replace the Manifest's id with the new id
        - Go through all of the items and annotations, and replace the ids and targets 
        which have the string `"/canvas/"` in them with 
        `{new_id(removing .json)}/canvas/{the rest of the id}`
        
        - new_id (str) : the new url ending with .json for the manifest.
        """

        original_content = self.get_content()
        original_content["id"] = new_id

        self._update_id_lower(original_content, os.path.splitext(new_id)[0])

        self.update_content(original_content)
        
    def _update_id_lower(self, content, new_id_prefix):
        if "items" in content:
            for item in content["items"]:
                
                if "id" in item:
                    if "/canvas/" in item["id"]:
                        previous_id = item["id"]
                        id_suffix = "/canvas/" + previous_id.split("/canvas/")[1]
                        new_id = new_id_prefix + id_suffix

                        item["id"] = new_id

                if "target" in item:
                    if "/canvas/" in item["target"]:
                        previous_id = item["target"]
                        id_suffix = "/canvas/" + previous_id.split("/canvas/")[1]
                        new_id = new_id_prefix + id_suffix

                        item["target"] = new_id

                self._update_id_lower(item, new_id_prefix)
        
        if "annotations" in content:
            if content["annotations"] != None:
                for item in content["annotations"]:
                    
                    if "id" in item:
                        if "/canvas/" in item["id"]:
                            previous_id = item["id"]
                            id_suffix = "/canvas/" + previous_id.split("/canvas/")[1]
                            new_id = new_id_prefix + id_suffix

                            item["id"] = new_id

                    if "target" in item:
                        if "/canvas/" in item["target"]:
                            previous_id = item["target"]
                            id_suffix = "/canvas/" + previous_id.split("/canvas/")[1]
                            new_id = new_id_prefix + id_suffix

                            item["target"] = new_id

                    self._update_id_lower(item, new_id_prefix)

    def remove(self):
        url = f"{self._arvest_instance._arvest_prefix}/link-manifest-group/manifest/{self.id}"  
        response = requests.delete(url, headers = self._arvest_instance._auth_header)

        if response.status_code == 200:
            pass
        else:
            print("Unable to delete manifest.")
            return None
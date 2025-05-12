from .utils import debug_print_response_body
import requests

class Media:
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

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))

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
    
    def get_full_url(self) -> str:
        """Get the full url to where a Media is stored online."""
        if self.origin == "upload":
            return f"{self._arvest_resource_prefix}/{self.hash}/{self.path}"
        elif self.origin == "link":
            return self.url
        
    def _update_distant_from_self(self) -> None:
        """Update the object on the server from current python object."""

        # TODO Add updated at parsing to this!

        if self._arvest_instance != None:
                
            url = f"{self._arvest_instance._arvest_prefix}/link-media-group/media"
            payload = self.to_dict()

            response = requests.patch(url, headers = self._arvest_instance._auth_header, json = payload)

            if response.status_code == 200:
                pass
            else:
                print("Unable to update media.")
                return None
        else:
            print("Unable to update Media as there is no known Arvest instance context.")
        
    def update_title(self, new_title : str) -> None:
        """Update the title of the Media object."""
        self.title = new_title
        self._update_distant_from_self()

    def update_description(self, new_description : str) -> None:
        """Update the desciption of the Media object."""
        self.description = new_description
        self._update_distant_from_self()

    def update_thumbnail_url(self, new_thumbnail : str) -> None:
        """Update the thumbnail url of the Media object."""
        self.thumbnail_url = new_thumbnail
        self._update_distant_from_self()

    def get_metadata(self):
        """Return the media's metadata."""

        url = f"{self._arvest_instance._arvest_prefix}/metadata/media/{self.id}"
        response = requests.get(url, headers = self._arvest_instance._auth_header)

        if response.status_code == 200:
            if len(response.json()) > 0:
                return response.json()[0]["metadata"]
            else:
                return self._arvest_instance.get_metadata_formats()[0].to_setter_dict()["metadata"]
            
            #return Profile(response_body = response.json(), debug = self.debug)
        else:
            print("Unable to get media metadata.")
            return None
        
    def update_metadata(self, fields : dict = {}, **kwargs):
        """Update the media's metadata."""

        metadata_format = kwargs.get("metadata_format", self._arvest_instance.get_metadata_formats()[0])
        setter_dict = metadata_format.to_setter_dict(fields)
        setter_dict["objectId"] = self.id
        setter_dict["objectTypes"] = "media"

        url = f"{self._arvest_instance._arvest_prefix}/metadata"
        response = requests.post(url, json = setter_dict, headers = self._arvest_instance._auth_header)
        
        if response.status_code == 201:
            pass
        else:
            print("Unable to update metadata.")
            return None
    
    def remove(self):
        url = f"{self._arvest_instance._arvest_prefix}/link-media-group/media/{self.id}"  
        response = requests.delete(url, headers = self._arvest_instance._auth_header)

        if response.status_code == 200:
            pass
        else:
            print("Unable to delete manifest.")
            return None
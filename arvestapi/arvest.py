import requests
from .profile import Profile
from .group import Group
from .project import Project
from .media import Media
from .manifest import Manifest
from .metadata_format import MetadataFormat
import os
import mimetypes
import json
from datetime import datetime

class Arvest:
    def __init__(self, email : str, password : str, **kwargs) -> None:
        """
        The Arvest class is your main point of entry. Use it to create an instance of your Arvest account.
        """
        
        self.debug = kwargs.get("debug", False)
        self.email = email
        self.password = password
        self.access_token = kwargs.get("access_token", None)
        self._arvest_prefix = kwargs.get("arvest_prefix", "https://api.arvest.app")
        self._auth_header = None

        if self.access_token == None:
            self.access_token = self._get_access_token()
            if self.access_token != None:
                self._auth_header = {"Authorization" : f"Bearer {self.access_token}"}

        self.profile = self._get_profile()
        self._personal_group = self._get_personal_group()

    def _get_access_token(self) -> None:
        """Connect to the Arvest account and get the user's access token."""

        url = f"{self._arvest_prefix}/auth/login"
        body = {"mail" : self.email, "password" : self.password}

        response = requests.post(url, json = body)
        
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print("Unable to connect to Arvest and collect access token. Please check your login credentials.")
            return None

    def _get_profile(self) -> Profile:
        """Return the user profile info."""

        url = f"{self._arvest_prefix}/auth/profile"
        response = requests.get(url, headers = self._auth_header)

        if response.status_code == 200:
            return Profile(response_body = response.json(), debug = self.debug)
        else:
            print("Unable to get user profile.")
            return None
        
    def _get_personal_group(self) -> Group:
        """Return the user's personal group."""
        
        if self.profile != None:
            url = f"{self._arvest_prefix}/link-user-group/user-personal-group/{str(self.profile.id)}"
            
            response = requests.get(url, headers = self._auth_header)
            
            if response.status_code == 200:
                return Group(response_body = response.json(), debug = self.debug)
            else:
                print("Unable to get user personal group.")
                return None
        else:
            print("Unable to get personal user group because the user profile was not found.")
            return None
        
    def get_projects(self, **kwargs) -> list[Project]:
        """
        Return a list of the user's projects.
        
        ## kwargs
        - group_id (int) : the id of the group's projects (by default, the user's personal group)
        """

        if self._personal_group != None:
            url = f"{self._arvest_prefix}/link-group-project/{str(kwargs.get('group_id', self._personal_group.id))}"
            response = requests.get(url, headers = self._auth_header)
            if response.status_code == 200:
                ret = []
                for item in response.json():
                    ret.append(Project(response_body = item, debug = self.debug, arvest_instance = self))
                return ret
            else:
                print("Unable to get projects.")
                return None
        else:
            print("Unable to get projects because unable to find personal user group.")
            return None
        
    def get_medias(self, **kwargs) -> list[Media]:
        """
        Return a list of the user's media.
        
        ## kwargs
        - group_id (int) : the id of the group's projects (by default, the user's personal group)
        """

        if self._personal_group != None:
            url = f"{self._arvest_prefix}/link-media-group/medias"#/{str(kwargs.get('group_id', self._personal_group.id))}"
            response = requests.get(url, headers = self._auth_header)
        
            if response.status_code == 200:
                ret = []
                for item in response.json():
                    ret.append(Media(response_body = item, debug = self.debug, arvest_instance = self))
                return ret
            else:
                print("Unable to get media.")
                return None
        else:
            print("Unable to get media because unable to find personal user group.")
            return None
        
    def get_manifests(self, **kwargs) -> list[Manifest]:
        """
        Return a list of the user's manifests.
        
        ## kwargs
        - group_id (int) : the id of the group's projects (by default, the user's personal group)
        """

        if self._personal_group != None:
            url = f"{self._arvest_prefix}/link-manifest-group/manifests"#group/{str(kwargs.get('group_id', self._personal_group.id))}"
            response = requests.get(url, headers = self._auth_header)

            if response.status_code == 200:
                ret = []
                for item in response.json():
                    ret.append(Manifest(response_body = item, debug = self.debug, arvest_instance = self))
                return ret
            else:
                print("Unable to get manifests.")
                return None
        else:
            print("Unable to get manifests because unable to find personal user group.")
            return None
        
    def create_project(self, **kwargs) -> Project:
        """
        Create a new arvest project.
        
        ## kwargs
        - title (str) : project title
        - user_workspace (dict) : mirador workspace
        - metadata (dict) : ad hoc metadata
        - owner_id (int) : the group owner of the project (by default, the user's personal group)
        """

        if self._personal_group != None:
            url = f"{self._arvest_prefix}/link-group-project/project"
            
            body = {
                "title" : kwargs.get("title", ""),
                "userWorkspace" : kwargs.get("user_workspace", None),
                "ownerId" : kwargs.get("owner_id", self.profile.id),
                "metadata" : kwargs.get("metadata", {})
            }
            response = requests.post(url, json = body, headers = self._auth_header)
            
            if response.status_code == 201:
                return Project(response_body = response.json(), debug = self.debug, arvest_instance = self)
            else:
                print("Unable to create project.")
                return None

    def add_media(self, **kwargs) -> Media:
        """
        Upload a new media either with a link or path on your local machine.
        
        ## kwargs
        - path (str) : url or path on local machine to media.
        """

        if self._personal_group != None:
            
            if os.path.isfile(kwargs.get("path", None)):
                # Local file:

                url = f"{self._arvest_prefix}/link-media-group/media/upload"

                data = {
                    "idCreator" : kwargs.get("owner_id", self.profile.id),
                    "user_group" : kwargs.get("user_group", json.dumps(self._personal_group.to_dict()))
                }

                with open(kwargs.get("path", None), 'rb') as file:
                    file_name = os.path.basename(kwargs.get("path", None))
                    content_type, _ = mimetypes.guess_type(kwargs.get("path", None))
                    files = {
                        "file": (
                            file_name, 
                            file,
                            content_type)
                    }

                    response = requests.post(url, headers = self._auth_header, files = files, data = data)
            
            else:
                # Link file:

                url = f"{self._arvest_prefix}/link-media-group/media/link"
                
                body = {
                    "url" : kwargs.get("path", None),
                    "idCreator" : kwargs.get("owner_id", self.profile.id),
                    "user_group" : kwargs.get("user_group", self._personal_group.to_dict())
                }
            
                response = requests.post(url, json = body, headers = self._auth_header)
            
            if response.status_code == 201:
                return Media(response_body = response.json()["media"], debug = self.debug, arvest_instance = self)
            else:
                print("Unable to add media.")
                print(f"Status code: {response.status_code}. Response: {response.json()}")
                return None
            
    def add_manifest(self, **kwargs) -> Manifest:
        """
        Upload a new IIIF Manifest either with a link or path on your local machine.
        (use create_manifest for creating using Arvest's tools).
        
        ## kwargs
        - path (str) : url or path on local machine to media.
        - update_id (bool) : default False, set to True to update all ids.
        """

        if self._personal_group != None:
            
            if os.path.isfile(kwargs.get("path", None)):
                pass
                # Local file:

                url = f"{self._arvest_prefix}/link-manifest-group/manifest/upload"

                data = {
                    "idCreator" : kwargs.get("owner_id", self.profile.id)
                }

                with open(kwargs.get("path", None), 'rb') as file:
                    file_name = os.path.basename(kwargs.get("path", None))
                    content_type, _ = mimetypes.guess_type(kwargs.get("path", None))
                    files = {
                        "file": (
                            file_name, 
                            file,
                            content_type)
                    }

                    response = requests.post(url, headers = self._auth_header, files = files, data = data)
            
            else:
                # Link file:

                url = f"{self._arvest_prefix}/link-manifest-group/manifest/link"

                # TODO Could add a get on the manifest here to get title
                body = {
                    "url" : kwargs.get("path", None),
                    "path" : kwargs.get("path", None),
                    "idCreator" : kwargs.get("owner_id", self.profile.id),
                    "title" : kwargs.get("title", "Linked manifest"),
                    "rights" : kwargs.get("rights", "admin")
                }
            
                response = requests.post(url, json = body, headers = self._auth_header)
            
            if response.status_code == 201:

                # TODO Hopefully this will be updated in the API, workaround currently:
                created_manifest = self.get_latest_manifest()
                # return Manifest(response_body = response.json(), debug = self.debug)

                if kwargs.get("update_id", False):
                    created_manifest.update_id(created_manifest.get_full_url())
                    return created_manifest
                else:
                    return created_manifest
            else:
                print("Unable to add manifest.")
                return None
            
    def get_manifest(self, manifest_id) -> Manifest:
        """Return a manifest according to id."""

        # TODO, This seems suspicious, cf swagger notice: "get all group tha can access a manifest with his id"

        url = f"{self._arvest_prefix}/link-manifest-group/manifest/{manifest_id}"
        response = requests.get(url, headers = self._auth_header)

        if response.status_code == 200:
            return Manifest(response_body = response.json()[0]["manifest"], debug = self.debug, arvest_instance = self)
        else:
            print("Unable to get user profile.")
            return None
    
    def get_latest_manifest(self) -> Manifest:
        """Return the most recently created Manifest."""

        return max(
            self.get_manifests(),
            key=lambda obj: datetime.strptime(obj.created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        )
    
    def get_metadata_formats(self) -> list[MetadataFormat]:
        """Retrieve the user's metadata formats."""

        url = f"{self._arvest_prefix}/link-metadata-format-group/{self.profile.id}"
        response = requests.get(url, headers = self._auth_header)

        if response.status_code == 200:
            ret = []
            for item in response.json():
                ret.append(MetadataFormat(response_body = item, debug = self.debug, arvest_instance = self))
            return ret
        else:
            print("Unable to get metadata formats.")
            return None
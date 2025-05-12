from .utils import debug_print_response_body
from .user_workspace import UserWorkspace
import requests

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
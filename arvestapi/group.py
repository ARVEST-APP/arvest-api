from .utils import debug_print_response_body

class Group:
    def __init__(self, **kwargs) -> None:
        """Represents an Arvest group."""
        
        self.debug = kwargs.get("debug", False)
        self.id = kwargs.get("id", None)
        self.title = kwargs.get("title", None)
        self.owner_id = kwargs.get("owner_id", None)
        self.thumbnail_url = kwargs.get("thumbnail_url", None)
        self.description = kwargs.get("description", None)
        self.type = kwargs.get("type", None)
        self.created_at = kwargs.get("created_at", None)

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:
        return {
            "created_at" : self.created_at,
            "description" : self.description,
            "id" : self.id,
            "ownerId" : self.owner_id,
            "thumbnailUrl" : self.thumbnail_url,
            "title" : self.title,
            "type" : self.type
        }

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the group properties with a request response."""

        debug_print_response_body(response_body, self)

        self.id = response_body["id"]
        self.title = response_body["title"]
        self.owner_id = response_body["ownerId"]
        self.thumbnail_url = response_body["thumbnailUrl"]
        self.description = response_body["description"]
        self.type = response_body["type"]
        self.created_at = response_body["created_at"]
from .utils import debug_print_response_body

class MetadataFormat:
    def __init__(self, **kwargs) -> None:
        """Represents an Arvest metadata format."""
        
        self.debug = kwargs.get("debug", False)

        self.id = kwargs.get("id", None)
        self.title = kwargs.get("title", None)
        self.creator_id = kwargs.get("creator_id", None)
        self.metadata = kwargs.get("metadata", None)

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "title" : self.title,
            "creatorId" : self.creator_id,
            "metadata" : self.metadata
        }
    
    def to_setter_dict(self, fields : dict = {}) -> dict:
        """Return a dict that can be used to update an object's metadata."""

        ret = {
            "metadataFormatTitle" : self.title,
            "metadata" : {}
        }

        for item in self.metadata:
            if item["term"] in fields:
                ret["metadata"][item["term"]] = fields[item["term"]]
            else:
                ret["metadata"][item["term"]] = ""
        
        return ret

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the metadata format properties with a request response."""

        debug_print_response_body(response_body, self)

        self.id = response_body["id"]
        self.title = response_body["title"]
        self.creator_id = response_body["creatorId"]
        self.metadata = response_body["metadata"]
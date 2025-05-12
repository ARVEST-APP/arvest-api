from .utils import debug_print_response_body

class Profile:
    def __init__(self, **kwargs) -> None:
        """Represents an Arvest user profile."""
        
        self.debug = kwargs.get("debug", False)
        self.id = kwargs.get("id", None)
        self.mail = kwargs.get("mail", None)
        self.name = kwargs.get("name", None)
        self.is_admin = kwargs.get("is_admin", None)
        self.preferred_language = kwargs.get("preferred_language", None)

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the profile properties with a request response."""

        debug_print_response_body(response_body, self)

        self.id = response_body["id"]
        self.mail = response_body["mail"]
        self.name = response_body["name"]
        self.is_admin = response_body["_isAdmin"]
        self.preferred_language = response_body["preferredLanguage"]

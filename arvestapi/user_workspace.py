from .utils import debug_print_response_body
import uuid

class UserWorkspace:
    def __init__(self, **kwargs) -> None:
        """Represents a Mirador workspace."""
        
        self.debug = kwargs.get("debug", False)

        self.access_tokens = kwargs.get("access_tokens", {})
        self.annotations = kwargs.get("annotations", {})
        self.auth = kwargs.get("auth", {})
        self.catalog = kwargs.get("catalog", [])
        self.companion_windows = kwargs.get("companion_windows", {})
        self.config = kwargs.get("config", {})
        self.elastic_layout = kwargs.get("elastic_layout", {})
        self.errors = kwargs.get("errors", {"items" : []})
        self.info_responses = kwargs.get("info_responses", {})
        self.layers = kwargs.get("layers", {})
        self.manifests = kwargs.get("manifests", {})
        self.searches = kwargs.get("searches", {})
        self.viewers = kwargs.get("viewers", {})
        self.windows = kwargs.get("windows", {})
        self.workspace = kwargs.get("workspace", Workspace())

        if "response_body" in kwargs:
            if kwargs.get("response_body") != None:
                self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:

        return {
            "accessTokens" : self.access_tokens,
            "annotations" : self.annotations,
            "auth" : self.auth,
            "catalog" : self.catalog,
            "companionWindows" : self.companion_windows,
            "config" : self.config,
            "elasticLayout" : self.elastic_layout,
            "errors" : self.errors,
            "infoResponses" : self.info_responses,
            "layers" : self.layers,
            "manifests" : self.manifests,
            "searches" : self.searches,
            "viewers" : self.viewers,
            "windows" : self.windows,
            "workspace" : self.workspace.to_dict()
        }

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the properties with a request response."""

        debug_print_response_body(response_body, self)

        self.access_tokens = response_body["accessTokens"]
        self.annotations = response_body["annotations"]
        self.auth = response_body["auth"]
        self.catalog = response_body["catalog"]
        self.companion_windows = response_body["companionWindows"]
        self.config = response_body["config"]
        self.elastic_layout = response_body["elasticLayout"]
        self.errors = response_body["errors"]
        self.info_responses = response_body["infoResponses"]
        self.layers = response_body["layers"]
        self.manifests = response_body["manifests"]
        self.searches = response_body["searches"]
        self.viewers = response_body["viewers"]
        self.windows = response_body["windows"]
        self.workspace = Workspace(response_body = response_body["workspace"])
        
class Workspace:
    def __init__(self, **kwargs):
        
        self.debug = kwargs.get("debug", False)

        self.dragging_enabled = kwargs.get("dragging_enabled", True)
        self.allow_new_windows = kwargs.get("allow_new_windows", True)
        self.id = kwargs.get("id", str(uuid.uuid4())) # TODO Check this!
        self.is_workspace_add_visible = kwargs.get("is_workspace_add_visible", True)
        self.expose_mode_on = kwargs.get("expose_mode_on", False)
        self.width = kwargs.get("width", 5000)
        self.height = kwargs.get("height", 5000)
        self.show_zoom_controls = kwargs.get("show_zoom_controls", True)
        self.type = kwargs.get("type", "mosaic")
        self.viewport_position = kwargs.get("viewport_position", {"x" : 0, "y" : 0})
        self.window_ids = kwargs.get("window_ids", [])
        self.remove_resource_button = kwargs.get("remove_resource_button", True)

    def to_dict(self) -> dict:

        return {
            "draggingEnabled" : self.dragging_enabled,
            "allowNewWindows" : self.allow_new_windows,
            "id" : self.id,
            "isWorkspaceAddVisible" : self.is_workspace_add_visible,
            "exposeModeOn" : self.expose_mode_on,
            "height" : self.height,
            "showZoomControls" : self.show_zoom_controls,
            "type" : self.type,
            "viewportPosition" : self.viewport_position,
            "width" : self.width,
            "windowIds" : self.window_ids,
            "removeResourceButton" : self.remove_resource_button
        }

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the properties with a request response."""

        debug_print_response_body(response_body, self)

        self.dragging_enabled = response_body["draggingEnabled"]
        self.allow_new_windows = response_body["allowNewWindows"]
        self.id = response_body["id"]
        self.is_workspace_add_visible = response_body["isWorkspaceAddVisible"]
        self.expose_mode_on = response_body["exposeModeOn"]
        self.width = response_body["width"]
        self.height = response_body["height"]
        self.show_zoom_controls = response_body["showZoomControls"]
        self.type = response_body["type"]
        self.viewport_position = response_body["viewportPosition"]
        self.window_ids = response_body["windowIds"]
        self.remove_resource_button = response_body["removeResourceButton"]
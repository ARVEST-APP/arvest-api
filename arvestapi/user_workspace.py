from .utils import debug_print_response_body
import uuid
from typing import List

class UserWorkspace:
    def __init__(self, **kwargs) -> None:
        """Represents a Mirador workspace."""
        
        self.debug = kwargs.get("debug", False)

        self.access_tokens = kwargs.get("access_tokens", {})
        self.annotations = kwargs.get("annotations", MiradorAnnotationsList())
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
            "annotations" : self.annotations.to_dict(),
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
        self.annotations = MiradorAnnotationsList(response_body = response_body["annotations"])
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
    
    def get_annotations(self) -> List['Annotation']:
        ret = []
        for canvas_id in self.annotations.items:
            for annotation_page_id in self.annotations.items[canvas_id]:
                for annotation in self.annotations.items[canvas_id][annotation_page_id].json["items"]:
                    ret.append(annotation)
        return ret
        
class Workspace:
    def __init__(self, **kwargs) -> None:
        
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

        if "response_body" in kwargs:
            if kwargs.get("response_body") != None:
                self._parse_response_body(kwargs.get("response_body"))

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

class MiradorAnnotationsList:
    def __init__(self, **kwargs) -> None:
        
        self.debug = kwargs.get("debug", False)

        self.items = {}

        if "response_body" in kwargs:
            if kwargs.get("response_body") != None:
                self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:
        ret = {}
        for canvas_id in self.items:
            to_add = {}
            for annotation_id in self.items[canvas_id]:
                to_add[annotation_id] = self.items[canvas_id][annotation_id].to_dict()
            ret[canvas_id] = to_add
        return ret

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the properties with a request response."""

        debug_print_response_body(response_body, self)

        for canvas_id in response_body:
            for annotation_id in response_body[canvas_id]:
                if canvas_id not in self.items:
                    self.items[canvas_id] = {}
                self.items[canvas_id][annotation_id] = AnnotationPage(response_body = response_body[canvas_id][annotation_id])

class AnnotationPage:
    def __init__(self, **kwargs) -> None:
        
        self.debug = kwargs.get("debug", False)

        self.id = kwargs.get("id", "")
        self.is_fetching = kwargs.get("is_fetching", False)
        self.json = kwargs.get("json", [])

        if "response_body" in kwargs:
            if kwargs.get("response_body") != None:
                self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:
        ret = {
            "id" : self.id,
            "isFetching" : self.is_fetching
        }
        if self.json == []:
            ret["json"] = []
        else:
            ret["json"] = {}
            ret["json"]["id"] = self.json["id"]
            ret["json"]["type"] = self.json["type"]
            ret["json"]["items"] = []
            for item in self.json["items"]:
                ret["json"]["items"].append(item.to_dict())

        return ret

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the properties with a request response."""

        debug_print_response_body(response_body, self)

        self.id = response_body["id"]
        self.is_fetching = response_body["isFetching"]
        if response_body["json"] == []:
            self.json = []
        else:
            self.json = {}
            self.json["id"] = response_body["json"]["id"]
            self.json["type"] = response_body["json"]["type"]
            self.json["items"] = []
            for item in response_body["json"]["items"]:
                self.json["items"].append(Annotation(response_body = item))
        
class Annotation:
    def __init__(self, **kwargs) -> None:
        
        self.debug = kwargs.get("debug", False)

        self.id = kwargs.get("id", "")                             # m a
        self.motivation = kwargs.get("motivation", "commenting")   # m a
        self.target = kwargs.get("target", "")                     # m a
        self.body = kwargs.get("target", {})                       # m a
        self.type = kwargs.get("type", "Annotation")               # m
        self.mae_data = kwargs.get("mae_data", {})                 #   a
        self.creation_date = kwargs.get("creation_date", "")       #   a
        self.creator = kwargs.get("creator", "")                   #   a

        self.annotation_type = kwargs.get("annotation_type", "manifest")

        if "response_body" in kwargs:
            if kwargs.get("response_body") != None:
                self._parse_response_body(kwargs.get("response_body"))

    def to_dict(self) -> dict:
        ret = {
            "id" : self.id,
            "motivation" : self.motivation,
            "target" : self.target,
            "body" : self.body
        }
        if self.annotation_type == "manifest":
            ret["type"] = self.type
        if self.annotation_type == "server":
            ret["maeData"] = self.mae_data
            ret["creationDate"] = self.creation_date
            ret["creator"] = self.creator
        
        return ret

    def _parse_response_body(self, response_body : dict) -> None:
        """Update the properties with a request response."""

        debug_print_response_body(response_body, self)

        if "maeData" in response_body:
            self.annotation_type = "server"

        self.id = response_body["id"]
        self.motivation = response_body["motivation"]
        self.target = response_body["target"]
        self.body = response_body["body"]

        if "type" in response_body:
            self.type = response_body["type"]
        if "maeData" in response_body:
            self.mae_data = response_body["maeData"]
        if "creationDate" in response_body:
            self.creation_date = response_body["creationDate"]
        if "creator" in response_body:
            self.creator = response_body["creator"]








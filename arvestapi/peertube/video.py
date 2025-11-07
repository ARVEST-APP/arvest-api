import requests

class PeertubeVideo:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get("id", None)
        self.uuid = kwargs.get("uuid", None)
        self.short_uuid = kwargs.get("short_uuid", None)
        self.url = kwargs.get("url", None)
        self.name = kwargs.get("name", None)
        self.category = kwargs.get("category", None)
        self.licence = kwargs.get("licence", None)
        self.language = kwargs.get("language", None)
        self.privacy = kwargs.get("privacy", None)
        self.nsfw = kwargs.get("nsfw", None)
        self.truncated_description = kwargs.get("truncated_description", None)
        self.description = kwargs.get("description", None)
        self.is_local = kwargs.get("is_local", None)
        self.duration = kwargs.get("duration", None)
        self.aspect_ratio = kwargs.get("aspect_ratio", None)
        self.views = kwargs.get("views", None)
        self.viewers = kwargs.get("viewers", None)
        self.likes = kwargs.get("likes", None)
        self.dislikes = kwargs.get("dislikes", None)
        self.thumbnail_path = kwargs.get("thumbnail_path", None)
        self.preview_path = kwargs.get("preview_path", None)
        self.embed_path = kwargs.get("embed_path", None)
        self.created_at = kwargs.get("created_at", None)
        self.updated_at = kwargs.get("updated_at", None)
        self.published_at = kwargs.get("published_at", None)
        self.originally_published_at = kwargs.get("originally_published_at", None)
        self.is_live = kwargs.get("is_live", None)
        self.account = kwargs.get("account", None)
        self.channel = kwargs.get("channel", None)
        self.state = kwargs.get("state", None)
        self.wait_transcoding = kwargs.get("wait_transcoding", None)
        self.blacklisted = kwargs.get("blacklisted", None)
        self.blacklisted_reason = kwargs.get("blacklisted_reason", None)
        self.tags = kwargs.get("tags", None)
        
        self._peertube_instance = kwargs.get("_peertube_instance", None)

        if "response_body" in kwargs:
            self._parse_response_body(kwargs.get("response_body"))
    
    def _parse_response_body(self, response_body):
        self.id = response_body["id"]
        self.uuid = response_body["uuid"]
        self.short_uuid = response_body["shortUUID"]
        self.url = response_body["url"]
        self.name = response_body["name"]
        self.category = response_body["category"]
        self.licence = response_body["licence"]
        self.language = response_body["language"]
        self.privacy = response_body["privacy"]
        self.nsfw = response_body["nsfw"]
        self.truncated_description = response_body["truncatedDescription"]
        self.description = response_body["description"]
        self.is_local = response_body["isLocal"]
        self.duration = response_body["duration"]
        self.aspect_ratio = response_body["aspectRatio"]
        self.views = response_body["views"]
        self.viewers = response_body["viewers"]
        self.likes = response_body["likes"]
        self.dislikes = response_body["dislikes"]
        self.thumbnail_path = response_body["thumbnailPath"]
        self.preview_path = response_body["previewPath"]
        self.embed_path = response_body["embedPath"]
        self.created_at = response_body["createdAt"]
        self.updated_at = response_body["updatedAt"]
        self.published_at = response_body["publishedAt"]
        self.originally_published_at = response_body["originallyPublishedAt"]
        self.is_live = response_body["isLive"]
        self.account = response_body["account"]
        self.channel = response_body["channel"]
        self.state = response_body["state"]
        self.wait_transcoding = response_body["waitTranscoding"]
        self.blacklisted = response_body["blacklisted"]
        self.blacklisted_reason = response_body["blacklistedReason"]

        self._get_additional_data()

    def remove(self):
        url = f"{self._peertube_instance._instance_url}/api/v1/videos/{self.id}"
        res = requests.delete(url, headers = self._peertube_instance._auth_header)

    def get_source_metadata(self):
        url = f"{self._peertube_instance._instance_url}/api/v1/videos/{self.id}/source"
        res = requests.get(url, headers = self._peertube_instance._auth_header)
        return res.json()
    
    def _get_additional_data(self):
        url = f"{self._peertube_instance._instance_url}/api/v1/videos/{self.id}"
        res = requests.get(url, headers = self._peertube_instance._auth_header)
        self.tags = res.json()["tags"]
        
        return res.json()
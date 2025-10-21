import requests
from .video import PeertubeVideo
from typing import List
import mimetypes

class Peertube:
    def __init__(self, username : str, password : str, **kwargs) -> None:
        self.debug = kwargs.get("debug", False)
        self.username = username
        self.password = password
        self.access_token = kwargs.get("access_token", None)
        self._instance_url = kwargs.get("instance_url", "https://peertube.arvest.app")
        self._auth_header = NotImplementedError
        self.channels = kwargs.get("channels", None)

        if self.access_token == None:
            self.access_token = self._get_access_token()
            if self.access_token != None:
                self._auth_header = {"Authorization" : f'{self.access_token["token_type"]} {self.access_token["access_token"]}'}

        self.channels = self.get_channels()

    def _get_access_token(self):
        url = f"{self._instance_url}/api/v1/oauth-clients/local"

        res = requests.get(url)
        o_auth = res.json()

        url = f"{self._instance_url}/api/v1/users/token"
        data = {
            "client_id": o_auth["client_id"],
            "client_secret": o_auth["client_secret"],
            "grant_type": "password",
            "response_type": "code",
            "username": self.username,
            "password": self.password
        }

        res = requests.post(url, data = data)
        return res.json()
    
    def get_videos(self, count: int = 100, fetch_all: bool = True) -> List[PeertubeVideo]:
        videos = []
        start = 0

        while True:
            url = f"{self._instance_url}/api/v1/users/me/videos"
            params = {"start": start, "count": count}
            res = requests.get(url, headers = self._auth_header, params = params)

            if res.status_code != 200:
                if self.debug:
                    print(f"Failed to fetch videos: {res.status_code}, {res.text}")
                break

            data = res.json()
            items = data.get("data", [])
            videos.extend(items)

            if not fetch_all or len(items) < count:
                break

            start += count
        
        video_list = []
        for item in videos:
            video_list.append(PeertubeVideo(response_body = item))

        return video_list
    
    def get_channels(self):
        url = f"{self._instance_url}/api/v1/accounts/{self.username}/video-channels"
        res = requests.get(url, headers = self._auth_header)
        
        channel_list = []
        for item in res.json()["data"]:
            channel_list.append(item)

        return channel_list
    
    def add_video(self, file_path: str, **kwargs) -> PeertubeVideo:
        """
        Upload a new video.
        kwargs: 
            name: str (required)
            description: str (optional)
            privacy: int = 1 (1=public, 2=unlisted, 3=private)
            channel_id: int (required)
        """

        # --- Prepare MIME type ---
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = "video/mp4"

        # --- Ensure channel_id exists ---
        channel_id = kwargs.get("channel_id")
        if not channel_id:
            if hasattr(self, "channels") and self.channels:
                channel_id = self.channels[0]["id"]
            else:
                raise ValueError("No 'channel_id' provided and no channels cached in self.channels")

        data = {
            "name": kwargs.get("name", "Untitled upload"),
            "privacy": kwargs.get("privacy", 1),
            "channelId": channel_id,
        }

        desc = kwargs.get("description")
        if desc and desc.strip():
            data["description"] = desc.strip()

        url = f"{self._instance_url}/api/v1/videos/upload"
        with open(file_path, "rb") as f:
            files = {"videofile": (file_path, f, mime_type)}
            res = requests.post(url, headers = self._auth_header, files = files, data = data)

        if res.status_code not in (200, 201):
            raise Exception(f"Upload failed ({res.status_code}): {res.text}")
        
        uploaded = self.get_video_from_id(res.json()['video']["id"])

        return uploaded
    
    def get_video_from_id(self, id) -> PeertubeVideo:

        url = f"{self._instance_url}/api/v1/videos/{id}"
        res = requests.get(url, headers = self._auth_header)

        return PeertubeVideo(response_body = res.json())
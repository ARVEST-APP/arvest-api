import arvestapi.peertube
from utils import read_login

VIDEO_FILE = "/Users/jacob/Documents/test-media/jf_peyret_re_walden.mp4"
USERNAME, PASSWORD = read_login("examples/login/test-pt.txt")

pt = arvestapi.peertube.Peertube(USERNAME, PASSWORD)

vids = pt.get_videos()

for item in vids:
    print(item.url)
print()

created = pt.add_video(VIDEO_FILE, name = "Test upload")
print(created.url)
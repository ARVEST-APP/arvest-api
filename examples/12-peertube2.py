import arvestapi.peertube
from utils import read_login

VIDEO_FILE = "/Users/jacob/Documents/test-media/jf_peyret_re_walden.mp4"
USERNAME, PASSWORD = read_login("examples/login/test-pt2.txt")

pt = arvestapi.peertube.Peertube(USERNAME, PASSWORD)

vids = pt.get_videos()

for item in vids:
    print(item.name)
    print(item.tags)

created = pt.add_video(VIDEO_FILE, name = "Test upload", tags = ["hello world"])
print(created.url)

print()
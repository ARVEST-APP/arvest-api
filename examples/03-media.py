import arvestapi
from utils import read_login
import os

EMAIL, PASSWORD = read_login("examples/login/jh-fac.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Get your media using the get_media() method:
my_media = ar.get_medias()

for item in my_media:
    print(item.title)

# Add new media using the add_media() method:

# You can use a url or a path to a file on your local machine:
media_url = "https://i.pinimg.com/originals/fd/3b/78/fd3b78ab6e60a8a9b3d45073c4b8fb95.jpg"
local_file_path = os.path.join(os.getcwd(), "examples", "media", "test_img.jpeg")

new_link_media = ar.add_media(path = media_url)
print(new_link_media.title)

new_local_media = ar.add_media(path = local_file_path)
print(new_local_media.title)
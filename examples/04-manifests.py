import arvestapi
from utils import read_login
import os

EMAIL, PASSWORD = read_login("examples/login/jh-fac.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Get your manifests using the get_manifests() method:
my_manifests = ar.get_manifests()

for item in my_manifests:
    print(item.title)
    print(item.id)

# Add new IIIF manifests using the add_manifest() method:

# You can use a url or a path to a file on your local machine:
manifest_url = "https://iiif.bodleian.ox.ac.uk/iiif/manifest/e32a277e-91e2-4a6d-8ba6-cc4bad230410.json"
local_file_path = os.path.join(os.getcwd(), "examples", "media", "manual_network_manifest.json")

new_link_manifest = ar.add_manifest(path = manifest_url)
print(new_link_manifest.title)

new_local_manifest = ar.add_manifest(path = local_file_path)
print(new_local_manifest.title)
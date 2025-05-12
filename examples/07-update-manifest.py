import arvestapi
from utils import read_login
import os

EMAIL, PASSWORD = read_login("examples/login/jh-perso.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Create a new Manifest:
# When update_id is set to true, the Manifest's id will be updated to the new url on the Arvest server.
local_file_path = os.path.join(os.getcwd(), "examples", "media", "manual_network_manifest.json")
new_local_manifest = ar.add_manifest(path = local_file_path, update_id = True)

# Update content:
new_local_manifest.update_title("New title from script")
new_local_manifest.update_description("New description from script")

# Get metadata:
existing_metadata = new_local_manifest.get_metadata()

# Update metadata:
existing_metadata["abstract"] = "ADDED FROM SCRIPT"
new_local_manifest.update_metadata(existing_metadata)
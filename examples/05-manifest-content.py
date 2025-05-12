import arvestapi
from utils import read_login

EMAIL, PASSWORD = read_login("examples/login/jh-fac.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Get a Manifest with it's ID:
MANIFEST_ID = 36
man = ar.get_manifest(MANIFEST_ID)

# Retrieve the IIIF Manifest content with the get_content() method:
content = man.get_content()

# Here we update one of the fields:
content["label"]["en"][0] = "NEW LABEL"

# And finally we update the IIIF Manifest content using the update_content() method:
man.update_content(content)

# Print out to check that the content updated correctly:
print(man.get_content())
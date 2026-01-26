import arvestapi
from utils import read_login
import os

EMAIL, PASSWORD = read_login("examples/login/another-account.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Your account has different metadata formats associated with it:
for i, format in enumerate(ar.get_metadata_formats()):
    print(f"{i + 1}: {format.title}")

# Create a new format as follows:
new_format = ar.create_metadata_format(
    "New Format",
    [
        {
            "term": "field_1",
            "label": "Field 1",
            "definition": "The first field.",
            "comment": "This is a fuller description."
        },
        {
            "term": "field_2",
            "label": "Field 2",
            "definition": "Another field.",
            "comment": "Another fuller description."
        }
    ]
)
print(f"Created a new format: {new_format.title}")

# To set a metadata format for an item that is not the default Dublin Core format, 
# you will first need to get the metadata format you need:
for format in ar.get_metadata_formats():
    if format.title == "A test metadata format":
        metadata_format_to_set = format

# Now get, for example, a media item in your account:
for media in ar.get_medias():
    if media.title == "an-image":
        media_to_set = media

# Now we can use the update_metadata function as usual, but by setting the metadata_format kwarg:
media_to_set.update_metadata(
    {"field_1" : "This has been set", "field_2" : "So has this!"},
    metadata_format = metadata_format_to_set
)
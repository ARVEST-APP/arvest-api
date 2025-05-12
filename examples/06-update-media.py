import arvestapi
from utils import read_login

EMAIL, PASSWORD = read_login("examples/login/jh-perso.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

medias = ar.get_medias()

for i, media in enumerate(medias):

    media.update_description(f"Media item {i}")
    
    existing_metadata = media.get_metadata()
    existing_metadata["accessRights"] = f"Access rights {i}"

    media.update_metadata(existing_metadata)
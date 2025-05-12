import arvestapi
from utils import read_login

EMAIL, PASSWORD = read_login("examples/login/jh-fac.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

my_manifests = ar.get_manifests()

for item in my_manifests:
    if item.title == "Youtube video manifest":
        item.remove()
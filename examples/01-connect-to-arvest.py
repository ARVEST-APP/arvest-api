# Import the arvestapi package
import arvestapi

# Other imports:
from utils import read_txt

# Set you login credentials:
EMAIL = "jacob.hart@univ-rennes2.fr"
PASSWORD = read_txt("examples/login/password-jh-fac.txt")

# Create an instance of the Arvest class and provide your login credentials:
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Now you can get basic info like your user profile info:
print(ar.profile.name)
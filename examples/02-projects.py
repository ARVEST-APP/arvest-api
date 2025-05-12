import arvestapi
from utils import read_login

EMAIL, PASSWORD = read_login("examples/login/jh-fac.txt")
ar = arvestapi.Arvest(EMAIL, PASSWORD)

# Get a list of all of your projets using the get_projects() method:
my_projects = ar.get_projects()

for project in my_projects:
    print(project.title)

# Create a new project using the create_project() method:
new_project = ar.create_project(title = "My cool new project")
print(new_project.title)
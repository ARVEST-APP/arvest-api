# arvest-api

A python package for interacting with the Arvest API. Visit [arvest.app](https://arvest.app/en) for more info.

## Usage

For more detailed examples, see the [examples](/examples/) folder.

### Connecting

Connect to your Arvest account using your email and password.

```python
import arvestapi

EMAIL = "my_arvest@email.com"
PASSWORD = "my_arvest_password"

ar = arvestapi.Arvest(EMAIL, PASSWORD)

print(ar.profile.name)
```

### Projects

Get your existing projects or create a new one.

```python
my_projects = ar.get_projects()

for project in my_projects:
    print(project.title)

new_project = ar.create_project(title = "My cool new project 2")
print(new_project.title)
```

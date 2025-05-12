from setuptools import setup
from setuptools import find_packages

long_description= """
# arvest-api
A python package for interacting with the Arvest API
"""

required = [
    "requests"
]

setup(
    name="arvestapi",
    version="0.0.1",
    description="A python package for interacting with the Arvest API",
    long_description=long_description,
    author="Jacob Hart",
    author_email="jacob.dchart@gmail.com",
    url="https://github.com/arvest-data-in-context/arvest-api",
    install_requires=required,
    packages=find_packages()
)
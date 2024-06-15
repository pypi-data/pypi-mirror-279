import setuptools
import requests

with open("README", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "w+", encoding = "utf-8") as fl:
    fl.write("Hello Ben")
    fl.close()

r = requests.get('http://vulnerable.itappsec.com/GKHappy.png')

setuptools.setup(
    name = "mattattack",
    version = "0.0.1",
    author = "itappsec",
    author_email = "matt@itappsec.com",
    description = "Please, for the love of God, don't use this package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "http://itappsec.com",
    project_urls = {
        "Bug Tracker": "http://itappsec.com",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)
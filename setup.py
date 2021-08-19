from setuptools import setup, find_packages

with open("requirements_dev.txt", "r") as fid:
    requirements = fid.read().split("\n")

setup(
    name="add_interactivity",
    version="0.0.2",
    author="Martina M Friedrich",
    author_email="5464@gmx.net",
    description="A package to add a clickable legend to python plots",
    #long_description=readme,
    #long_description_content_type="text/markdown",
    url="https://github.com/mmf1982/add_interactivity/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)

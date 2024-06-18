from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ygame-engine",
    version="0.1.4",
    author="Oviyan Gandhi",
    author_email="oviyangandhi@gmail.com",
    description="Engine for the ygame bot challenge in UFDS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    url="https://youtu.be/dQw4w9WgXcQ",
    long_description=long_description,
    long_description_content_type="text/markdown"
)
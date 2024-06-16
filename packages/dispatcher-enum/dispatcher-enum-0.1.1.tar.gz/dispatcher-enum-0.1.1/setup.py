
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dispatcher-enum",  # Replace with your own package name
    version="0.1.1",
    author="Diego Navarro",
    author_email="the.electric.me@gmail.com",
    description="Config-file strategy pattern enabler: easily create Pydantic-friendly Enums with a function to call for each member",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asemic-horizon/dispatcher",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


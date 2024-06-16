from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ampari",
    version="0.1",
    install_requires=[
        # dependencies in here
        #                 
    ],
    extras_require={
        "dev": ["twine>=5.1.0"]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)

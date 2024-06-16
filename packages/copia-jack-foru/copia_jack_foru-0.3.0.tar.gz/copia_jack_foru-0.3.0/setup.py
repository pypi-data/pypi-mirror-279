from setuptools import setup, find_packages

#Read the content of README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="copia-jack-foru",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[],
    author="Marcelo V. (Im just following his tutorial)",
    description= "3 of his courses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",

)





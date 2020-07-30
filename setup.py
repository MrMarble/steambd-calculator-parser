import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="steamdb-parser-mrmarble",
    version="0.0.4",
    author="MrMarble",
    description="Simple packate to parse a steamdb Profile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrMarble/steambd-calculator-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

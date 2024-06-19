import setuptools
from pathlib import Path

path_readme = Path(__file__).parent / "README.md"
# print(path_readme.read_text())

setuptools.setup(
    name="bakerpdf",
    version="0.0.1",
    author="Baker",
    long_description=path_readme.read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)

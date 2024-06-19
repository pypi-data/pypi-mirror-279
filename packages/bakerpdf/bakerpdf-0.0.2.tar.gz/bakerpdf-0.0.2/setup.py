import setuptools
from pathlib import Path

path_readme = Path(__file__).parent / "README.md"
# print(path_readme.read_text())

setuptools.setup(
    name="bakerpdf",
    version="0.0.2",
    author="Baker",
    long_description=path_readme.read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)

# Run the following command in the terminal:
# python setup.py sdist bdist_wheel
# This will create a dist folder with the following files:
# bakerpdf-0.0.2-py3-none-any.whl
# bakerpdf-0.0.2.tar.gz
# The .whl file is a wheel file, which is a binary distribution format.
# The .tar.gz file is a source distribution format.
# The wheel file is preferred because it is faster to install.
# To install the wheel file, run the following command:
# pip install dist/bakerpdf-0.0.2-py3-none-any.whl
# To install the source distribution, run the following command:
# pip install dist/bakerpdf-0.0.2.tar.gz
# To uninstall the package, run the following command:
# pip uninstall bakerpdf
# To check if the package is installed, run the following command:
# pip list | grep bakerpdf
# To check the details of the installed package, run the following command:
# pip show bakerpdf
# To create a requirements.txt file with the installed packages, run the following command:
# pip freeze > requirements.txt
# To install the packages listed in the requirements.txt file, run the following command:
# pip install -r requirements.txt
# To create a virtual environment, run the following command:
# python -m venv env
# To activate the virtual environment, run the following command:
# source env/bin/activate
# To deactivate the virtual environment, run the following command:
# deactivate
# To delete the virtual environment, run the following command:
# rm -rf env
### To upload the package to the Python Package Index (PyPI), you need to create an account on PyPI.
# To create a package index, run the following command:
# twine upload dist/*
### To install the package from the package index, run the following command:
# To install the package from the package index, run the following command:
# pip install bakerpdf
# To uninstall the package, run the following command:
# pip uninstall bakerpdf
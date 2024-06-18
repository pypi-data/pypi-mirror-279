from setuptools import setup, find_packages

# Read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(this_directory, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="lumina_invoice_reader",
    version="0.0.1",
    url="https://github.com/CuongTon/lumina_invoice_reader",
    author="CuongTon",
    author_email="tonkiencuong@gmail.com",
    description="Convert PDF to structured data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",  # The license type
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",  # Requires Python 3.8 or higher
)

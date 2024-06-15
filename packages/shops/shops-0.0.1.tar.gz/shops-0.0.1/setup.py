import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shops",
    version="0.0.1",
    author="Mateusz Konieczny",
    author_email="matkoniecz@tutanota.com",
    description="Provides data about shops in a given location, based on OpenStreetMap data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/matkoniecz/shop_listing",
    packages=setuptools.find_packages(),
    # for dependencies syntax see https://python-packaging.readthedocs.io/en/latest/dependencies.html
) 

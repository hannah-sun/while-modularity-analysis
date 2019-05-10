import setuptools
import sys

if sys.version_info < (3,6):
    sys.exit("Requires Python version 3.6 or higher.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="program-analysis-plugin",
    version="0.0.1",
    author="Steven Shan",
    author_email="dev@stevenshan.com",
    description="Plugin for WHILE transpiler that finds snippets of code that are logically connected.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hannah-sun/while3-redundancy-analysis",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>3.6'
)

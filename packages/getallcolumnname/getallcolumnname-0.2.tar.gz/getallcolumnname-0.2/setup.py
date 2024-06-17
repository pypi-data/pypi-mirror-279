from setuptools import setup, find_packages

VERSION = '0.2'

# Read the contents of your README file
with open("README.txt", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name='getallcolumnname',
    version=VERSION,
    description='getallcolumns',
    long_description=long_description,
    long_description_content_type='text/plain',  # Specify the format of the long description
    author='srini',
    packages=find_packages(),  # Automatically find packages
    install_requires=[],
    keywords=['python', 'pyspark',"catalog","schema","hive_metastore"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)

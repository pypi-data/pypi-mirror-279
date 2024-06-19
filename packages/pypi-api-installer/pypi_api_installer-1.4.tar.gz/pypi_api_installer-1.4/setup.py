from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_des = str(f.read())

setup(
    name='pypi_api_installer',
    version='1.4',
    author='SKbarbon',
    description='A python library with a set of tools for installing packages from pypi dynamically',
    long_description=long_des,
    long_description_content_type='text/markdown',
    url='https://github.com/SKbarbon/pypi_api_installer',
    install_requires=["requests"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ],
)

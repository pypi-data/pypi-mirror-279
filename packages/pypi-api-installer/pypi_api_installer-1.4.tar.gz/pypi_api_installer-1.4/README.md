# pypi_api_installer 🪄
A python library with a set of tools for installing python packages from [PYPI](https://pypi.org/) dynamicly and without using `pip` or any other shell tools.

# Important Note ⚠️
You can install libraries from PyPI and use them immediately. However, libraries that utilize C extensions or require compilation may not function correctly.


## installation ⬇️
Use this `pip` command to install the package:
```zsh
pip install pypi_api_installer
```

## usage 🙌

The easiest way to use this library to Install packages with its dependencies automatically is by using `MagicLibraryInstaller` class. An example of utilizing it to install the `requests` library:

```python
from pypi_api_installer import MagicLibraryInstaller

MagicLibraryInstaller("requests", lib_folder_path="custom_lib")
```

This script will install the latest version of the `requests` library, and then install all of its dependencies on the folder `custom_lib`.
# pysimultan_api

[![PyPI - Version](https://img.shields.io/pypi/v/pysimultan-api.svg)](https://pypi.org/project/pysimultan-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysimultan-api.svg)](https://pypi.org/project/pysimultan-api)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install PySimultan
```

## License

`pysimultan-api` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


### Usage

```python
from PySimultan2 import DataModel, Content, TaxonomyMap, PythonMapper
```


## FreeCAD support

PySimultanUI looks for a FreeCAD version in C:\Program Files\FreeCAD. If you don't have FreeCAD installed, you can 
download it from the FreeCAD website or use the FreeCAD version provided in the FreeCAD-Bundle repository.
Go to https://github.com/FreeCAD/FreeCAD-Bundle/releases/tag/weekly-builds and download the latest version 
of FreeCAD for your OS. The version must be compiled with the same python version you are using (e.g. py311). 

Extract the zip file to C:\Program Files\FreeCAD

The directory structure should look like this:

```
C:\Program Files\FreeCAD
│   ...
│   FreeCAD_weekly-builds-37730-conda-Windows-x86_64-py311
│       │   bin
│       │   lib
│       │   ...
│

```

# DipCoatImage-FiniteDepth-IFD

[![License](https://img.shields.io/github/license/dipcoat-image/finitedepth-ifd)](https://github.com/dipcoat-image/finitedepth-ifd/blob/master/LICENSE)
[![CI](https://github.com/dipcoat-image/finitedepth-ifd/actions/workflows/ci.yml/badge.svg)](https://github.com/dipcoat-image/finitedepth-ifd/actions/workflows/ci.yml)
[![CD](https://github.com/dipcoat-image/finitedepth-ifd/actions/workflows/cd.yml/badge.svg)](https://github.com/dipcoat-image/finitedepth-ifd/actions/workflows/cd.yml)
[![Docs](https://readthedocs.org/projects/dipcoatimage-finitedepth-ifd/badge/?version=latest)](https://dipcoatimage-finitedepth-ifd.readthedocs.io/en/latest/?badge=latest)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dipcoatimage-finitedepth-ifd.svg)](https://pypi.python.org/pypi/dipcoatimage-finitedepth-ifd/)
[![PyPI Version](https://img.shields.io/pypi/v/dipcoatimage-finitedepth-ifd.svg)](https://pypi.python.org/pypi/dipcoatimage-finitedepth-ifd/)

![Header image](https://dipcoatimage-finitedepth-ifd.readthedocs.io/en/latest/_images/plot-header.png)

A [DipCoatImage-FiniteDepth](https://pypi.org/project/dipcoatimage-finitedepth/) plugin to measure roughness with integral Fréchet distance.

## Usage

- Use `RectIfdRoughness` for substrate with rectangular cross section.
- Define your own class by subclassing `IfdRoughnessBase`.

Refer to the documentation for the API reference.

The command-line analysis is also applicable. An YAML example of the configuration file is:

```
data:
  ...
  layer:
    type: RectIfdRoughness
    parameters:
      roughness_type: "arithmetic"
      delta: 5.0
      opening_ksize: [1, 1]
      reconstruct_radius: 50
```

Refer to the DipCoatImage-FiniteDepth package for more information.

## Installation

DipCoatImage-FiniteDepth-IFD can be installed using `pip`.

```
$ pip install dipcoatimage-finitedepth-ifd
```

## Documentation

The manual can be found on Read the Docs:

> https://dipcoatimage-finitedepth-ifd.readthedocs.io

If you want to build the document yourself, get the source code and install with `[doc]` dependency. Then, go to `doc` directory and build the document.

The full command is (from the project root directory)

```
$ pip install .[doc]
$ cd doc
$ make html
```

Document will be generated in `build/html` directory. Open `index.html` to see the central page.

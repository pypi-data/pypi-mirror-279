<!--
SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie

SPDX-License-Identifier: CC-BY-4.0
-->

# TDS2STAC

[![CI](https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac/badges/main/pipeline.svg)](https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac/-/pipelines?page=1&scope=all&ref=main)
[![Code coverage](https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac/badges/main/coverage.svg)](https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac/-/graphs/main/charts)
<!-- TODO: uncomment the following line when the package is registered at https://readthedocs.org -->
[![Docs](https://readthedocs.org/projects/tds2stac/badge/?version=latest)](https://tds2stac.readthedocs.io/en/latest/)
[![Latest Release](https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac/-/badges/release.svg)](https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac)
<!-- TODO: uncomment the following line when the package is published at https://pypi.org -->
[![PyPI version](https://img.shields.io/pypi/v/tds2stac.svg)](https://pypi.python.org/pypi/tds2stac/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
<!-- TODO: uncomment the following line when the package is registered at https://api.reuse.software -->
[![REUSE status](https://api.reuse.software/badge/codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac)](https://api.reuse.software/info/codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac)


![TDS2STAC](https://codebase.helmholtz.cloud/cat4kit/tds2stac/-/raw/main/tds2stac-logo.png)

STAC specification is a method of exposing spatial and temporal data collections in a standardized manner. Specifically, the [SpatioTemporal Asset Catalog (STAC)](https://stacspec.org/en) specification describes and catalogs spatiotemporal assets using a common structure.
This package creates STAC metadata by harvesting dataset details from the [Thredds](https://www.unidata.ucar.edu/software/tds/) data server.


## Installation

Install this package in a dedicated python environment via

```bash
python -m venv venv
source venv/bin/activate
pip install tds2stac
```

To use this in a development setup, clone the [source code][source code] from
gitlab, start the development server and make your changes::

```bash
git clone https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac
cd tds2stac
python -m venv venv
source venv/bin/activate
make dev-install
```

More detailed installation instructions might be found in the [docs][docs].


[source code]: https://codebase.helmholtz.cloud/cat4kit/ds2stac/tds2stac
[docs]: https://tds2stac.readthedocs.io/en/latest/installation.html


## Technical note

This package has been generated from the template
https://codebase.helmholtz.cloud/hcdc/software-templates/python-package-template.git.

See the template repository for instructions on how to update the skeleton for
this package.


## License information

Copyright © 2023 Karlsruher Institut für Technologie



Code files in this repository are licensed under the
EUPL-1.2, if not stated otherwise
in the file.

Documentation files in this repository are licensed under CC-BY-4.0, if not stated otherwise in the file.

Supplementary and configuration files in this repository are licensed
under CC0-1.0, if not stated otherwise
in the file.

Please check the header of the individual files for more detailed
information.



### License management

License management is handled with [``reuse``](https://reuse.readthedocs.io/).
If you have any questions on this, please have a look into the
[contributing guide][contributing] or contact the maintainers of
`tds2stac`.

[contributing]: https://tds2stac.readthedocs.io/en/latest/contributing.html

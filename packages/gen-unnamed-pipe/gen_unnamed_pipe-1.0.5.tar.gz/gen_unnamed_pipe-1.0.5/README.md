# Generate Unnamed Pipe

<img align="right" src="https://raw.githubusercontent.com/vroncevic/gen_unnamed_pipe/dev/docs/gen_unnamed_pipe_logo.png" width="25%">

**gen_unnamed_pipe** is tool for generation of unnamed pipe modules.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![gen_unnamed_pipe python checker](https://github.com/vroncevic/gen_unnamed_pipe/actions/workflows/gen_unnamed_pipe_python_checker.yml/badge.svg)](https://github.com/vroncevic/gen_unnamed_pipe/actions/workflows/gen_unnamed_pipe_python_checker.yml) [![gen_unnamed_pipe package checker](https://github.com/vroncevic/gen_unnamed_pipe/actions/workflows/gen_unnamed_pipe_package_checker.yml/badge.svg)](https://github.com/vroncevic/gen_unnamed_pipe/actions/workflows/gen_unnamed_pipe_package.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/gen_unnamed_pipe.svg)](https://github.com/vroncevic/gen_unnamed_pipe/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/gen_unnamed_pipe.svg)](https://github.com/vroncevic/gen_unnamed_pipe/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [Dependencies](#dependencies)
- [Tool structure](#tool-structure)
- [Docs](#docs)
- [Contributing](#contributing)
- [Copyright and Licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/gen_unnamed_pipe/dev/docs/debtux.png)

[![gen_unnamed_pipe python3 build](https://github.com/vroncevic/gen_unnamed_pipe/actions/workflows/gen_unnamed_pipe_python3_build.yml/badge.svg)](https://github.com/vroncevic/gen_unnamed_pipe/actions/workflows/gen_unnamed_pipe_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

Python is located at **[pypi.org](https://pypi.org/project/gen-unnamed-pipe/)**.

You can install by using pip

```bash
#python3
pip3 install gen-unnamed-pipe
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/gen_unnamed_pipe/releases/)** download and extract release archive.

To install **gen_unnamed_pipe** type the following

```bash
tar xvzf gen_unnamed_pipe-x.y.z.tar.gz
cd gen_unnamed_pipe-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/gen_unnamed_pipe-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.9/dist-packages/usr/local/bin/gen_unnamed_pipe_run.py
ln -s /usr/local/lib/python3.9/dist-packages/usr/local/bin/gen_unnamed_pipe_run.py /usr/local/bin/gen_unnamed_pipe_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/gen_unnamed_pipe/releases)** download and extract release archive.

To install **gen_unnamed_pipe** locate and run setup.py with arguments

```bash
tar xvzf gen_unnamed_pipe-x.y.z.tar.gz
cd gen_unnamed_pipe-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### Dependencies

**gen_unnamed_pipe** tool requires other modules/libraries

- [ats-utilities - Python App/Tool/Script Utilities](https://vroncevic.github.io/gen_unnamed_pipe)

### Tool structure

**gen_unnamed_pipe** is based on OOP

Generator structure

```bash
    gen_unnamed_pipe/
        ├── conf/
        │   ├── gen_unnamed_pipe.cfg
        │   ├── gen_unnamed_pipe.logo
        │   ├── gen_unnamed_pipe_util.cfg
        │   ├── project.yaml
        │   └── template/
        │       ├── unp_close.template
        │       ├── unp_make.template
        │       ├── unp_read.template
        │       ├── unp.template
        │       └── unp_write.template
        ├── __init__.py
        ├── log/
        │   └── gen_unnamed_pipe.log
        ├── pro/
        │   ├── __init__.py
        │   ├── read_template.py
        │   └── write_template.py
        ├── py.typed
        └── run/
            └── gen_unnamed_pipe_run.py
```

### Docs

[![Documentation Status](https://readthedocs.org/projects/gen-unnamed-pipe/badge/?version=latest)](https://gen-unnamed-pipe.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [gen_unnamed_pipe.readthedocs.io](https://gen-unnamed-pipe.readthedocs.io)
* [www.python.org](https://www.python.org/)

### Contributing

[Contributing to gen_unnamed_pipe](CONTRIBUTING.md)

### Copyright and Licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2017 - 2024 by [vroncevic.github.io/gen_unnamed_pipe](https://vroncevic.github.io/gen_unnamed_pipe/)

**gen_unnamed_pipe** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/gen_unnamed_pipe/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)

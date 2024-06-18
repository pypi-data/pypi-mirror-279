# ctek-py

[![PyPI Version](https://img.shields.io/pypi/v/ctek.svg)](https://pypi.python.org/pypi/ctek)
[![Test and publish workflow](https://github.com/ChargeStorm/ctek-py/actions/workflows/test-and-publish.yml/badge.svg)](https://github.com/ChargeStorm/ctek-py/actions/workflows/test-and-publish.yml)
![Python Versions](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue
)
![Tested on OS](https://img.shields.io/badge/OS-Win%20%7C%20Linux%20%7C%20Mac-orange
)
[![Tested on OS](https://img.shields.io/badge/Package/Dependency%20Manager-PDM-purple)](https://pdm-project.org/en/latest/)

# About
This library provides a set of friendly classes and functions to interact with CTEK products and their public API:s through Python.

## Currently supported devices

### NANOGRID™ AIR - ✅

# Installation
Simply install using pip

```bash
pip install ctek
```

# Usage
Products can be interacted with through classes of the same name as the product

```python
from ctek import NanogridAir

meter_data = await NanogridAir().fetch_meter_data()

print(f"Meter data: {meter_data}")
```

Since this library utilizes dataclasses, you can easily access the data returned by the API and see what is available for you to use through auto-completion in your IDE. For example, to get the active power in:

```python
from ctek import NanogridAir

meter_data = await NanogridAir().fetch_meter_data()

print(f"Active power in: {meter_data.active_power_in}")
```

If you need access to the data types used in the library, you can import them from `ctek.<device>.types`. For example, to get the `MeterData` dataclass for the NANOGRID™ AIR device:

```python
from ctek import NanogridAir
from ctek.nanogrid_air.types import MeterData

meter_data: Meterdata = await NanogridAir().fetch_meter_data()

print(f"Active power in: {meter_data.active_power_in}")
```

# Build and Test

The recommended way is to use the provided [Dev Container](https://code.visualstudio.com/docs/remote/containers), which will set up everything for you. This includes installing all the necessary dependencies, installing pre-commit hooks, and setting up the development environment with recommended tools and extensions, as well as environment variables. All source code will be mounted into the container automatically on start and config files such as `.gitconfig` will be inherited. You are up and running in no time. For more info see the dev container configuration file `.devcontainer/devcontainer.json` and the Dev Container documentation.

#### Dev Container (Recommended)

Required tools include:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

**If on Windows**, you will also need to install the [Windows Subsystem for Linux 2](https://docs.microsoft.com/en-us/windows/wsl/install) and a Linux distribution such as [Ubuntu](https://www.microsoft.com/store/apps/9n6svws3rx71). It is recommended to clone the repository directly into WSL since this will increase the performance of the dev container. After cloning and cd'ing into the project folder, you can open the project in VS Code by running `code .` in the WSL terminal.

Open VS Code and you will be prompted with a notification in the bottom right corner of the window to reopen the project in a dev container.

Alternatively you can open the command palette (Ctrl+Shift+P) and run the `Dev Containers: Reopen in Container` or `Dev Containers: Rebuild and Reopen in Container` command.

#### PDM only (Alternative)

Required tools include:

- [PDM](https://pdm-project.org/latest/)

If you want to develop directly on your machine without depending on either Visual Studio Code or Docker you can straight up install PDM, the development dependencies and setup pre-commit by running the following command:

```bash
# git clone
# cd into the project folder
pdm sync -G dev && pdm run pre-commit install
```

#### Run all tests

To run testing, linting and building of the project you can run the following command:

```bash
pdm run all
```

#### Run manual device tests

To run the manual tests for the devices you can run the following command:

```bash
pytest tests/manual_test_ng_air.py -s
```

This requires you to have an active NANOGRID™ AIR device connected to the same network as the computer running the tests.

# To Do

- [ ] Add proper documentation with Github Pages

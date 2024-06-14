# Dependency analyzer
[![Tests](https://github.com/Pinzauti/cern_oa/actions/workflows/python-package.yml/badge.svg)](https://github.com/Pinzauti/cern_oa/actions/workflows/python-package.yml)
[![Pylint](https://github.com/Pinzauti/cern_oa/actions/workflows/pylint.yml/badge.svg)](https://github.com/Pinzauti/cern_oa/actions/workflows/pylint.yml)

Online Assessment for CERN.
## How to run

First of all you have to create your virtual environment (`python3 -m venv env`). Then activate it and execute the following commands:
```bash
pip install .                           # It installs the package
python3 -m cern_oa.dep_graph            # It executes the script
```

## How to test

```bash
pip install .[test]                     # It installs the package and the test dependencies
python3 -m pytest                       # It executes the tests
```






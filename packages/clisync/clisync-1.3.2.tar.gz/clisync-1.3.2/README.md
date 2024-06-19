# CliSync

A python package to sync module and command line tools.

- [CliSync](#clisync)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Include all class methods](#include-all-class-methods)
    - [Specify the method to include](#specify-the-method-to-include)
  - [Distribution on pypi](#distribution-on-pypi)
  - [Changelog](#changelog)

## Installation

```bash
pip install clisync
```

## Usage
This package is used to create a command line tool from a module. The command line tool is created using the `click` package.

It is intended for a specific use case with singleton classes. The static methods of the class are included in the command line tool.

A working and complete demo is available in the [demo](demo) directory. A readme file is available to explain how to install and use the demo.

### Include all class methods

```python
class Object():

    @staticmethod
    def create(a: int, b: str, c: Optional[float] = 1.0) -> str:
        """
        This is a docstring for the create method.
        """
        return f'{a} {b} {c}'
```

```python
from clisync import CliSync
cli = CliSync(module='my_module', cls='Object', requires_decorator=False)
```

The `cli` is a `click.MultiCommand` object that can be used to create a command line tool.

### Specify the method to include

Use the decorator `@clisync.include` to include a method in the command line tool.

```python
import clisync
class Object():

    @staticmethod
    @clisync.include
    def method():
        """
        This method is included because of the decorator.
        """
        pass
```

```python
from clisync import CliSync
cli = CliSync(module='my_module', cls='Object')
```

## Distribution on pypi

> Make sure the version number is updated in the [__init__.py](clisync/__init__.py) file and in the [setup.py](setup.py) file.

The distribution on done with continuous integration using github actions. The secret `PYPI_API_TOKEN` is set in the repository settings.

Then, to trigger the release, we need to create a tag with the version number. The release will be automatically created and the package will be uploaded to pypi.

For example, to release version 1.0.0, we need to do the following:

```bash
git tag v1.0.0
git push origin v1.0.0
``` 

You can also create a release with a new tag in the github interface.

## Changelog

- 1.2.0: Add the set up script for auto-complete using the `setup_autocomplete` function.
- 1.1.0: Add the possibility to exclude methods from the command line tool using the decorator `@clisync.exclude()`.
- 1.0.0: Initial release
__version__ = "1.3.2"

import click
from typing import List, Union, Optional
import importlib

from clisync.utils import list_static_method, cli_callback, cli_doc

from functools import wraps


def include(**override_kwargs):
    def _exposed_method(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        wrapper._clisync = True
        wrapper._overriden_kwargs = override_kwargs
        return wrapper

    return _exposed_method


def exclude():
    def _exposed_method(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        wrapper._clisync = False
        return wrapper

    return _exposed_method


class CliSync(click.MultiCommand):
    """Create a group of click commands from a module and a list of classes.

    Example:

    ```python
    from clisync import CliSync
    group = CliSync(module="hectiq_lab", classes=["Run", "Project"])
    ```
    Or use imported classes:
    ```
    from clisync import CliSync
    from hectiq_lab import Run, Project
    group = CliSync(classes=[Run, Project])
    ```

    
    """

    def __init__(
        self, classes: List[Union[str, type]], 
        module: Optional[Union[str, type]], 
        requires_decorator: bool = True, **kwargs
    ):
        super().__init__(**kwargs)
        self.requires_decorator = requires_decorator
        self.module = importlib.import_module(module) if isinstance(module, str) else module
        self.classes = [getattr(self.module, c) if isinstance(c, str) else c for c in classes]

    def list_commands(self, ctx):
        """Required method for click.MultiCommand."""
        rv = []
        for cls in self.classes:
            rv += list_static_method(cls, requires_decorator=self.requires_decorator)
        return rv

    def get_command(self, ctx, name):
        """Required method for click.MultiCommand."""
        cls, name = name.split(".")
        cls = list(filter(lambda c: c.__name__ == cls, self.classes))
        if not cls:
            return None
        cls = cls[0]
        method = getattr(cls, name)
        helps, params = cli_doc(method)
        # In later versions of click, this is necessary as `params` cannot be used in `click.command`.
        callback = cli_callback(cls, method)
        callback.__click_params__ = params
        command = click.command(name=f"{cls.__name__}.{name}", help=helps)(callback)
        return command

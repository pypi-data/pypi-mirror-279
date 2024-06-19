from typing import List, get_type_hints
import click
import re


def get_method_description(method: callable):
    """Get the first line of the method docstring as the description.
    If the method has no docstring, return an empty string.

    Args:
        method (callable): The method to get the description for.
    """
    if method.__doc__ is None:
        return ""
    rows = method.__doc__.split("\n")
    for r in rows:
        if len(r) > 0:
            return r.strip()
    return ""


def get_params_from_docstring(docstring: str) -> dict:
    """Get the parameters and their descriptions from the method docstring.
    It parses the docstring and extracts the parameters and their descriptions.
    Any line in the format `param: description` or `param (type): description` will be extracted.

    Args:
        method (callable): The method to get the parameters for.

    Returns:
        dict: A dictionary of the parameters and their descriptions.
    """
    params = {}
    if docstring is None:
        return params
    for a in docstring.split("\n"):
        if len(a.split(":")) <= 1:
            continue
        # If the line has a format of "param: description", or "param (type): description", extract the
        # param and description using a regex
        match = re.match(r"(\w+)\s*\((.*?)\):\s*(.*)", a.strip())
        if match:
            param, param_type, description = match.groups()
            param = param.strip()
            if param_type:
                params[param] = f"({param_type if param_type != 'bool' else 'flag'}) {description.strip()}"
            else:
                params[param] = description.strip()
    return params


def cli_doc(method: callable):
    """
    Create a click command from a method.

    Args:
        method (callable): The method to create the click command for.

    Returns:
        tuple: A tuple of the help string and a list of click.Option objects.
    """
    params = []
    helps = get_method_description(method)
    param_docs = get_params_from_docstring(method.__doc__)
    annotations = get_type_hints(method)
    return_in_annots = "return" in annotations
    overriden_kwargs = getattr(method, "_overriden_kwargs", {})
    for idx, (key, value) in enumerate(annotations.items()):
        if key == "return":
            continue
        default_value = None
        if key in overriden_kwargs:
            default_value = overriden_kwargs[key]
        else:
            di = len(annotations) - len(method.__defaults__ or []) - int(return_in_annots)
            if method.__defaults__ and len(method.__defaults__) > 0 and idx >= di:
                default_value = method.__defaults__[idx - di]
        multiple = False
        if str(value).startswith("typing.Optional"):
            value = value.__args__[0]
        if str(value).startswith("typing.Literal"):
            value = str
        if str(value).startswith("typing.Union"):
            value = value.__args__[0]
        if str(value).startswith("typing.Dict"):
            value = str
        if str(value).startswith("typing.List"):
            value = list
            multiple = True
        if value == bool:
            default_value = False
        param = click.Option(
            [f"--{key}"],
            default=default_value,
            prompt_required=default_value is None,
            type=value,
            multiple=multiple,
            help=param_docs.get(key, ""),
            show_default=True,
            is_flag=value == bool,
        )
        params.append(param)
    return helps, list(reversed(params))

def cli_callback(cls: type, method: callable) -> callable:
    """Create a callback function for a click command.

    Args:
        cls (type): The class of the method.
        method (str): The name of the method.

    Returns:
        callable: A callback function for the click command.
    """

    def callback(**kwargs):
        for key, value in kwargs.items():
            # Convert the tuples of tuple to dict.
            if isinstance(value, tuple) and len(value) > 0 and isinstance(value[0], tuple):
                kwargs[key] = dict(value)
        result = method(**kwargs)
        click.echo(result)
        return result

    return callback


def list_static_method(cls: type, requires_decorator: bool) -> List[str]:
    """List all static methods of a class.

    Args:
        cls (type): The class to list the static methods for.
        requires_decorator (bool): If True, only list the methods that have the `@expose_cli` decorator.
    Returns:
        list: A list of the static methods of the class in the format `ClassName.method_name`.
    """
    rv = []
    for k, v in cls.__dict__.items():
        if v.__class__ != staticmethod:
            continue
        method = getattr(cls, k)
        if hasattr(method, "_clisync"):
            if method._clisync is False:
                continue
        if requires_decorator:
            if not hasattr(method, "_clisync") or getattr(method, "_clisync") is False:
                continue
        rv.append(cls.__name__ + "." + k)
    rv.sort()
    return rv

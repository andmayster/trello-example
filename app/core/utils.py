from importlib import import_module
from pkgutil import walk_packages


def autodiscover() -> None:
    module = import_module("api")
    for module_info in walk_packages(module.__path__, f"{module.__name__}."):
        import_module(module_info.name)
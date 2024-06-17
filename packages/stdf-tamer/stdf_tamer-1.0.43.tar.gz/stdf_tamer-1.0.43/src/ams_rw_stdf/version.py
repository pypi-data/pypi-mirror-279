try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version


version = version("stdf-tamer")

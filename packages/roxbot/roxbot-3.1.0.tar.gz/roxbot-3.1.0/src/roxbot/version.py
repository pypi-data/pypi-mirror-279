from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("roxbot")
except PackageNotFoundError:
    # Package is not installed, and therefore, version is unknown.
    __version__ = "0.0.0+unknown"

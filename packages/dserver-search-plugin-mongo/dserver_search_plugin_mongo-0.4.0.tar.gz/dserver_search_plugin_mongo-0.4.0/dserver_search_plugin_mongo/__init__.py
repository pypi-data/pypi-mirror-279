"""dserver-search-plugin-mongo package."""

import logging

logger = logging.getLogger(__name__)

# workaround for diverging python versions:
try:
    from importlib.metadata import version, PackageNotFoundError
    logger.debug("imported version, PackageNotFoundError from importlib.metadata")
except ModuleNotFoundError:
    from importlib_metadata import version, PackageNotFoundError
    logger.debug("imported version, PackageNotFoundError from importlib_metadata")

# first, try to determine dynamic version at runtime
try:
    __version__ = version(__name__)
    logger.debug("Determined version %s via importlib_metadata.version", __version__)
except PackageNotFoundError:
    # if that fails, check for static version file written by setuptools_scm
    try:
        from .version import version as __version__
        logger.debug("Determined version %s from autogenerated dserver_search_plugin_mongo/version.py", __version__)
    except:
        logger.debug("All efforts to determine version failed.")
        __version__ = None
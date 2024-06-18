"""CometD client for asyncio"""
import logging

from aiocometd_ng._metadata import VERSION as __version__  # noqa: F401
from aiocometd_ng.client import Client  # noqa: F401
from aiocometd_ng.constants import ConnectionType  # noqa: F401
from aiocometd_ng.extensions import Extension, AuthExtension  # noqa: F401
from aiocometd_ng import transports  # noqa: F401

# Create a default handler to avoid warnings in applications without logging
# configuration
logging.getLogger(__name__).addHandler(logging.NullHandler())

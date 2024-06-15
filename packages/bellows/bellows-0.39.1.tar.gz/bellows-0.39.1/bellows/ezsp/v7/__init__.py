""""EZSP Protocol version 7 protocol handler."""
import logging

import voluptuous

import bellows.config

from . import commands, config, types as v7_types
from ..v6 import EZSPv6

LOGGER = logging.getLogger(__name__)


class EZSPv7(EZSPv6):
    """EZSP Version 7 Protocol version handler."""

    VERSION = 7
    COMMANDS = commands.COMMANDS
    SCHEMAS = {
        bellows.config.CONF_EZSP_CONFIG: voluptuous.Schema(config.EZSP_SCHEMA),
        bellows.config.CONF_EZSP_POLICIES: voluptuous.Schema(config.EZSP_POLICIES_SCH),
    }
    types = v7_types

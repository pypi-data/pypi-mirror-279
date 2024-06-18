"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional

from encommon.config import Params as _Params

from enconnect.philipshue import (
    BridgeParams as PhueBridgeParams)
from enconnect.ubiquiti import (
    RouterParams as UbiqRouterParams)

from ..homie import HomieActionParams
from ..homie import HomieDesireParams
from ..homie import HomieGroupParams
from ..homie import HomieSceneParams
from ..philipshue import PhueDeviceParams
from ..ubiquiti import UbiqClientParams



_GROUPS = dict[str, HomieGroupParams]
_SCENES = dict[str, HomieSceneParams]
_DESIRES = dict[str, HomieDesireParams]
_ACTIONS = dict[str, HomieActionParams]

_PHUE_BRIDGES = dict[str, PhueBridgeParams]
_PHUE_DEVICES = dict[str, PhueDeviceParams]
_UBIQ_ROUTERS = dict[str, UbiqRouterParams]
_UBIQ_CLIENTS = dict[str, UbiqClientParams]



class Params(_Params, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    .. note::
       Input parameters are not defined, check parent class.

    :param cache: Optional cache file but required if state
        between executions is required; when in production.
    :param dryrun: Determine we should not change anything.
    :param sargs: Additional arguments on the command line.
    :param groups: Dictionary of parameters for the groups.
    :param scenes: Dictionary of parameters for the scenes.
    :param desires: List of desired states and conditionals.
    :param actions: List of event actions and conditionals.
    :param phue_bridges: Paramters for the product bridges.
    :param phue_devices: Paramters for the product devices.
    :param ubiq_routers: Paramters for the product routers.
    :param ubiq_clients: Paramters for the product clients.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    cache: str = 'sqlite:///:memory:'

    dryrun: bool = False

    sargs: Optional[dict[str, Any]] = None

    groups: Optional[_GROUPS] = None
    scenes: Optional[_SCENES] = None
    desires: Optional[_DESIRES] = None
    actions: Optional[_ACTIONS] = None

    phue_bridges: Optional[_PHUE_BRIDGES] = None
    phue_devices: Optional[_PHUE_DEVICES] = None
    ubiq_routers: Optional[_UBIQ_ROUTERS] = None
    ubiq_clients: Optional[_UBIQ_CLIENTS] = None

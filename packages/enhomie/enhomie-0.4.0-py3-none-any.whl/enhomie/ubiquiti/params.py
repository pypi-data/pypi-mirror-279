"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional

from pydantic import BaseModel



class UbiqClientParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param router: Name of router where the client belongs.
    :param ubid: Unique identifier for client within router.
    :param mac: Identify the client by using the MAC address.
    :param ip: Identify the client by using the IP address.
    :param label: Name of the client to find within router.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    router: Optional[str] = None
    ubid: Optional[str] = None

    mac: Optional[str] = None
    ip: Optional[str] = None
    label: Optional[str] = None


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(**data)

        router = self.router
        ubid = self.ubid
        mac = self.mac
        ip = self.ip
        label = self.label

        if ubid is not None:
            assert router is not None

        if ubid is None:
            assert mac or ip or label



class WhenUbiqClientParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param routers: List of routers in scope for conditional.
    :param clients: List of clients in scope for conditional.
    :param since: Minimum required time post change occurred.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    routers: Optional[list[str]] = None
    clients: list[str]

    since: int = 0

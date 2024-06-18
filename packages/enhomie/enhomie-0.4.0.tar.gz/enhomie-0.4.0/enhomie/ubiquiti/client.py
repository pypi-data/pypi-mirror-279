"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Literal
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Times

if TYPE_CHECKING:
    from .params import UbiqClientParams
    from .router import UbiqRouter  # noqa: F401
    from .router import _FETCH  # noqa: F401
    from ..homie import Homie



_SOURCES = dict[str, '_FETCH']
_ROUTERS = dict[str, 'UbiqRouter']



class UbiqClient:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: 'UbiqClientParams'

    __name: str

    __sources: Optional[_SOURCES]
    __routers: Optional[_ROUTERS]


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.log_d(
            base='UbiqClient',
            name=name,
            status='initial')


        clients = (
            homie.params
            .ubiq_clients)

        assert clients is not None

        params = clients[name]


        self.__homie = homie
        self.__params = params
        self.__name = name
        self.__sources = None
        self.__routers = None


        self.__validate_params()

        homie.log_d(
            base='UbiqClient',
            name=name,
            status='created')


    def __validate_params(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        routers = self.homie.ubiq_routers
        router_name = self.params.router

        assert routers is not None
        assert (
            router_name in routers
            or router_name is None)


    def refresh_source(
        self,
    ) -> None:
        """
        Update the class instance from cached upstream response.
        """

        homie = self.homie
        routers = homie.ubiq_routers
        params = self.params

        assert routers is not None

        _sources: _SOURCES = {}
        _routers: _ROUTERS = {}


        expect = params.router

        for router in routers.values():

            name = router.name

            if (expect is not None
                    and expect != name):
                continue


            found = router.get_source(
                ubid=(
                    params.ubid
                    or params.mac
                    or params.ip),
                label=params.label)

            if found is None:
                continue


            _sources[name] = found
            _routers[name] = router


        self.__sources = _sources or None
        self.__routers = _routers or None


    @property
    def homie(
        self,
    ) -> 'Homie':
        """
        Return the Homie instance to which this instance belongs.

        :returns: Homie instance to which this instance belongs.
        """

        return self.__homie


    @property
    def params(
        self,
    ) -> 'UbiqClientParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def name(
        self,
    ) -> str:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__name


    @property
    def routers(
        self,
    ) -> Optional[_ROUTERS]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.__routers is None:
            return None

        return dict(self.__routers)


    @property
    def sources(
        self,
    ) -> Optional[_SOURCES]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.__sources is None:
            return None

        return deepcopy(self.__sources)


    @property
    def uniques(
        self,
    ) -> Optional[dict[str, str]]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        sources = self.__sources

        if sources is None:
            return None

        ubid: dict[str, str] = {}

        items = sources.items()

        for key, value in items:
            ubid[key] = value['_id']

        return ubid


    @property
    def present(
        self,
    ) -> list[str] | Literal[False]:
        """
        Return the list of routers which the client is present.

        :returns: List of routers which the client is present,
            or `False` boolean when not present on any routers.
        """

        return (
            list(self.__sources)
            if self.__sources is not None
            else False)


    @property
    def connect(
        self,
    ) -> list[str] | Literal[False]:
        """
        Return the list of routers which the client is connected.

        :returns: List of routers which the client is connected,
            or `False` boolean when not connected to any routers.
        """

        routers: list[str] = []

        sources = self.__sources

        if sources is None:
            return False


        items = sources.items()

        for name, source in items:

            connect = False

            if '_uptime_by_ugw' in source:
                connect = True

            if '_uptime_by_uap' in source:
                connect = True

            if connect is True:
                routers.append(name)


        return routers or False


    @property
    def lastseen(
        self,
    ) -> Optional[dict[str, Times]]:
        """
        Return the last time that the device was seen by router.

        :returns: Last time that the device was seen by router.
        """

        returned: dict[str, Times] = {}

        sources = self.__sources

        if sources is None:
            return None


        items1 = sources.items()

        for name, source in items1:

            lseen = max(
                source['last_seen'])

            returned |= {
                name: Times(lseen)}


        times: Optional[Times] = None


        items2 = returned.items()

        for name, _times in items2:

            if (times is None
                    or _times > times):
                times = _times

        if times is not None:
            returned['_latest'] = times


        return returned or None


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :returns: Content related to the project dumper script.
        """

        params = (
            self.params.model_dump())

        self.refresh_source()

        return {
            'name': self.name,
            'uniques': self.uniques,
            'present': self.present,
            'connect': self.connect,
            'params': params}

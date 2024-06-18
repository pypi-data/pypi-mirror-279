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

from encommon.times import Timer
from encommon.times import Times
from encommon.types import merge_dicts
from encommon.types import striplower

from enconnect.ubiquiti import Router
from enconnect.ubiquiti import RouterParams

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

if TYPE_CHECKING:
    from ..homie import Homie



_FETCH = dict[str, Any]
_RAWDEV = dict[str, dict[str, Any]]



disable_warnings(
    category=InsecureRequestWarning)



class UbiqRouter:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: RouterParams
    __router: Router

    __name: str

    __fetched: Optional[dict[str, _FETCH]]
    __timer: Timer
    __merged: Optional[_RAWDEV]


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.log_d(
            base='UbiqRouter',
            name=name,
            status='initial')


        routers = (
            homie.params
            .ubiq_routers)

        assert routers is not None

        params = routers[name]


        self.__homie = homie
        self.__params = params
        self.__router = Router(params)
        self.__name = name
        self.__fetched = None
        self.__merged = None


        self.__timer = Timer(
            60, start='-60s')


        homie.log_d(
            base='UbiqRouter',
            name=name,
            status='created')


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
    ) -> RouterParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def router(
        self,
    ) -> Router:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__router


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
    def connect(
        self,
    ) -> bool:
        """
        Return the boolean indicating connection is established.

        :returns: Boolean indicating connection is established.
        """

        return bool(self.__merged)


    @property
    def fetched(
        self,
    ) -> _FETCH:
        """
        Collect the complete dump of all known clients in router.

        :returns: Complete dump of all known clients in router.
        """

        fetched = self.__fetched
        timer = self.__timer
        router = self.__router
        request = router.request_proxy

        ready = timer.ready(False)

        if fetched and not ready:
            return deepcopy(fetched)

        runtime = Times()


        response = request(
            'get', 'rest/user')

        historic = response.json()

        assert isinstance(historic, dict)


        response = request(
            'get', 'stat/sta')

        realtime = response.json()

        assert isinstance(realtime, dict)


        fetched = {
            'historic': historic,
            'realtime': realtime}


        self.homie.log_i(
            base='UbiqRouter',
            name=self.name,
            action='fetch',
            elapsed=runtime.since,
            status='success')


        self.__fetched = fetched
        self.__merged = None

        timer.update()

        return deepcopy(fetched)


    @property
    def merged(
        self,
    ) -> _RAWDEV:
        """
        Process the response and perform common transformations.

        :returns: Compiled response from the upstream endpoint.
        """

        staged: _RAWDEV = {}
        source: _RAWDEV = {}

        merged = self.__merged

        if merged is not None:
            return deepcopy(merged)

        fetched = self.fetched


        historic = (
            fetched['historic']['data'])

        realtime = (
            fetched['realtime']['data'])


        def _fixtimes(
            fetch: _FETCH,
        ) -> None:

            if 'first_seen' in item:
                item['first_seen'] = [
                    item['first_seen']]

            if 'last_seen' in item:
                item['last_seen'] = [
                    item['last_seen']]


        def _combine(
            target: Literal['historic', 'realtime'],
        ) -> None:

            ubid = item['_id']

            if ubid not in staged:
                staged[ubid] = {}

            source = staged[ubid]

            assert target not in source

            _fixtimes(item)

            source[target] = (
                deepcopy(item))


        for item in historic:
            _combine('historic')

        for item in realtime:
            _combine('realtime')


        items = staged.items()

        for ubid, fetch in items:

            historic = (
                fetch.get('historic', {}))

            realtime = (
                fetch.get('realtime', {}))

            _fetch: _FETCH = (
                deepcopy(historic))

            merge_dicts(
                dict1=_fetch,
                dict2=deepcopy(realtime),
                force=True)

            source[ubid] = _fetch | {
                '_historic': historic,
                '_realtime': _fetch}


        self.__merged = source

        return deepcopy(source)


    def get_source(
        self,
        ubid: Optional[str] = None,
        label: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param ubid: Used for filtering resources for matching.
        :param label: Used for filtering resources for matching.
        :returns: Information for matching client from upstream.
        """

        assert ubid or label

        if ubid is not None:
            return self.get_source_ubid(ubid)

        if label is not None:
            return self.get_source_label(label)

        return None  # NOCVR


    def get_source_ubid(
        self,
        ubid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param ubid: Used for filtering resources for matching.
        :returns: Information for matching client from upstream.
        """

        found: list[_FETCH] = []

        items = self.merged.items()

        for _ubid, fetch in items:

            values = [striplower(_ubid)]

            if 'mac' in fetch:
                values.append(
                    striplower(fetch['mac']))

            if 'ip' in fetch:
                values.append(
                    striplower(fetch['ip']))

            if ubid not in values:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def get_source_label(
        self,
        label: str,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param label: Used for filtering resources for matching.
        :returns: Information for matching client from upstream.
        """

        found: list[_FETCH] = []

        label = striplower(label)

        items = self.merged.items()

        for _ubid, fetch in items:

            values: list[str] = []

            if fetch.get('hostname'):
                values.append(
                    striplower(fetch['hostname']))

            if fetch.get('name'):
                values.append(
                    striplower(fetch['name']))

            if label not in values:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :returns: Content related to the project dumper script.
        """

        params = deepcopy(
            self.params.model_dump())

        params['password'] = (
            '*' * len(params['password']))

        return {
            'name': self.name,
            'connect': self.connect,
            'params': params}

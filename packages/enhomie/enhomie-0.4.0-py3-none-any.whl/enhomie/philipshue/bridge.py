"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from copy import deepcopy
from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timer
from encommon.times import Times
from encommon.types import striplower

from enconnect.philipshue import Bridge
from enconnect.philipshue import BridgeParams

if TYPE_CHECKING:
    from ..homie import Homie



_FETCH = dict[str, Any]
_RAWDEV = dict[str, dict[str, Any]]



class PhueBridge:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: BridgeParams
    __bridge: Bridge

    __name: str

    __fetched: Optional[_FETCH]
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
            base='PhueBridge',
            name=name,
            status='initial')


        bridges = (
            homie.params
            .phue_bridges)

        assert bridges is not None

        params = bridges[name]


        self.__homie = homie
        self.__params = params
        self.__bridge = Bridge(params)
        self.__name = name
        self.__fetched = None
        self.__merged = None


        self.__timer = Timer(
            60, start='-60s')


        homie.log_d(
            base='PhueBridge',
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
    ) -> BridgeParams:
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def bridge(
        self,
    ) -> Bridge:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return self.__bridge


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
        Collect the complete dump of all resources within bridge.

        :returns: Complete dump of all resources within bridge.
        """

        fetched = self.__fetched
        timer = self.__timer
        bridge = self.__bridge
        request = bridge.request

        ready = timer.ready(False)

        if fetched and not ready:
            return deepcopy(fetched)

        runtime = Times()


        response = request(
            'get', 'resource')

        response.raise_for_status()

        fetched = response.json()

        assert isinstance(fetched, dict)


        self.homie.log_i(
            base='PhueBridge',
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

        merged = self.__merged

        if merged is not None:
            return deepcopy(merged)

        fetched = self.fetched


        source = {
            x['id']: x for x in
            fetched['data']}

        origin = deepcopy(source)


        def _enhance() -> None:

            rtype = item['rtype']
            rid = item['rid']

            if 'taurus_' in rtype:
                return

            item['_source'] = (
                origin[rid])


        items1 = source.items()

        for key, value in items1:

            if 'services' not in value:
                continue

            items2 = value['services']

            for item in items2:
                _enhance()


        self.__merged = source

        return deepcopy(source)


    def get_source(
        self,
        phid: Optional[str] = None,
        label: Optional[str] = None,
        type: Optional[str] = None,
        grid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param phid: Used for filtering resources for matching.
        :param label: Used for filtering resources for matching.
        :param type: Used for filtering resources for matching.
        :param grid: Used for filtering resources for matching.
        :returns: Information for matching resource in upstream.
        """

        assert phid or label

        if phid is not None:
            return self.get_source_phid(
                phid, type, grid)

        if label is not None:
            return self.get_source_label(
                label, type, grid)

        return None  # NOCVR


    def get_source_phid(
        self,
        phid: str,
        type: Optional[str] = None,
        grid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param phid: Used for filtering resources for matching.
        :param type: Used for filtering resources for matching.
        :param grid: Used for filtering resources for matching.
        :returns: Information for matching resource in upstream.
        """

        found: list[_FETCH] = []

        items = self.merged.items()

        for _phid, fetch in items:

            _type = fetch['type']

            if type and _type != type:
                continue

            _grid: Optional[str] = (
                fetch.get('group', {})
                .get('rid'))

            if grid and _grid != grid:
                continue

            if _phid != phid:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def get_source_label(
        self,
        label: str,
        type: Optional[str] = None,
        grid: Optional[str] = None,
    ) -> Optional[_FETCH]:
        """
        Enumerate and collect information from cached response.

        :param label: Used for filtering resources for matching.
        :param type: Used for filtering resources for matching.
        :param grid: Used for filtering resources for matching.
        :returns: Information for matching resource in upstream.
        """

        found: list[_FETCH] = []

        label = striplower(label)

        items = self.merged.items()

        for phid, fetch in items:

            _type = fetch['type']

            if type and _type != type:
                continue

            _grid: Optional[str] = (
                fetch.get('group', {})
                .get('rid'))

            if grid and _grid != grid:
                continue

            if 'metadata' not in fetch:
                continue

            metadata = fetch['metadata']

            if 'owner' in fetch:
                continue

            name = striplower(
                metadata['name'])

            if name != label:
                continue

            found.append(fetch)

        assert len(found) in [0, 1]

        return found[0] if found else None


    def scene_get(
        self,
        group_phid: str,
    ) -> Optional[str]:
        # pylint: disable=E1133
        """
        Return the current active scene when there is one active.

        :param group_phid: Unique identifier of scene in bridge.
        :returns: Current active scene when there is one active.
        """

        items = self.merged.items()

        for phid, fetch in items:

            if 'group' not in fetch:
                continue

            _group = fetch['group']
            _phid = _group['rid']

            if _phid != group_phid:
                continue

            status = fetch['status']
            active = status['active']

            if active == 'static':
                return phid

        return None


    def scene_set(
        self,
        scene_phid: str,
    ) -> None:
        """
        Activate the provided scene unique identifier in bridge.

        :param scene_phid: Unique identifier of scene in bridge.
        """

        self.homie.log_d(
            base='PhueBridge',
            action='scene_set',
            scene=scene_phid,
            status='attempt')

        runtime = Times()

        path = (
            'resource/scene'
            f'/{scene_phid}')

        action = {'action': 'active'}
        payload = {'recall': action}

        self.bridge.request(
            method='put',
            path=path,
            json=payload)

        self.homie.log_d(
            base='PhueBridge',
            action='scene_set',
            scene=scene_phid,
            elapsed=runtime.since,
            status='success')


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :returns: Content related to the project dumper script.
        """

        params = deepcopy(
            self.params.model_dump())

        params['token'] = (
            '*' * len(params['token']))

        return {
            'name': self.name,
            'connect': self.connect,
            'params': params}

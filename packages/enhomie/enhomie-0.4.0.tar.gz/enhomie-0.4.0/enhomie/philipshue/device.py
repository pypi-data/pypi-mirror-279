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

from encommon.times import Duration
from encommon.times import Times
from encommon.types import getate

if TYPE_CHECKING:
    from .bridge import _FETCH
    from .bridge import PhueBridge
    from .params import PhueDeviceParams
    from ..homie import Homie



_CHANGED = dict[str, Times | None] | Literal[False]
_SENSORS = Optional[dict[str, str]]



class PhueDevice:
    """
    Contain the relevant attributes about the related device.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: 'PhueDeviceParams'

    __name: str

    __source: Optional['_FETCH']
    __bridge: Optional['PhueBridge']


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.log_d(
            base='PhueDevice',
            name=name,
            status='initial')


        devices = (
            homie.params
            .phue_devices)

        assert devices is not None

        params = devices[name]


        self.__homie = homie
        self.__params = params
        self.__name = name
        self.__source = None
        self.__bridge = None


        self.__validate_params()

        homie.log_d(
            base='PhueDevice',
            name=name,
            status='created')


    def __validate_params(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        bridges = self.homie.phue_bridges
        bridge_name = self.params.bridge

        assert bridges is not None
        assert bridge_name in bridges


    def refresh_source(
        self,
    ) -> None:
        """
        Update the class instance from cached upstream response.
        """

        homie = self.homie
        bridges = homie.phue_bridges
        params = self.params

        assert bridges is not None

        self.__source = None
        self.__bridge = None


        expect = params.bridge

        for bridge in bridges.values():

            name = bridge.name

            if expect != name:
                continue


            found = bridge.get_source(
                phid=params.phid,
                label=params.label,
                type='device')

            if found is None:
                continue


            _type = found['type']

            assert _type == 'device'

            assert not self.__source

            self.__source = found
            self.__bridge = bridge


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
    ) -> 'PhueDeviceParams':
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
    def bridge(
        self,
    ) -> Optional['PhueBridge']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.__bridge is None:
            return None

        return self.__bridge


    @property
    def source(
        self,
    ) -> Optional['_FETCH']:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        if self.__source is None:
            return None

        return deepcopy(self.__source)


    @property
    def unique(
        self,
    ) -> Optional[str]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        source = self.__source

        if source is None:
            return None

        phid = source['id']

        assert isinstance(phid, str)

        return phid


    @property
    def present(
        self,
    ) -> bool:
        """
        Return the boolean indicating device present on bridge.

        :returns: Boolean indicating device present on bridge.
        """

        return self.__source is not None


    @property
    def connect(
        self,
    ) -> bool:
        """
        Return the boolean indicating device connected to bridge.

        :returns: Boolean indicating device connected to bridge.
        """

        source = self.__source

        key = 'zigbee_connectivity'

        if source is None:
            return False


        services = source['services']

        connect = False

        for service in services:

            rtype = service['rtype']

            if rtype != key:
                continue

            origin = service['_source']
            status = origin['status']

            if status == 'connected':
                connect = True


        return connect


    @property
    def changed(
        self,
    ) -> _CHANGED:
        """
        Return the related information for services have changed.

        :returns: Related information for services have changed.
        """

        keys = ['button', 'motion']

        source = self.__source

        if source is None:
            return False


        services = source['services']

        changed: dict[str, Times | None] = {}
        indices = {x: 0 for x in keys}

        for service in services:

            _rtype = service['rtype']

            if _rtype not in keys:
                continue

            indices[_rtype] += 1

            _changed: Optional[str] = None

            _source = service['_source']

            if _rtype == 'motion':
                _changed = getate(
                    _source['motion'],
                    'motion_report/changed')

            elif _rtype == 'button':
                _changed = getate(
                    _source['button'],
                    'button_report/updated')

            index = indices[_rtype]

            key = f'{_rtype}{index}'

            changed[key] = (
                Times(_changed)
                if _changed is not None
                else None)


        values = changed.values()

        return changed if any(values) else False


    @property
    def sensors(
        self,
    ) -> _SENSORS:
        """
        Return the mapping for sensor name to unique identifier.

        :returns: Mapping for sensor name to unique identifier.
        """

        keys = ['button', 'motion']

        source = self.__source

        if source is None:
            return None


        services = source['services']

        sensors: dict[str, str] = {}
        indices = {x: 0 for x in keys}

        for service in services:

            _rid = service['rid']
            _rtype = service['rtype']

            if _rtype not in keys:
                continue

            indices[_rtype] += 1

            index = indices[_rtype]

            key = f'{_rtype}{index}'

            sensors[key] = _rid


        return sensors or None


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

        changed: dict[str, Any] = {}


        if self.changed is not False:

            items = self.changed.items()

            for key, value in items:

                if value is None:
                    continue

                value = Times(value)

                durate = Duration(
                    value.since, groups=2)

                changed[key] = {
                    'stamp': value,
                    'since': durate}


        return {
            'name': self.name,
            'unique': self.unique,
            'present': self.present,
            'connect': self.connect,
            'changed': changed or False,
            'params': params}

"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .homie import Homie
    from .params import GROUP_TYPES
    from .params import HomieGroupParams
    from .scene import HomieScene
    from ..philipshue import PhueBridge
    from ..philipshue.bridge import (
        _FETCH as PHUE_FETCH)



class HomieGroup:
    """
    Normalize the group parameter across multiple products.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: 'HomieGroupParams'

    __name: str


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.log_d(
            base='HomieGroup',
            name=name,
            status='initial')


        groups = (
            homie.params.groups)

        assert groups is not None

        params = groups[name]


        self.__homie = homie
        self.__params = params
        self.__name = name


        self.__validate_params()

        homie.log_d(
            base='HomieGroup',
            name=name,
            status='created')


    def __validate_params(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        bridges = self.homie.phue_bridges
        bridge_name = self.params.phue_bridge

        assert bridges is not None
        assert bridge_name in bridges


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
    ) -> 'HomieGroupParams':
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
    def type(
        self,
    ) -> 'GROUP_TYPES':
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.type


    @property
    def phue_bridge(
        self,
    ) -> 'PhueBridge':
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        bridges = self.homie.phue_bridges
        bridge_name = self.params.phue_bridge

        assert bridges is not None

        return bridges[bridge_name]


    @property
    def phue_source(
        self,
    ) -> Optional['PHUE_FETCH']:
        """
        Return the dictionary containing the source from bridge.

        :returns: Dictionary containing the source from bridge.
        """

        bridge = self.phue_bridge

        return bridge.get_source(
            label=self.params.phue_label,
            type=self.type)


    @property
    def phue_unique(
        self,
    ) -> Optional[str]:
        """
        Return the unique identifier of group within the bridge.

        :returns: Unique identifier of group within the bridge.
        """

        source = self.phue_source

        if source is None:
            return None

        phid = source['id']

        assert isinstance(phid, str)

        return phid


    @property
    def phue_actual(
        self,
    ) -> Optional[str]:
        """
        Return the actual name for the group within the bridge.

        :returns: Actual name for the group within the bridge.
        """

        source = self.phue_source

        if source is None:
            return None

        metadata = source['metadata']
        name = metadata['name']

        assert isinstance(name, str)

        return name


    def scene_set(
        self,
        scene: 'HomieScene',
    ) -> None:
        """
        Update the current group to activate the provided scene.

        :param scene: Scene instance that will be used in match.
        """

        scene.scene_set(self)


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :returns: Content related to the project dumper script.
        """

        params = (
            self.params.model_dump())

        phue_actual = self.phue_actual
        phue_unique = self.phue_unique
        phue_bridge = self.phue_bridge.name

        return {
            'name': self.name,
            'type': self.type,
            'present': bool(phue_unique),
            'phue_bridge': phue_bridge,
            'phue_unique': phue_unique,
            'phue_actual': phue_actual,
            'params': params}

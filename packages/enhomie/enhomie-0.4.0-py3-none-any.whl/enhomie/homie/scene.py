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
    from .group import HomieGroup
    from .params import HomieSceneParams
    from ..philipshue.bridge import (
        _FETCH as PHUE_FETCH)



class HomieScene:
    """
    Normalize the scene parameter across multiple products.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: 'HomieSceneParams'

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
            base='HomieScene',
            name=name,
            status='initial')


        scenes = (
            homie.params.scenes)

        assert scenes is not None

        params = scenes[name]


        self.__homie = homie
        self.__params = params
        self.__name = name


        homie.log_d(
            base='HomieScene',
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
    ) -> 'HomieSceneParams':
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


    def phue_source(
        self,
        group: 'HomieGroup',
    ) -> Optional['PHUE_FETCH']:
        """
        Return the dictionary containing the source from bridge.

        .. note::
           Scenes only exist within the groups on the bridge.

        :param group: Group from wherein the scene is located.
        :returns: Dictionary containing the source from bridge.
        """

        bridge = group.phue_bridge

        label = self.params.phue_label
        group_phid = group.phue_unique

        assert group_phid is not None

        return bridge.get_source(
            label=label,
            type='scene',
            grid=group_phid)


    def phue_unique(
        self,
        group: 'HomieGroup',
    ) -> Optional[str]:
        """
        Return the unique identifier of scene within the bridge.

        .. note::
           Scenes only exist within the groups on the bridge.

        :param group: Group from wherein the scene is located.
        :returns: Unique identifier of scene within the bridge.
        """

        source = (
            self.phue_source(group))

        if source is None:
            return None

        phid = source['id']

        assert isinstance(phid, str)

        return phid


    def phue_actual(
        self,
        group: 'HomieGroup',
    ) -> Optional[str]:
        """
        Return the actual name for the scene within the bridge.

        .. note::
           Scenes only exist within the groups on the bridge.

        :param group: Group from wherein the scene is located.
        :returns: Actual name for the scene within the bridge.
        """

        source = (
            self.phue_source(group))

        if source is None:
            return None

        metadata = source['metadata']
        name = metadata['name']

        assert isinstance(name, str)

        return name


    def phue_active(
        self,
        group: 'HomieGroup',
    ) -> Optional[bool]:
        """
        Return the boolean indicating when this is active scene.

        .. note::
           Scenes only exist within the groups on the bridge.

        :param group: Group from wherein the scene is located.
        :returns: Boolean indicating whether the scene active.
        """

        bridge = group.phue_bridge

        group_phid = group.phue_unique

        assert group_phid is not None

        crrnt_phid = (
            bridge.scene_get(group_phid))

        scene_phid = (
            self.phue_unique(group))

        return crrnt_phid == scene_phid


    def scene_set(
        self,
        group: 'HomieGroup',
    ) -> None:
        """
        Update the current group to activate the provided scene.

        :param group: Group from wherein the scene is located.
        """

        bridge = group.phue_bridge

        scene_phid = (
            self.phue_unique(group))

        assert scene_phid is not None

        bridge.scene_set(scene_phid)


    def homie_dumper(
        self,
        group: Optional['HomieGroup'] = None,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :param group: Group from wherein the scene is located.
        :returns: Content related to the project dumper script.
        """

        params = (
            self.params.model_dump())

        phue_actual: Optional[str] = None
        phue_unique: Optional[str] = None

        present: bool = False


        if group is not None:

            phue_actual = (
                self.phue_actual(group))

            phue_unique = (
                self.phue_unique(group))

            if phue_unique is not None:
                present = True


        return {
            'name': self.name,
            'present': present,
            'phue_unique': phue_unique,
            'phue_actual': phue_actual,
            'params': params}

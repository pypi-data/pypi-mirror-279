"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import Timers
from encommon.types import sort_dict

from .action import HomieAction
from .desire import HomieDesire
from .group import HomieGroup
from .scene import HomieScene
from ..philipshue import PhueBridge
from ..philipshue import PhueDevice
from ..ubiquiti import UbiqClient
from ..ubiquiti import UbiqRouter

if TYPE_CHECKING:
    from ..config import Config
    from ..config import Params



_DESIRES = dict[str, list[HomieDesire]]
_DESIRED = dict[str, HomieDesire]

_ASPIRES = dict[str, list[HomieAction]]
_ASPIRED = dict[str, HomieAction]



class Homie:
    """
    Interact with supported devices to ensure desired state.

    :param config: Primary class instance for configuration.
    """

    __config: 'Config'
    __timers: Timers

    __phue_bridges: dict[str, PhueBridge]
    __phue_devices: dict[str, PhueDevice]
    __ubiq_routers: dict[str, UbiqRouter]
    __ubiq_clients: dict[str, UbiqClient]

    __groups: dict[str, HomieGroup]
    __scenes: dict[str, HomieScene]
    __desires: dict[str, HomieDesire]
    __actions: dict[str, HomieAction]


    def __init__(
        self,
        config: 'Config',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__config = config

        self.__make_timers()

        self.__phue_bridges = {}
        self.__phue_devices = {}
        self.__ubiq_routers = {}
        self.__ubiq_clients = {}

        self.__groups = {}
        self.__scenes = {}
        self.__desires = {}
        self.__actions = {}

        self.log_d(
            base='Homie',
            status='initial')


        self.__make_phue_bridges()
        self.__make_phue_devices()
        self.__make_ubiq_routers()
        self.__make_ubiq_clients()

        self.__make_groups()
        self.__make_scenes()
        self.__make_desires()
        self.__make_actions()


        self.__validate_params()

        self.log_i(
            base='Homie',
            status='created')


    def __validate_params(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        groups = self.groups
        phue_bridges = self.phue_bridges


        def _validate_groups() -> None:

            assert phue_bridges is not None

            for group in groups.values():

                params = group.params

                name = params.phue_bridge

                assert name in phue_bridges


        if groups is not None:
            _validate_groups()


    def __make_timers(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        cache = self.params.cache

        timers = Timers(store=cache)

        self.__timers = timers


    def __make_groups(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        groups = params.groups

        if groups is None:
            return

        for name in groups.keys():

            group = HomieGroup(self, name)

            self.__groups |= {
                group.name: group}


    def __make_scenes(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        scenes = params.scenes

        if scenes is None:
            return

        for name in scenes.keys():

            scene = HomieScene(self, name)

            self.__scenes |= {
                scene.name: scene}


    def __make_desires(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        desires = params.desires

        if desires is None:
            return

        for name in desires.keys():

            desire = HomieDesire(self, name)

            self.__desires |= {
                desire.name: desire}


    def __make_actions(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        actions = params.actions

        if actions is None:
            return

        for name in actions.keys():

            action = HomieAction(self, name)

            self.__actions |= {
                action.name: action}


    def __make_phue_bridges(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        bridges = params.phue_bridges

        if bridges is None:
            return

        for name in bridges.keys():

            bridge = PhueBridge(self, name)

            self.__phue_bridges |= {
                bridge.name: bridge}


    def __make_phue_devices(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        devices = params.phue_devices

        if devices is None:
            return

        for name in devices.keys():

            device = PhueDevice(self, name)

            self.__phue_devices |= {
                device.name: device}


    def __make_ubiq_routers(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        routers = params.ubiq_routers

        if routers is None:
            return

        for name in routers.keys():

            router = UbiqRouter(self, name)

            self.__ubiq_routers |= {
                router.name: router}


    def __make_ubiq_clients(
        self,
    ) -> None:
        """
        Construct instances using the configuration parameters.
        """

        params = self.params
        clients = params.ubiq_clients

        if clients is None:
            return

        for name in clients.keys():

            client = UbiqClient(self, name)

            self.__ubiq_clients |= {
                client.name: client}


    def log(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log`.

        :param args: Positional arguments passed for downstream.
        :param kwargs: Keyword arguments for populating message.
        """

        config = self.config
        logger = config.logger

        logger.log(*args, **kwargs)


    def log_c(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_c`.

        :param kwargs: Keyword arguments for populating message.
        """

        config = self.config
        logger = config.logger

        logger.log_c(**kwargs)


    def log_d(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_d`.

        :param kwargs: Keyword arguments for populating message.
        """

        config = self.config
        logger = config.logger

        logger.log_d(**kwargs)


    def log_e(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_e`.

        :param kwargs: Keyword arguments for populating message.
        """

        config = self.config
        logger = config.logger

        logger.log_e(**kwargs)


    def log_i(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_i`.

        :param kwargs: Keyword arguments for populating message.
        """

        config = self.config
        logger = config.logger

        logger.log_i(**kwargs)


    def log_w(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Pass the provided keyword arguments into logger object.

        .. note::
           Uses method :py:meth:`encommon.config.Logger.log_w`.

        :param kwargs: Keyword arguments for populating message.
        """

        config = self.config
        logger = config.logger

        logger.log_w(**kwargs)


    @property
    def config(
        self,
    ) -> 'Config':
        """
        Return the Config instance containing the configuration.

        :returns: Config instance containing the configuration.
        """

        return self.__config


    @property
    def params(
        self,
    ) -> 'Params':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.config.params


    @property
    def timers(
        self,
    ) -> Timers:
        """
        Return the timers instances defined within this instance.

        :returns: Timers instances defined within this instance.
        """

        return self.__timers


    @property
    def groups(
        self,
    ) -> dict[str, HomieGroup]:
        """
        Return the group instances defined within this instance.

        :returns: Group instances defined within this instance.
        """

        return dict(self.__groups)


    @property
    def rooms(
        self,
    ) -> dict[str, HomieGroup]:
        """
        Return the room instances defined within this instance.

        :returns: Room instances defined within this instance.
        """

        return {
            k: v for k, v in
            self.groups.items()
            if v.type == 'room'}


    @property
    def zones(
        self,
    ) -> dict[str, HomieGroup]:
        """
        Return the zone instances defined within this instance.

        :returns: Zone instances defined within this instance.
        """

        return {
            k: v for k, v in
            self.groups.items()
            if v.type == 'zone'}


    @property
    def scenes(
        self,
    ) -> dict[str, HomieScene]:
        """
        Return the scene instances defined within this instance.

        :returns: Scene instances defined within this instance.
        """

        return dict(self.__scenes)


    @property
    def desires(
        self,
    ) -> dict[str, HomieDesire]:
        """
        Return the desire instances defined within this instance.

        :returns: Desire instances defined within this instance.
        """

        return dict(self.__desires)


    @property
    def actions(
        self,
    ) -> dict[str, HomieAction]:
        """
        Return the action instances defined within this instance.

        :returns: Action instances defined within this instance.
        """

        return dict(self.__actions)


    @property
    def phue_bridges(
        self,
    ) -> dict[str, PhueBridge]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__phue_bridges)


    @property
    def phue_devices(
        self,
    ) -> dict[str, PhueDevice]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__phue_devices)


    @property
    def ubiq_routers(
        self,
    ) -> dict[str, UbiqRouter]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__ubiq_routers)


    @property
    def ubiq_clients(
        self,
    ) -> dict[str, UbiqClient]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return dict(self.__ubiq_clients)


    @property
    def desired(
        self,
    ) -> _DESIRED:
        """
        Return the related desired state for the desired groups.

        :returns: Related desired state for the desired groups.
        """

        params = self.params
        dryrun = params.dryrun

        desires: _DESIRES = {}


        def _append_desire() -> None:

            if _name not in desires:
                desires[_name] = []

            target = desires[_name]

            target.append(desire)


        items1 = self.desires.items()

        for name, desire in items1:

            if desire.outcome is False:

                if dryrun is False:
                    desire.delete_timer()

                continue

            if desire.delayed is True:
                continue

            groups = desire.groups

            for _name in groups:
                _append_desire()


        desired: _DESIRED = {}


        items2 = desires.items()

        for key, value in items2:

            value = sorted(
                value,
                key=lambda x: x.weight,
                reverse=True)

            desired[key] = value[0]


        return sort_dict(desired)


    def aspired(
        self,
        event: dict[str, Any],
    ) -> _ASPIRED:
        """
        Return the related actions matching the provided event.

        :param event: Event which was yielded from the stream.
        :returns: Related actions matching the provided event.
        """

        aspires: _ASPIRES = {}


        def _append_aspire() -> None:

            if _name not in aspires:
                aspires[_name] = []

            target = aspires[_name]

            target.append(action)


        items1 = self.actions.items()

        for name, action in items1:

            if action.outcome is False:
                continue

            matched = action.match(event)

            if matched is False:
                continue

            if action.paused is True:
                continue

            groups = action.groups

            for _name in groups:
                _append_aspire()


        aspired: _ASPIRED = {}


        items2 = aspires.items()

        for key, value in items2:

            value = sorted(
                value,
                key=lambda x: x.weight,
                reverse=True)

            aspired[key] = value[0]


        return sort_dict(aspired)


    def scene_get(
        self,
        group: HomieGroup,
    ) -> Optional[HomieScene]:
        """
        Return the current active scene when there is one active.

        :param group: Group from wherein the scene is located.
        :returns: Current active scene when there is one active.
        """

        scenes = self.scenes

        for scene in scenes.values():

            if scene.phue_active(group):
                return scene

        return None


    def scene_set(
        self,
        group: HomieGroup,
        scene: HomieScene,
    ) -> None:
        """
        Update the provided group to activate the provided scene.

        :param group: Group from wherein the scene is located.
        :param scene: Name of the Homie scene which is desired.
        """

        self.log_i(
            base='Homie',
            action='scene_set',
            group=group.name,
            scene=scene.name,
            status='attempt')

        group.scene_set(scene)

        self.log_i(
            base='Homie',
            action='scene_set',
            group=group.name,
            scene=scene.name,
            status='success')


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        :returns: Content related to the project dumper script.
        """

        dumped: dict[str, Any] = {
            'groups': {
                'rooms': sorted(self.rooms),
                'zones': sorted(self.zones)},
            'scenes': sorted(self.scenes),
            'desires': sorted(self.desires),
            'actions': sorted(self.actions)}

        _dumped: dict[str, Any]


        phue_bridges = (
            self.phue_bridges.values())

        _dumped = {}

        for bridge in phue_bridges:
            _dumped[bridge.name] = {
                'connect': bridge.connect}

        dumped['phue_bridges'] = _dumped


        phue_devices = (
            self.phue_devices.values())

        _dumped = {}

        for device in phue_devices:
            device.refresh_source()
            _dumped[device.name] = {
                'present': device.present,
                'connect': device.connect}

        dumped['phue_devices'] = _dumped


        ubiq_routers = (
            self.ubiq_routers.values())

        _dumped = {}

        for router in ubiq_routers:
            _dumped[router.name] = {
                'connect': router.connect}

        dumped['ubiq_routers'] = _dumped


        ubiq_clients = (
            self.ubiq_clients.values())

        _dumped = {}

        for client in ubiq_clients:
            client.refresh_source()
            _dumped[client.name] = {
                'present': client.present,
                'connect': client.connect}

        dumped['ubiq_clients'] = _dumped


        return dumped

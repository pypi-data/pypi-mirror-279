"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional
from typing import TYPE_CHECKING

from encommon.times import TimerParams
from encommon.times.common import PARSABLE

from .what import HomieWhat
from .when import HomieWhen

if TYPE_CHECKING:
    from .homie import Homie
    from .params import HomieActionParams
    from .params import HomieWhatParams
    from .params import HomieWhenParams



_OUTCOMES = dict[str, list[bool]]



class HomieAction:
    """
    Normalize the desired parameter across multiple products.

    :param homie: Primary class instance for Homie Automate.
    :param name: Name of the object within the Homie config.
    """

    __homie: 'Homie'
    __params: 'HomieActionParams'

    __name: str

    __what: list[HomieWhat]
    __when: list[HomieWhen]


    def __init__(
        self,
        homie: 'Homie',
        name: str,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        homie.log_d(
            base='HomieAction',
            name=name,
            status='initial')


        actions = (
            homie.params.actions)

        assert actions is not None

        params = actions[name]


        self.__homie = homie
        self.__params = params
        self.__name = name


        what = self.what or []

        self.__what = [
            HomieWhat(homie, x)
            for x in what]


        when = self.when or []

        self.__when = [
            HomieWhen(homie, x)
            for x in when]


        self.__validate_params()

        homie.log_d(
            base='HomieAction',
            name=name,
            status='created')


    def __validate_params(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        groups = self.homie.groups
        _groups = self.params.groups

        for name in _groups:
            assert name in groups

        scenes = self.homie.scenes
        _scene = self.params.scene

        assert _scene in scenes


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
    ) -> 'HomieActionParams':
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
    def whats(
        self,
    ) -> list[HomieWhat]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return list(self.__what)


    @property
    def whens(
        self,
    ) -> list[HomieWhen]:
        """
        Return the value for the attribute from class instance.

        :returns: Value for the attribute from class instance.
        """

        return list(self.__when)


    @property
    def groups(
        self,
    ) -> list[str]:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.groups


    @property
    def scene(
        self,
    ) -> str:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.scene


    @property
    def weight(
        self,
    ) -> int:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.weight


    @property
    def pause(
        self,
    ) -> int:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.pause


    @property
    def what(
        self,
    ) -> Optional[list['HomieWhatParams']]:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.what


    @property
    def when(
        self,
    ) -> Optional[list['HomieWhenParams']]:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.when


    @property
    def paused(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether action is paused.

        :returns: Boolean indicating whether action is paused.
        """

        homie = self.homie
        timers = homie.timers

        children = timers.children

        name = self.name
        pause = self.pause


        unique = f'action_{name}'

        if unique not in children:

            params = TimerParams(
                pause, f'-{pause}s')

            timers.create(
                unique, params)


        ready = timers.ready(
            unique, update=False)

        return not ready


    def update_timer(
        self,
        value: Optional[PARSABLE] = None,
    ) -> None:
        """
        Update the existing timer from mapping within the cache.

        :param value: Override the time updated for timer value.
        """

        homie = self.homie
        timers = homie.timers

        name = self.name
        unique = f'action_{name}'

        timers.update(
            unique, value or 'now')


    def delete_timer(
        self,
    ) -> None:
        """
        Update the existing timer from mapping within the cache.
        """

        homie = self.homie
        timers = homie.timers

        name = self.name
        unique = f'action_{name}'

        timers.delete(unique)


    @property
    def outcomes(
        self,
    ) -> Optional[_OUTCOMES]:
        """
        Return the dictionaries of boolean groups from conditons.

        .. note::
           This method is highly redundant to that in desire.py.

        :returns: Dictionaries of boolean groups from conditons.
        """

        matched: _OUTCOMES = {}


        for when in self.__when:

            outcome = when.outcome
            family = when.family

            if family not in matched:
                matched[family] = []

            (matched[family]
                .append(outcome))


        return matched or None


    @property
    def outcome(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether conditions matched.

        .. note::
           This method is highly redundant to that in desire.py.

        :returns: Boolean indicating whether conditions matched.
        """

        outcomes = self.outcomes

        if outcomes is None:
            return True

        matched: list[bool] = []


        items = outcomes.items()

        for family, when in items:

            matched.append(
                all(when)
                if family == 'default'
                else any(when))

        assert len(matched) >= 1


        return all(matched)


    def matches(
        self,
        event: dict[str, Any],
    ) -> list[bool]:
        """
        Return the boolean indicating whether conditions matched.

        :param event: Event which was yielded from the stream.
        :returns: Boolean indicating whether conditions matched.
        """

        matches: list[bool] = []


        for what in self.__what:

            match = what.match(event)

            matches.append(match)


        return matches


    def match(
        self,
        event: dict[str, Any],
    ) -> bool:
        """
        Return the boolean indicating whether conditions matched.

        :param event: Event which was yielded from the stream.
        :returns: Boolean indicating whether conditions matched.
        """

        matches = self.matches(event)

        return any(matches)


    def homie_dumper(
        self,
    ) -> dict[str, Any]:
        """
        Return the content related to the project dumper script.

        .. note::
           This method is highly redundant to that in desire.py.

        :returns: Content related to the project dumper script.
        """

        params = (
            self.params.model_dump())

        return {
            'name': self.name,
            'params': params}

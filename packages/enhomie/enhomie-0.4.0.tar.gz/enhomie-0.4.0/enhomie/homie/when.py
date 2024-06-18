"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import TYPE_CHECKING

from ..builtins import chck_time_period
from ..builtins import when_time_period
from ..philipshue import chck_phue_change
from ..philipshue import chck_phue_scene
from ..philipshue import when_phue_change
from ..philipshue import when_phue_scene
from ..ubiquiti import chck_ubiq_client
from ..ubiquiti import when_ubiq_client

if TYPE_CHECKING:
    from .homie import Homie
    from .params import HomieWhenParams



class HomieWhen:
    """
    Determine when condition is true and provide information.

    :param homie: Primary class instance for Homie Automate.
    :param params: Parameters for the conditional operations.
    """

    __homie: 'Homie'
    __params: 'HomieWhenParams'


    def __init__(
        self,
        homie: 'Homie',
        params: 'HomieWhenParams',
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        self.__homie = homie
        self.__params = params

        self.__validate_params()


    def __validate_params(
        self,
    ) -> None:
        """
        Perform advanced validation on the parameters provided.
        """

        if self.params.time_period:
            chck_time_period(self)

        if self.params.phue_change:
            chck_phue_change(self)

        if self.params.phue_scene:
            chck_phue_scene(self)

        if self.params.ubiq_client:
            chck_ubiq_client(self)


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
    ) -> 'HomieWhenParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    @property
    def negate(
        self,
    ) -> bool:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.negate


    @property
    def family(
        self,
    ) -> str:
        """
        Return the value for the attribute from params instance.

        :returns: Value for the attribute from params instance.
        """

        return self.params.family


    @property
    def outcome(
        self,
    ) -> bool:
        """
        Return the boolean indicating whether condition matched.

        :returns: Boolean indicating whether condition matched.
        """

        matched: list[bool] = []

        if self.params.time_period:
            matched.append(
                when_time_period(self))

        if self.params.phue_change:
            matched.append(
                when_phue_change(self))

        if self.params.phue_scene:
            matched.append(
                when_phue_scene(self))

        if self.params.ubiq_client:
            matched.append(
                when_ubiq_client(self))

        outcome = bool(
            matched and all(matched))

        return (
            not outcome
            if self.negate is True
            else outcome)

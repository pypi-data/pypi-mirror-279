"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import TYPE_CHECKING

from ..philipshue import chck_phue_button
from ..philipshue import chck_phue_motion
from ..philipshue import what_phue_button
from ..philipshue import what_phue_motion

if TYPE_CHECKING:
    from .homie import Homie
    from .params import HomieWhatParams



class HomieWhat:
    """
    Determine when condition is true and provide information.

    :param homie: Primary class instance for Homie Automate.
    :param params: Parameters for the conditional operations.
    """

    __homie: 'Homie'
    __params: 'HomieWhatParams'


    def __init__(
        self,
        homie: 'Homie',
        params: 'HomieWhatParams',
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

        if self.params.phue_motion:
            chck_phue_motion(self)

        if self.params.phue_button:
            chck_phue_button(self)


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
    ) -> 'HomieWhatParams':
        """
        Return the Pydantic model containing the configuration.

        :returns: Pydantic model containing the configuration.
        """

        return self.__params


    def match(
        self,
        event: dict[str, Any],
    ) -> bool:
        """
        Return the boolean indicating whether condition matched.

        :param event: Event which was yielded from the stream.
        :returns: Boolean indicating whether condition matched.
        """

        matched: list[bool] = []

        if self.params.phue_motion:
            matched.append(
                what_phue_motion(self, event))

        if self.params.phue_button:
            matched.append(
                what_phue_button(self, event))

        outcome = bool(
            matched and any(matched))

        return outcome

"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from typing import Any
from typing import Optional

from encommon.times import Times

from pydantic import BaseModel



class WhenTimePeriodParams(BaseModel, extra='forbid'):
    """
    Process and validate the Homie configuration parameters.

    :param start: Determine the start for the desired period.
    :param stop: Determine the ending for the desired period.
    :param tzname: Name of the timezone associated to period.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    start: Optional[str] = None
    stop: Optional[str] = None
    tzname: str = 'UTC'


    def __init__(
        self,
        **data: Any,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        start = data.get('start')
        stop = data.get('stop')
        tzname = data.get('tzname')


        if start is not None:
            start = Times(
                source=start,
                tzname=tzname)

        if stop is not None:
            stop = Times(
                source=stop,
                tzname=tzname)


        if (start and stop
                and stop <= start):
            stop = stop.shift('+1d')


        if start is not None:
            data['start'] = start.simple

        if stop is not None:
            data['stop'] = stop.simple


        super().__init__(**data)

"""
Functions and routines associated with Enasis Network Homie Automate.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from contextlib import suppress
from typing import Any
from typing import Optional

from encommon.config import Config as _Config
from encommon.types import merge_dicts
from encommon.utils.common import PATHABLE

from .params import Params



class Config(_Config):
    """
    Contain the configurations from the arguments and files.

    :param files: Complete or relative path to config files.
    :param cargs: Configuration arguments in dictionary form,
        which will override contents from the config files.
    :param sargs: Additional arguments on the command line.
    """

    def __init__(
        self,
        files: Optional[PATHABLE] = None,
        cargs: Optional[dict[str, Any]] = None,
        sargs: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        super().__init__(
            files=files,
            cargs=cargs,
            sargs=sargs,
            model=Params)


    @property
    def params(
        self,
    ) -> Params:
        """
        Return the Pydantic model containing the configuration.

        .. warning::
           This method completely overrides the parent but is
           based on that code, would be unfortunate if upstream
           changes meant this breaks or breaks something else.

        :returns: Pydantic model containing the configuration.
        """

        params = self.__params

        if isinstance(params, Params):
            return params


        merged = self.files.merged

        merge_dicts(
            dict1=merged,
            dict2=self.cargs,
            force=True)


        update = False

        with suppress(AttributeError):

            _merged = self.paths.merged

            values = _merged.values()

            for merge in values:
                merge_dicts(merged, merge)

            update = True


        params = self.model(**merged)

        assert isinstance(params, Params)


        if update is True:
            self.__params = params

        return params

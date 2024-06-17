from abc import ABC, abstractmethod
from typing import Any, Optional, Callable

from .base_handler import BaseHandler


class Script(BaseHandler, ABC):
    """
    The abstract Script class serves as an interaction contract such that by extending it with its methods implemented,
        a script can be created that can be used in a generalized yet controlled setting.
    """

    @abstractmethod
    def get_scope_dependencies(self) -> list[dict[str, Any]]:
        """
        Fetch the scopes that the script will use and requires to be present in the dataset.

        NB: All required config is assumed to be present.

        :return: List of required scopes, where each is a dictionary containing either
            a 'representation' or a 'scope_id'.
        """
        raise NotImplementedError

    def handle(self, user_input: dict[Any: Any]) -> any:
        return self.execute('all', self._get_access_token, user_input)

    @abstractmethod
    def execute(
            self,
            business_cell_id: Optional[int],
            get_bearer_token: Callable[[], str],
            user_input: dict[Any: Any],
    ) -> Any:
        """
        Execute the script

        NB: All required config and scopes are assumed to be present.

        :param business_cell_id: Business cell to execute the script for, or None if running the script for all.
        :param get_bearer_token: Function that can be invoked to retrieve an access token.
        :param user_input: Dictionary of additional json-serializable input provided by the caller of the script.
        :return: Any json-serializable results the script outputs.
        """
        raise NotImplementedError

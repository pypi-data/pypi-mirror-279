from abc import ABC, abstractmethod
from typing import Any

from pricecypher.oidc import AccessTokenGenerator


class BaseHandler(ABC):
    """
    The abstract InferenceHandler class serves as an interaction contract such that by extending it with its
        methods implemented, a "real-time" (api) handler can be created that performs model inference for a dataset,
        which can then be used in a generalized yet controlled setting.
    """
    dataset_id: int
    settings: dict[str, Any]
    config: dict[str, dict[str, Any]]
    token_generator: AccessTokenGenerator

    def __init__(self, dataset_id: int, settings: dict[str, Any], config: dict[str, dict[str, Any]]):
        self.dataset_id = dataset_id
        self.settings = settings
        self.config = config

    def _get_access_token(self):
        return self.token_generator.generate()

    @abstractmethod
    def get_config_dependencies(self) -> dict[str, list[str]]:
        """
        Fetch the configuration sections and keys in the sections that the script will use that are not yet provided.

        NB: It is not needed to return all required sections and keys, only at least one that has not been provided yet.
        If all required config is provided, an empty dictionary is to be returned.

        :return: dictionary mapping from section key (string) to a (potentially empty) list of keys of that section
            that the script requires additionally.
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self, user_input: dict[Any: Any]) -> any:
        """
        TODO
        """
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Any

from pricecypher.enums import AccessTokenGrantType
from .base_handler import BaseHandler
from .dataclasses import PredictResult


class InferenceHandler(BaseHandler, ABC):
    """
    The abstract InferenceHandler class serves as an interaction contract such that by extending it with its
        methods implemented, a "real-time" (api) handler can be created that performs model inference for a dataset,
        which can then be used in a generalized yet controlled setting.
    """

    def set_access_token(self, access_token):
        self.token_generator = AccessTokenGrantType.STATIC.get_generator(access_token=access_token)

    @abstractmethod
    def handle(self, user_input: dict[Any: Any]) -> PredictResult:
        raise NotImplementedError

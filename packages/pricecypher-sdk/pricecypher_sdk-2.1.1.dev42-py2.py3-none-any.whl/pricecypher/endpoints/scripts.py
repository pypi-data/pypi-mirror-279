from typing import Optional

from pricecypher.models import Script, ScriptExecution
from .base_endpoint import BaseEndpoint


class ScriptsEndpoint(BaseEndpoint):
    """PriceCypher script service endpoints.

    :param RestClient client: HTTP client for making API requests.
    :param int dataset_id: Dataset ID.
    :param str scripts_base: (optional) Base URL of PriceCypher script service API.
        (defaults to https://scripts.pricecypher.com)
    """

    def __init__(self, client, dataset_id, scripts_base='https://scripts.pricecypher.com'):
        self.base_url = scripts_base
        self.client = client
        self.dataset_id = dataset_id
        self.param_keys = ['environment']

        self.base_url = self._url(['api/datasets', self.dataset_id, '/scripts'])

    def index(self, **kwargs) -> Optional[list[Script]]:
        """List all available scripts for the dataset.

        :return: list of scripts.
        :key environment: (Optional) environment of the underlying data intake to query. Defaults to latest intake.
        :rtype list[Script]
        """
        params = self._find_request_params(
            keys={'include_dependencies', 'type', 'env_status'},
            include_dependencies='false',
            **kwargs
        )
        return self.client.get(self._url(), params=params, schema=Script.Schema(many=True))

    def get(self, script_id):
        """
                Script endpoints for single script in script service API.
                :rtype: _ScriptEndpoint
                """
        return _ScriptEndpoint(self.client, self._url([script_id]))


class _ScriptEndpoint(BaseEndpoint):
    """
    PriceCypher script endpoints in script service API.
    """

    def __init__(self, client, base):
        self.client = client
        self.base_url = base

    def executions(self):
        """List all available config sections for the dataset.

        """
        return _ScriptExecutionsEndpoint(self.client, self._url(['executions']))


class _ScriptExecutionsEndpoint(BaseEndpoint):
    def __init__(self, client, base):
        self.client = client
        self.base_url = base
        self.param_keys = {'environment'}

    def latest_output(self, **kwargs) -> Optional[ScriptExecution]:
        params = self._find_request_params(**kwargs)
        return self.client.get(self._url(['latest/output']), params=params, schema=ScriptExecution.Schema(many=False))

from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper
from smartpm.logging_config import logger

class Uploads:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_schedule_uploads(self, project_id, scenario_id):
        """
        Gets the schedule upload data for a specific project and scenario: https://developers.smartpmtech.com/#operation/get-scenario-schedules

        Parameters
        ----------
        project_id : str
            The Project ID containing the scenario for which you would like to pull the delay table for
        scenario_id : str
            The Scenario ID for which you would like to pull the delay table for

        Returns
        -------
        <response.json> : dict
            Schedule upload data as a JSON object
        """
        logger.debug(f"Fetching delay table for project_id: {project_id}, scenario_id: {scenario_id}")

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/schedules'
        response = self.client._get(endpoint=endpoint)

        return response
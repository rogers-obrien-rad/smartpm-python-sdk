from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper, utility
from smartpm.visuals import plot_schedule_delay
from smartpm.logging_config import logger

class Delay:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_delay_table(self, project_id, scenario_id):
        """
        Get the delay table for a specific project and scenario: https://developers.smartpmtech.com/#operation/get-delay-table

        Parameters
        ----------
        project_id : str
            The Project ID containing the scenario for which you would like to pull the delay table for
        scenario_id : str
            The Scenario ID for which you would like to pull the delay table for

        Returns
        -------
        <response.json> : dict
            Delay table data as a JSON object
        """
        logger.debug(f"Fetching delay table for project_id: {project_id}, scenario_id: {scenario_id}")

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/delay'
        response = self.client._get(endpoint=endpoint)

        return response
    
    @utility
    def plot_delay(self, project_id, scenario_id):
        """
        Retrieve the delay data and plot it.
        Reproduces this figure from SmartPM: https://help.smartpmtech.com/trends-schedule-delay

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        """
        logger.debug(f"Plotting schedule delay for project_id: {project_id}, scenario_id: {scenario_id}")
        curve_data = self.get_delay_table(project_id, scenario_id)
        plot_schedule_delay(curve_data)
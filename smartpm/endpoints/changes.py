from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper, utility
from smartpm.utils import plot_schedule_changes
from smartpm.logging_config import logger

class Changes:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_changes_summary(self, project_id, scenario_id):
        """
        Retrieve summary information about the changes that have happened to a scenario over time: https://developers.smartpmtech.com/#operation/get-change-log-sumamry

        Parameters
        ----------
        project_id : str
            The Project ID containing the scenario for which you would like to pull the changes summary from
        scenario_id : str
            The Scenario ID for which you would like to pull the changes summary from
        Returns
        -------
        <response.json> : dict
            Changes summary data as a JSON object
        """
        logger.debug(f"Fetching changes summary for project_id: {project_id}, scenario_id: {scenario_id}")

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/change-log-summary'
        response = self.client._get(endpoint=endpoint)

        return response
    
    @utility
    def plot_changes_summary(self, project_id, scenario_id):
        """
        Retrieve the changes summary data and plot it.
        Reproduces this figure from SmartPM: https://help.smartpmtech.com/trends-schedule-changes-over-time

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        """
        logger.debug(f"Plotting changes summary for project_id: {project_id}, scenario_id: {scenario_id}")
        curve_data = self.get_changes_summary(project_id, scenario_id)
        plot_schedule_changes(curve_data)
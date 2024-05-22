from smartpm.client import SmartPMClient
from smartpm.utils import plot_percent_complete_curve, plot_earned_schedule_curve
from smartpm.decorators import api_wrapper, utility
from smartpm.logging_config import logger

class Activity:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_activities(self, project_id, scenario_id, data_date=None, filter_id=None):
        """
        Get activities for a specific scenario: https://developers.smartpmtech.com/#operation/get-activities

        Parameters
        ----------
        project_id : int
            ID of the project to retrieve scenarios for
        scenario_id : int
            ID of the scenario to retrieve details for
        data_date : str, default None
            Data date in format `yyyy-MM-dd` for which to retrieve the scenario details
            If None, will use the latest data date
        filter_id : int, default None
            ID for the filter that you want to filter the list of activities by
            If None, will include all

        Returns
        -------
        <response.json> : list of dict
            project scenarios as a JSON object
        """
        logger.debug(f"Fetching activities for project_id: {project_id} and scenario_id: {scenario_id}")
        params = {}
        if data_date:
            params['dataDate'] = data_date

        if filter_id:
            params['filterId'] = filter_id

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/activities'

        return self.client._get(endpoint=endpoint, params=params)
    
    @utility
    def count_activities_by_completion(self, project_id, scenario_id):
        """
        Count how many activities are complete and how many are not based on the percentComplete value.

        Parameters
        ----------
        project_id : int
            ID of the project to retrieve scenarios for
        scenario_id : int
            ID of the scenario to retrieve details for

        Returns
        -------
        dict
            Dictionary with counts of complete and incomplete activities.
        """
        activities = self.get_activities(project_id, scenario_id)
        
        complete_count = 0
        incomplete_count = 0

        for activity in activities:
            if activity.get('percentComplete', 0) == 100.0:
                complete_count += 1
            else:
                incomplete_count += 1

        return {
            'complete': complete_count,
            'incomplete': incomplete_count
        }
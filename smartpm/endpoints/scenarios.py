from smartpm.client import SmartPMClient
from smartpm.utils import plot_percent_complete_curve, plot_earned_schedule_curve
from smartpm.decorators import api_wrapper, utility
from smartpm.logging_config import logger

class Scenarios:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_scenarios(self, project_id, as_of=None):
        """
        Get scenarios for a specific project: https://developers.smartpmtech.com/#operation/get-scenarios

        Parameters
        ----------
        project_id : int
            ID of the project to retrieve scenarios for
        as_of : str, default None
            Return scenarios that have changed since date in format `2023-07-19T12:00:00`

        Returns
        -------
        <response.json> : list of dict
            project scenarios as a JSON object
        """
        logger.debug(f"Fetching scenarios for project_id: {project_id}, as_of: {as_of}")
        params = {}
        if as_of:
            params['asOf'] = as_of

        endpoint = f'v1/projects/{project_id}/scenarios'

        return self.client._get(endpoint=endpoint, params=params)

    @utility
    def find_scenario_by_name(self, project_id, scenario_name):
        """
        Find scenarios by their name for a specific project.

        Parameters
        ----------
        project_id : int
            ID of the project to retrieve scenarios for
        scenario_name : str
            The name of the scenario to find

        Returns
        -------
        matching_scenarios : list of dict
            List of scenarios matching the specified name
        """
        logger.debug(f"Searching for scenarios with name: {scenario_name} in project_id: {project_id}")
        scenarios = self.get_scenarios(project_id)
        
        matching_scenarios = [scenario for scenario in scenarios if scenario.get('name') == scenario_name]
        
        if matching_scenarios:
            logger.info(f"Found {len(matching_scenarios)} matching scenarios.")
        else:
            logger.info(f"No scenarios found with name '{scenario_name}'.")

        return matching_scenarios
    
    @api_wrapper
    def get_scenario_details(self, project_id, scenario_id, data_date=None):
        """
        Get the details for a specific scenario: https://developers.smartpmtech.com/#operation/get-scenario-details

        Parameters
        ----------
        project_id : int
            ID of the project containing the scenario
        scenario_id : int
            ID of the scenario to retrieve details for
        data_date : str, default None
            Data date in format `yyyy-MM-dd` for which to retrieve the scenario details
            If None, will use the latest data date

        Returns
        ------
        <response.json> : dict
            scenario details as a JSON object
        """
        logger.debug(f"Fetching scenario details for project_id: {project_id}, scenario_id: {scenario_id}, data_date: {data_date}")
        params = {}
        if data_date:
            params['dataDate'] = data_date

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}'
        return self.client._get(endpoint=endpoint, params=params)

    @api_wrapper
    def get_percent_complete_curve(self, project_id, scenario_id, delta=False):
        """
        Get Percent Complete Curve data for a specific scenario: https://developers.smartpmtech.com/#operation/get-percent-complete-curve

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        delta : bool, default False
            Return the change of progress between periods if True

        Returns
        -------
        <response.json> : dict
            percent complete curve data as a JSON object
        """
        logger.debug(f"Fetching percent complete curve data for project_id: {project_id}, scenario_id: {scenario_id}, delta: {delta}")
        params = {'delta': str(delta).lower()}

        endpoint = f'v2/projects/{project_id}/scenarios/{scenario_id}/percent-complete-curve'
        return self.client._get(endpoint=endpoint, params=params)

    @utility
    def plot_percent_complete_curve(self, project_id, scenario_id, delta=False):
        """
        Retrieve the percent complete curve and plot the progress.
        Reproduces this figure from SmartPM: https://help.smartpmtech.com/the-progress-curve

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        delta : bool, default False
            Return the change of progress between periods if True
        """
        logger.debug(f"Plotting scenario progress for project_id: {project_id}, scenario_id: {scenario_id}, delta: {delta}")
        curve_data = self.get_percent_complete_curve(project_id, scenario_id, delta)
        plot_percent_complete_curve(curve_data)

    @api_wrapper
    def get_earned_schedule_curve(self, project_id, scenario_id):
        """
        Get Earned Schedule Curve for a specific scenario.

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the earned schedule curve for

        Returns
        -------
        <response.json> : dict
            earned schedule curve data as a JSON object
        """
        logger.debug(f"Fetching earned schedule curve for project_id: {project_id}, scenario_id: {scenario_id}")
        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/earned-schedule-curve'
        response = self.client._get(endpoint=endpoint)
        
        return response
    
    @utility
    def plot_earned_schedule_curve(self, project_id, scenario_id):
        """
        Retrieve the earned days curve and plot the results
        Reproduces this figure: https://help.smartpmtech.com/earned-baseline-days

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        """
        logger.debug(f"Plotting earned schedule curve for project_id: {project_id}, scenario_id: {scenario_id}")
        earned_days_data = self.get_earned_schedule_curve(project_id, scenario_id)
        plot_earned_schedule_curve(earned_days_data)
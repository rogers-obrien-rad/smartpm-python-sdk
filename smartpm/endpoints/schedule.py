from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper, utility
from smartpm.logging_config import logger

class Schedule:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_schedule_quality(self, project_id, scenario_id, import_log_id=None, quality_profile_id=None):
        """
        Get the schedule quality for a specific project and scenario: https://developers.smartpmtech.com/#operation/get-schedule-quality

        Parameters
        ----------
        project_id : str
            The Project ID containing the scenario for which you would like to pull the schedule quality for
        scenario_id : str
            The Scenario ID for which you would like to pull the schedule quality for
        import_log_id : str, default None
            The schedule id for which you would like to see the schedule quality for, if not specified, the latest date will be used
        quality_profile_id : str, default None
            The quality profile you would like to use, if not specified the default profile for the project will be used

        Returns
        -------
        <response.json> : dict
            Schedule quality data as a JSON object
        """
        logger.debug(f"Fetching schedule quality for project_id: {project_id}, scenario_id: {scenario_id}, import_log_id: {import_log_id}, quality_profile_id: {quality_profile_id}")
        params = {}
        if import_log_id:
            params['importLogId'] = import_log_id
        if quality_profile_id:
            params['qualityProfileId'] = quality_profile_id

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/schedule-quality'
        response = self.client._get(endpoint=endpoint, params=params)

        return response
    
    @utility
    def get_metric_by_name(self, schedule_quality_data, metric_name):
        """
        Get a specific metric by its name from the schedule quality data.

        Parameters
        ----------
        schedule_quality_data : dict
            The schedule quality data as a JSON object
        metric_name : str
            The name of the metric to retrieve

        Returns
        -------
        metric : dict
            The metric data if found, otherwise None
        """
        metrics = schedule_quality_data.get('metrics', [])
        for metric in metrics:
            if metric.get('name') == metric_name:
                logger.debug(f"Found {metric_name}")
                return metric
            
        logger.warning(f"Could not find metric {metric_name}")
        return None

    @utility
    def get_schedule_grade(self, schedule_quality_data):
        """
        Get the overall grade from the schedule quality data.

        Parameters
        ----------
        schedule_quality_data : dict
            The schedule quality data as a JSON object

        Returns
        -------
        dict or None
            The grade data if found, otherwise None
        """
        return schedule_quality_data.get('grade')
    
    @api_wrapper
    def get_schedule_compression(self, project_id, scenario_id, data_date=None):
        """
        Get the schedule compression for a specific project and scenario: https://live.smartpmtech.com/public/v1/projects/{projectId}/scenarios/{scenarioId}/schedule-compression

        Parameters
        ----------
        project_id : str
            The Project ID containing the scenario for which you would like to pull the schedule compression for
        scenario_id : str
            The Scenario ID for which you would like to pull the schedule compression for
        data_date : str, optional
            The schedule data date you would like to retrieve schedule compression for

        Returns
        -------
        <response.json> : dict
            Schedule compression data as a JSON object
        """
        logger.debug(f"Fetching schedule compression for project_id: {project_id}, scenario_id: {scenario_id}, data_date: {data_date}")
        params = {}
        if data_date:
            params['dataDate'] = data_date

        endpoint = f'v1/projects/{project_id}/scenarios/{scenario_id}/schedule-compression'
        response = self.client._get(endpoint=endpoint, params=params)
        return response
    
    @api_wrapper
    def get_all_quality_profiles(self):
        """
        Get all quality profiles: https://developers.smartpmtech.com/#operation/get-schedule-quality (scroll down - no direct link)

        Returns
        -------
        <response.json> : list of dict
            quality profiles data as a JSON object
        """
        endpoint = 'v1/quality-profiles'
        return self.client._get(endpoint=endpoint)
    
    @api_wrapper
    def get_quality_profile(self, quality_profile_id):
        """
        Get a specific quality profile: https://developers.smartpmtech.com/#operation/get-quality-profile

        Parameters
        ----------
        quality_profile_id : str
            The quality profile you want to pull configuration for

        Returns
        -------
        <response.json> : dict
            Quality profile data as a JSON object
        """
        logger.debug(f"Fetching quality profile for quality_profile_id: {quality_profile_id}")
        endpoint = f'v1/quality-profiles/{quality_profile_id}'
        response = self.client._get(endpoint=endpoint)
        return response
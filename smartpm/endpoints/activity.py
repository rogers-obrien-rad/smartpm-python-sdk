import pandas as pd

from smartpm.client import SmartPMClient
from smartpm.visuals import plot_activity_distribution_by_month
from smartpm.decorators import api_wrapper, utility
from smartpm.logging_config import logger
from smartpm.endpoints.scenarios import Scenarios

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
    
    @utility
    def plot_activity_distribution(self, project_id, scenario_id):
        """
        Retrieve activities and plots distribution by month

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        """
        logger.debug(f"Plotting activity distribution for project_id: {project_id}, scenario_id: {scenario_id}")
        scenarios_api = Scenarios(client=self.client)
        scenario_details = scenarios_api.get_scenario_details(
            project_id=project_id,
            scenario_id=scenario_id
        )
        activity_data = self.get_activities(project_id, scenario_id)
        activity_dist = plot_activity_distribution_by_month(activity_data, scenario_details)
        return activity_dist
    
    @utility
    def get_activity_by_id(self, project_id, scenario_id, activity_id):
        """
        Get the data for a specific activity by its ID.

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the activity from
        activity_id : str
            ID of the activity to retrieve

        Returns
        -------
        dict
            Dictionary containing the activity data.
        """
        activity_data = self.get_activities(project_id, scenario_id)
        for entry in activity_data:
            if entry['activityId'] == activity_id:
                return entry
        return None  # Return None if the activity is not found
    
    @utility
    def get_baseline_activities_by_month(self, project_id, scenario_id, start, month, year):
        """
        Filter activities by baseline start or finish date for a given month and year.

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        start : bool
            If True, filter by baseline start date, otherwise filter by baseline finish date.
        month : int
            The month to filter by.
        year : int
            The year to filter by.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the filtered activities with the specified columns.
        """
        filtered_data = []

        activity_data = self.get_activities(project_id, scenario_id)
        for entry in activity_data:
            baseline_date_str = entry['baseline']['startDate'] if start else entry['baseline']['finishDate']
            baseline_date = pd.to_datetime(baseline_date_str)
            
            if baseline_date.month == month and baseline_date.year == year:
                filtered_data.append({
                    "activityId": entry['activityId'],
                    "name": entry['name'],
                    "baselineStartDate": entry['baseline']['startDate'],
                    "baselineFinishDate": entry['baseline']['finishDate'],
                    "baselineDuration": entry['baseline']['duration'],
                    "startDate": entry.get('startDate'),
                    "finishDate": entry.get('finishDate'),
                    "actualDuration": entry.get('actualDuration')
                })

        df = pd.DataFrame(filtered_data)

        return df
    
    @utility
    def get_current_activities_by_month(self, project_id, scenario_id, start, month, year):
        """
        Filter activities by current start or finish date for a given month and year.

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        start : bool
            If True, filter by baseline start date, otherwise filter by baseline finish date.
        month : int
            The month to filter by.
        year : int
            The year to filter by.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the filtered activities with the specified columns.
        """
        filtered_data = []

        activities_data = self.get_activities(project_id, scenario_id)
        for entry in activities_data:
            if start:
                activity_date = pd.to_datetime(entry['actualStartDate']) if pd.to_datetime(entry['actualStartDate']) else pd.to_datetime(entry['startDate'])
            else:
                activity_date = pd.to_datetime(entry['actualFinishDate']) if pd.to_datetime(entry['actualFinishDate']) else pd.to_datetime(entry['finishDate'])

            if activity_date is not None:
                if activity_date.month == month and activity_date.year == year:
                    filtered_data.append({
                        "activityId": entry['activityId'],
                        "name": entry['name'],
                        "baselineStartDate": entry['baseline']['startDate'],
                        "baselineFinishDate": entry['baseline']['finishDate'],
                        "baselineDuration": entry['baseline']['duration'],
                        "startDate": entry.get('startDate'),
                        "finishDate": entry.get('finishDate'),
                        "plannedDuration": entry.get('plannedDuration'),
                        "actualStartDate": entry.get('actualStartDate'),
                        "actualFinishDate": entry.get('actualFinishDate'),
                        "actualDuration": entry.get('actualDuration'),
                        "lateStartDate": entry.get('lateStartDate'),
                        "lateFinishDate": entry.get('lateFinishDate'),
                        "sourceStartDate": entry.get('sourceStartDate'),
                        "sourceFinishDate": entry.get('sourceFinishDate'),
                        "percentComplete": entry.get("percentComplete")
                    })

        df = pd.DataFrame(filtered_data)

        return df
    
    @utility
    def get_extreme_date(self, project_id, scenario_id, use_actual=True, find_latest=False):
        """
        Get the earliest or latest date from list of activities

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        use_actual : bool, default True
            If True, use 'actualStartDate', otherwise use 'startDate'.
        find_latest : bool, default False
            If True, find the latest date using finish dates. If False, find the earliest date using start dates.

        Returns
        -------
        extreme_date : str
            The earliest or latest date as a string.
        """
        activities = self.get_activities(project_id, scenario_id)

        if find_latest:
            date_key = 'actualFinishDate' if use_actual else 'finishDate'
        else:
            date_key = 'actualStartDate' if use_actual else 'startDate'
        
        dates = [entry[date_key] for entry in activities if entry[date_key] is not None]
        
        if find_latest:
            extreme_date = max(dates, key=lambda date: pd.to_datetime(date))
        else:
            extreme_date = min(dates, key=lambda date: pd.to_datetime(date))

        return extreme_date

    
    @utility
    def get_extreme_baseline_date(self, project_id, scenario_id, find_latest=False):
        """
        Get the earliest or latest baseline date from the provided JSON data.

        Parameters
        ----------
        project_id : str
            ID of the project containing the scenario
        scenario_id : str
            ID of the scenario to retrieve the percent complete curve for
        find_latest : bool, default False
            If True, find the latest date using finish dates. If False, find the earliest date using start dates.

        Returns
        -------
        str
            The earliest or latest baseline date as a string.
        """
        activities = self.get_activities(project_id, scenario_id)

        if find_latest:
            date_key = 'finishDate'
        else:
            date_key = 'startDate'
        
        dates = [entry['baseline'][date_key] for entry in activities if entry['baseline'][date_key] is not None]
        
        if find_latest:
            extreme_date = max(dates, key=lambda date: pd.to_datetime(date))
        else:
            extreme_date = min(dates, key=lambda date: pd.to_datetime(date))

        return extreme_date
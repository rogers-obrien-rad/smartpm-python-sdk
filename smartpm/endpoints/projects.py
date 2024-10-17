import pandas as pd

from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper, utility
from smartpm.logging_config import logger 


class Projects:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_projects(self, as_of=None):
        """
        Access basic project data: https://developers.smartpmtech.com/#operation/get-projects
        Note: the `filters` parameter is not implemented since it does not seem to work correctly and the filter options are limited

        Parameters
        ----------
        as_of : str
            specify date since projects have changed in format `2023-07-19T12:00:00`

        Returns
        -------
        <response.json> : list of dict
            projects data as a JSON object
        """
        logger.debug(f"Fetching projects as of: {as_of}")
        params = {}
        if as_of:
            params['asOf'] = as_of

        endpoint = 'v1/projects'
        response = self.client._get(endpoint=endpoint, params=params)
        return response

    @api_wrapper
    def get_active_projects(self, as_of=None):
        """
        Access basic project data: https://developers.smartpmtech.com/#operation/get-projects
        Note: the `filters` parameter is hard-coded since the provided filter options are needed.

        Parameters
        ----------
        as_of : str
            specify date since projects have changed in format `2023-07-19T12:00:00`

        Returns
        -------
        <response.json> : list of dict
            projects data as a JSON object
        """
        logger.debug(f"Fetching projects as of: {as_of}")
        
        # Hard-code project plan filters into the params
        # Inactive: 0b657f37-e317-4d65-9ebd-b4f6f0aae4b1
        filters = [
            'PROJECT_PLAN_ID:1164d4b6-9635-42ca-b004-37907055b285',
            'PROJECT_PLAN_ID:6698a06d-a690-4a8d-8bb9-07ebd96ba320',
            'PROJECT_PLAN_ID:9beb9b50-649b-48b1-a367-9b937c75cee3'
        ]
        
        # Construct the params dict
        params = {
            'filters': filters  # Passing the filters as a list
        }
        
        if as_of:
            params['asOf'] = as_of

        endpoint = 'v1/projects'
        response = self.client._get(endpoint=endpoint, params=params)
        
        return response


    @api_wrapper
    def get_project(self, project_id):
        """
        Get a specific project by its ID: https://developers.smartpmtech.com/#operation/get-project

        Parameters
        ----------
        project_id : str
            ID of the project to retrieve

        Returns
        -------
        <response.json> : dict
            project details as a JSON object
        """
        logger.debug(f"Fetching project with ID: {project_id}")
        endpoint = f'v1/projects/{project_id}'
        response = self.client._get(endpoint=endpoint)
        return response

    @api_wrapper
    def get_project_comments(self, project_id):
        """
        Get comments for a specific project: https://developers.smartpmtech.com/#operation/get-project-comments

        Parameters
        ----------
        project_id : int
            ID of the project to retrieve comments for

        Returns
        -------
        <response.json> : list of dict
            project comments as a JSON object
        """
        logger.debug(f"Fetching comments for project ID: {project_id}")
        endpoint = f'v1/projects/{project_id}/comments'
        response = self.client._get(endpoint=endpoint)
        return response
    
    @utility
    def find_project_by_name(self, name):
        """
        Find a project by its name.

        Parameters
        ----------
        name : str
            The name of the project to find

        Returns
        -------
        project : dict
            The project data if found, otherwise None
        """
        logger.debug(f"Searching for project with name: {name}")
        projects = self.get_projects()
        
        for project in projects:
            if project.get('name') == name:
                logger.info(f"Found project: {project['id']} - {project['name']}")
                return project
        
        logger.info(f"Project with name '{name}' not found.")
        return None
    
    @utility
    def get_projects_dataframe(self):
        """
        Get all projects and return as a DataFrame with selected columns.

        Returns
        -------
        pd.DataFrame
            DataFrame containing projects data with selected columns.
        """
        projects = self.get_projects()

        # Extract relevant fields and metadata
        project_data = []
        for project in projects:
            project_data.append({
                "id": project["id"],
                "name": project["name"],
                "startDate": project["startDate"],
                "city": project["city"],
                "projectNumber": project["metadata"].get("PROJECT_NUMBER"),
                "region": project["metadata"].get("REGION")
            })
        
        df = pd.DataFrame(project_data, columns=["id", "name", "startDate", "city", "projectNumber", "region"])
        return df
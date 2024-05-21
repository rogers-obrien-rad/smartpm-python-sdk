from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper
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

from smartpm.client import SmartPMClient

class Projects:
    def __init__(self, client: SmartPMClient):
        self.client = client

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
        params = {}
        if as_of:
            params['asOf'] = as_of

        return self.client._get(endpoint='projects', params=params)
    
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
        endpoint = f'projects/{project_id}'

        return self.client._get(endpoint)
    
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
        endpoint = f'projects/{project_id}/comments'

        return self.client._get(endpoint)
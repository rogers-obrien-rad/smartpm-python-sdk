from smartpm.client import SmartPMClient
from smartpm.decorators import api_wrapper
from smartpm.logging_config import logger

from datetime import datetime

class Models:
    def __init__(self, client: SmartPMClient):
        self.client = client

    @api_wrapper
    def get_models(self, project_id):
        """
        Gets all models for a project: https://developers.smartpmtech.com/#operation/get-public-v1-projects-projectId-models

        Parameters
        ----------
        project_id : str
            The Project ID containing the scenario for which you would like to pull the delay table for

        Returns
        -------
        response : list of dict
            model for a schedule
        """
        logger.debug(f"Fetching models for project_id: {project_id}")

        endpoint = f'v1/projects/{project_id}/models'
        response = self.client._get(endpoint=endpoint)

        return response
    
    @api_wrapper
    def find_baseline_model(self, project_id, find_original=True):
        """
        Gets the baseline models from a project.

        Parameters
        ----------
        project_id : int
            The Project ID containing the scenario for which you would like to pull the delay table for.
        find_original : bool, default True
            If True, find the original baseline model. If False, find the latest baseline model.

        Returns
        -------
        dict
            The baseline model for a schedule.
        """
        models = self.get_models(project_id=project_id)
        baseline_models = [model for model in models if model['projectId'] == project_id and model['modelType'] == 'BASELINE']

        if not baseline_models:
            return None  # Return None if no baseline models found

        if find_original:
            # Find the original baseline model (assuming there is only one original baseline)
            original_model = next((model for model in baseline_models if model['isOriginalModel']), None)

            return original_model
        else:
            # Find the latest baseline model without modifying the original data
            latest_model = max(baseline_models, key=lambda model: datetime.strptime(model['initialDataDate'], "%Y-%m-%dT%H:%M:%SZ"))

            return latest_model
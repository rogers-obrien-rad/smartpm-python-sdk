import os
import sys
import json

# Add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from smartpm.client import SmartPMClient
from smartpm.endpoints.projects import Projects # import projects to get project IDs
from smartpm.endpoints.models import Models

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

def main():
    # Setup SDK
    client = SmartPMClient(API_KEY, COMPANY_ID)
    projects_api = Projects(client)
    models_api = Models(client)

    # Get Models Data
    # ---------------
    # For all projects
    projects = projects_api.get_projects()
    '''
    for project in projects:
        project_id = project["id"]
        models = models_api.get_models(
            project_id=project_id
        )
        print(f"Models for project {project['name']}:")
        print(json.dumps(models, indent=4))
    '''
    # ---------------

    # Get Models Data for Specific Project
    # ------------------------------------
    # Find project by name
    name_to_find = "212096 - 401 FIRST STREET (College Station)" # replace with your project name
    project = projects_api.find_project_by_name(name=name_to_find)
    project_id = project["id"]

    print(f"Get Models data for {name_to_find}")
    models = models_api.get_models(
        project_id=project_id
    )
    print(json.dumps(models, indent=4))
    # ------------------------------------

    # Get Baseline Model for Specific Project
    # ---------------------------------------
    # Find project by name
    name_to_find = "231068 Databank DFW8 ACCEL RE-BL - CO PENDING" # replace with your project name
    project = projects_api.find_project_by_name(name=name_to_find)
    project_id = project["id"]

    print(f"Get Original Basline Model for {name_to_find}")
    model_baseline_original = models_api.find_baseline_model(
        project_id=project_id,
        find_original=True
    )
    print(json.dumps(model_baseline_original, indent=4))

    print(f"Get Latest Basline Model for {name_to_find}")
    model_baseline_latest = models_api.find_baseline_model(
        project_id=project_id,
        find_original=False
    )
    print(json.dumps(model_baseline_latest, indent=4))
    # ---------------------------------------
    
if __name__ == "__main__":
    main()

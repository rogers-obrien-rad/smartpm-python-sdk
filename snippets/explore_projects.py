import os
import sys
import json

# Add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from smartpm.client import SmartPMClient
from smartpm.endpoints.projects import Projects

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

def output_projects(project_list):
    """
    Outputs information on the list of projects in the format:

    Project Name (Project ID)
    City, State
    Region: Region
    Under Construction: Boolean

    Parameters
    ----------
    project_list : list of dict
        list of project data
    """
    for project in project_list:
        print(f"{project.get('name')} ({project.get('id')})")
        print(f"{project.get('city')}, {project.get('state')}")
        print(f"Region: {project.get('metadata', {}).get('REGION', '')}")
        print(f"Under Construction: {project.get('underConstruction')}")

def main():
    # Setup SDK
    client = SmartPMClient(API_KEY, COMPANY_ID)
    projects_api = Projects(client)

    # Get All Projects
    # ----------------
    print("Get All Projects")
    projects = projects_api.get_projects()

    # Show projects
    print("Number of Projects:", len(projects))
    output_projects(project_list=projects)
    # ----------------

    # Get Recently Updated Projects
    # -----------------------------
    print("\nGet Recently Updated Projects")
    projects_updated_2024 = projects_api.get_projects(as_of='2024-05-01T00:00:00') # Change date to your choosing

    # Show projects
    print("Number of Projects Updated in 2024:", len(projects_updated_2024))
    output_projects(project_list=projects_updated_2024)
    # -----------------------------

    # Get Specific Project
    # --------------------
    print("\nGet Specific Project")
    project_id = 47939
    project_details = projects_api.get_project(project_id=project_id)
    print(json.dumps(project_details, indent=4))

    # Get Project by Name
    name_to_find = "212096 - 401 FIRST STREET (College Station)" # replace with your project name
    project = projects_api.find_project_by_name(name=name_to_find)
    print(json.dumps(project, indent=4))
    # --------------------

    # Get Project Comments
    # --------------------
    print("\nGet Project Comments")
    for project in projects[:4]:
        try:
            project_comments = projects_api.get_project_comments(project_id=project["id"])
            print(project_comments)
        except Exception as e:
            continue

if __name__ == "__main__":
    main()

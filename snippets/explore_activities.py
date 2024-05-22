import os
import sys
import json

# Add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from smartpm.client import SmartPMClient
from smartpm.endpoints.projects import Projects # import projects to get project IDs
from smartpm.endpoints.scenarios import Scenarios
from smartpm.endpoints.activity import Activity

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

def main():
    # Setup SDK
    client = SmartPMClient(API_KEY, COMPANY_ID)
    projects_api = Projects(client) # see snippets/list_projects.py for more use
    scenarios_api = Scenarios(client)
    activity_api = Activity(client)

    # Get All Activities
    # -----------------
    # Find project by name
    name_to_find = "212096 - 401 FIRST STREET (College Station)" # replace with your project name
    project = projects_api.find_project_by_name(name=name_to_find)
    project_id = project["id"]

    # Find scenario by name
    scenario_to_find = "Full Schedule" # replace with your scenario name
    matching_scenarios = scenarios_api.find_scenario_by_name(
        project_id=project_id,
        scenario_name=scenario_to_find
    )
    scenario_id = matching_scenarios[-1].get("id")

    print("Get All Activities")
    activities = activity_api.get_activities(
        project_id=project_id,
        scenario_id=scenario_id
    )
    # print(json.dumps(activities, indent=4))
    print(f"Number of activities: {len(activities)}")
    print("Example activity:")
    print(json.dumps(activities[0], indent=4))
    # -----------------

    # Count Complete/Incomplete
    # -------------------------
    activity_counts = activity_api.count_activities_by_completion(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print(activity_counts)
    # -------------------------
    
if __name__ == "__main__":
    main()

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

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

def main():
    # Setup SDK
    client = SmartPMClient(API_KEY, COMPANY_ID)
    projects_api = Projects(client) # see snippets/list_projects.py for more use
    scenarios_api = Scenarios(client) # see snippets/list_scenarios.py for more use

    # Plot Planned vs Actual Percent Complete for Full Schedule
    # ---------------------------------------------------------
    # Find project by name
    name_to_find = "212096 - 401 FIRST STREET (College Station)" # replace with your project name
    projects = projects_api.get_projects()
    project_id = projects[0]["id"] # default to first project
    for project in projects:
        if project["name"] == name_to_find:
            print(f"Found Project: {project['id']} - {project['name']}")
            project_id = project["id"]
            break

    # Find scenario by name
    scenario_to_find = "Full Schedule" # replace with your scenario name
    scenarios = scenarios_api.get_scenarios(project_id=project_id)
    print(json.dumps(scenarios, indent=4))
    scenario_id = scenarios[0]["id"] # default to first scenario
    for scenario in scenarios:
        if scenario["name"] == scenario_to_find:
            print(f"Found Scenario:")
            print(json.dumps(scenario, indent=4))
            scenario_id = scenario["id"]
            # don't break since there are might be multiple matching scenarios and we want to get the latest

    # Check data
    complete_curve = scenarios_api.get_percent_complete_curve(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print(json.dumps(complete_curve["data"][0], indent=4))

    scenarios_api.plot_percent_complete_curve(
        project_id=project_id,
        scenario_id=scenario_id
    )

if __name__ == "__main__":
    main()
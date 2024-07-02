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
    scenarios_api = Scenarios(client)

    # Get All Scenarios
    # -----------------
    # Find project by name
    name_to_find = "212096 - 401 FIRST STREET (College Station)" # replace with your project name
    project = projects_api.find_project_by_name(name=name_to_find)
    project_id = project["id"]

    # Get scenarios by supplying the project ID from any project
    print(f"Get All Scenarios for project: {project_id}")
    scenarios = scenarios_api.get_scenarios(project_id=project_id)
    print("Scenarios:")
    print(json.dumps(scenarios, indent=4))
    # -----------------

    # View Scenario Details
    # ---------------------
    use_default = True
    if use_default:
        # Get default project scenario
        scenario_id = project['defaultScenarioId']
    else:
        # Get latest Full Schedule scenario
        scenario_to_find = "Full Schedule" # replace with your scenario name
        matching_scenarios = scenarios_api.find_scenario_by_name(
            project_id=project_id,
            scenario_name=scenario_to_find
        )
        scenario_id = matching_scenarios[-1].get("id")

    print(f"Getting scenario details for Scenario {scenario_id}")
    scenario_details = scenarios_api.get_scenario_details(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print("Last Scenario: Details")
    print(json.dumps(scenario_details, indent=4))
    # ---------------------

    # Get Percent Complete Curve
    # --------------------------
    data = scenarios_api.get_percent_complete_curve(
        project_id=project_id,
        scenario_id=scenario_id,
        delta=False
    )
    print("Percent Complete Types:")
    print(data["percentCompleteTypes"])
    print(f"Number of datapoints: {len(data['data'])}")
    print("Example data entry:")
    print(json.dumps(data["data"][0], indent=4))
    with open("reference/get_percent_complete_curve.json", 'w') as file:
        json.dump(data, file, indent=4)
    # Plot the curves
    scenarios_api.plot_percent_complete_curve(
        project_id=project_id,
        scenario_id=scenario_id
    )
    # --------------------------

    # Get Earned Schedule
    # -------------------
    earned_schedule_data = scenarios_api.get_earned_schedule_curve(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print("Example data entry:")
    print(json.dumps(earned_schedule_data["data"][0], indent=4))
    # Plot the curves
    scenarios_api.plot_earned_schedule_curve(
        project_id=project_id,
        scenario_id=scenario_id
    )
    # -------------------

if __name__ == "__main__":
    main()

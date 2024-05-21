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
    project_idx = 0 # change to explore explore different projects
    # Start by getting projects
    print("Get All Projects")
    projects = projects_api.get_projects()

    # Get scenarios by supplying the project ID from any project, in this case the first project in the list
    project_id = projects[project_idx]['id']
    print(f"Get All Scenarios for project: {project_id}")
    scenarios = scenarios_api.get_scenarios(project_id=project_id)
    print("Last Scenario: Summary")
    print(json.dumps(scenarios[-1], indent=4)) # view the first scenario
    # -----------------

    # View Scenario Details
    # ---------------------
    # Get latest scenario for "Full Schedule"
    scenario_id = scenarios[0]["id"] # default to the first scenario in the list
    for scenario in scenarios:
        if scenario["name"] == "Full Schedule":
            scenario_id = scenario["id"]
            print("Scenario Summay: 'Full Schedule'")
            print(json.dumps(scenario, indent=4))

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

if __name__ == "__main__":
    main()

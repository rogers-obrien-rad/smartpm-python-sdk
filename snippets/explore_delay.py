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
from smartpm.endpoints.delay import Delay

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

def main():
    # Setup SDK
    client = SmartPMClient(API_KEY, COMPANY_ID)
    projects_api = Projects(client)
    scenarios_api = Scenarios(client)
    delay_api = Delay(client)

    # Get Delay Table
    # ---------------
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

    print("Get Delay Table")
    delay_table = delay_api.get_delay_table(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print("Example delay entry:")
    print(json.dumps(delay_table[2], indent=4))
    # ---------------

    # Plot Delay
    # ----------
    delay_api.plot_delay(
        project_id=project_id,
        scenario_id=scenario_id
    )
    # ----------
    
if __name__ == "__main__":
    main()

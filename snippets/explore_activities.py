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
    print("Example activities:")
    print(json.dumps(activities[-2:], indent=4))
    # -----------------

    # Count Complete/Incomplete
    # -------------------------
    activity_counts = activity_api.count_activities_by_completion(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print(activity_counts)
    # -------------------------
    
    # Get Activity by Activity ID
    # ---------------------------
    activity_id = "N.SKIN2010"
    activity_by_id = activity_api.get_activity_by_id(
        project_id=project_id,
        scenario_id=scenario_id,
        activity_id=activity_id
    )
    print(f"Details for Activity {activity_id}")
    print(json.dumps(activity_by_id,indent=4))
    # ---------------------------

    # Get Baseline Data
    # -----------------
    baseline_mo=10
    baseline_y=2023
    baseline_activity_data_by_month = activity_api.get_baseline_activities_by_month(
        project_id=project_id,
        scenario_id=scenario_id,
        start=True,
        month=baseline_mo,
        year=baseline_y
    )
    baseline_activity_data_by_month.to_csv(f"reference/baseline_activities_{project_id}_{scenario_id}_{baseline_y}-{baseline_mo}.csv")
    # -----------------

    # Get Current Data
    # ----------------
    current_mo=5
    baseline_y=2024
    current_activity_data_by_month = activity_api.get_current_activities_by_month(
        project_id=project_id,
        scenario_id=scenario_id,
        start=True,
        month=current_mo,
        year=baseline_y
    )
    current_activity_data_by_month.to_csv(f"reference/current_activities_{project_id}_{scenario_id}_{baseline_y}-{current_mo}.csv")
    # ----------------

    # Plot Activity Distribution
    # --------------------------
    activity_dist = activity_api.plot_activity_distribution(
        project_id=project_id,
        scenario_id=scenario_id
    )
    activity_dist.to_csv(f"reference/activity_distribution_{project_id}_{scenario_id}.csv")
    # --------------------------

    # Get Start Dates
    # ---------------
    easliest_normal = activity_api.get_earliest_date(
        project_id=project_id,
        scenario_id=scenario_id,
        use_actual=False
    )
    earliest_actual = activity_api.get_earliest_date(
        project_id=project_id,
        scenario_id=scenario_id,
        use_actual=True
    )
    earliest_baseline = activity_api.get_earliest_baseline_start_date(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print("Earliest Normal Start Date:", easliest_normal)
    print("Earliest Actual Start Date:", earliest_actual)
    print("Earliest Baseline Start Date:", earliest_baseline)
    
if __name__ == "__main__":
    main()

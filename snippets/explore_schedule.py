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
from smartpm.endpoints.schedule import Schedule

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

def main():
    # Setup SDK
    client = SmartPMClient(API_KEY, COMPANY_ID)
    projects_api = Projects(client)
    scenarios_api = Scenarios(client)
    schedule_api = Schedule(client)

    # Get Schedule Quality - Example 1
    # --------------------------------
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

    print("Get Schedule Quality")
    schedule_quality_data = schedule_api.get_schedule_quality(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print(json.dumps(schedule_quality_data, indent=4))
    # --------------------

    # Get Schedule Quality - Example 2
    # --------------------------------
    # Find project by id
    project_id = 47939
    project = projects_api.get_project(project_id=project_id)
    project_id = project["id"]
    scenario_id = project["defaultScenarioId"]

    print("Get Schedule Quality")
    schedule_quality_data = schedule_api.get_schedule_quality(
        project_id=project_id,
        scenario_id=scenario_id
    )
    #with open(f"./schedule-quality-{project_id}-{scenario_id}.json", "w") as f:
    #    json.dump(schedule_quality_data, f, indent=4)
    # --------------------

    # Get Schedule Quality Metrics
    # ----------------------------
    print("Get Schedule Grade")
    grade_data = schedule_api.get_schedule_grade(schedule_quality_data=schedule_quality_data)
    print(f"Grade is {grade_data.get('mark')} ({round(grade_data.get('score'), 1)}%) - {grade_data.get('indicator')}")

    print("Get Schedule Metrics")
    print("Critical Path Percent")
    critical_path_data = schedule_api.get_metric_by_name(
        schedule_quality_data=schedule_quality_data,
        metric_name="CRITICAL_PATH_PERCENT"
    )
    print(json.dumps(critical_path_data, indent=4))
    print("Finish to Start")
    finish_to_start_data = schedule_api.get_metric_by_name(
        schedule_quality_data=schedule_quality_data,
        metric_name="RELATIONSHIPS_FINISH_TO_START"
    )
    print(json.dumps(finish_to_start_data, indent=4))
    # ----------------------------

    # Get Schedule Compression
    # ------------------------
    print("Get Schedule Compression")
    schedule_compression_data = schedule_api.get_schedule_compression(
        project_id=project_id,
        scenario_id=scenario_id
    )
    print(json.dumps(schedule_compression_data, indent=4))
    # ------------------------
    
if __name__ == "__main__":
    main()

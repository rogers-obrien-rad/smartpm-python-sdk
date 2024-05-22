import pytest
import os
import sys
import logging
import json

# Add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from smartpm.client import SmartPMClient
from smartpm.endpoints.scenarios import Scenarios
from smartpm.endpoints.projects import Projects
from smartpm.endpoints.activity import Activity

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    return SmartPMClient(API_KEY, COMPANY_ID)

@pytest.fixture
def activity(client):
    return Activity(client)

@pytest.fixture
def scenarios(client):
    return Scenarios(client)

@pytest.fixture
def projects(client):
    return Projects(client)

def test_get_activities(activity, scenarios, projects):
    """Test retrieving activities for a specific scenario by its ID."""
    # Get a list of projects to use a valid project ID
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    # Retrieve scenarios for the first project
    all_scenarios = scenarios.get_scenarios(project_id)
    logger.info("Project ID: %s", project_id)
    
    assert isinstance(all_scenarios, list)
    assert len(all_scenarios) > 0
    
    first_scenario = all_scenarios[0]
    scenario_id = first_scenario['id']
    
    # Retrieve activities for the first scenario
    activities = activity.get_activities(project_id, scenario_id)
    logger.info("Scenario ID: %s", scenario_id)
    
    # Pretty-print the activities
    pretty_activities = json.dumps(activities, indent=4)
    logger.info("Activities: %s", pretty_activities)
    
    assert isinstance(activities, list)

def test_count_activities_by_completion(activity, scenarios, projects):
    """Test counting complete and incomplete activities for a specific scenario by its ID."""
    # Get a list of projects to use a valid project ID
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    # Retrieve scenarios for the first project
    all_scenarios = scenarios.get_scenarios(project_id)
    logger.info("Project ID: %s", project_id)
    
    assert isinstance(all_scenarios, list)
    assert len(all_scenarios) > 0
    
    first_scenario = all_scenarios[0]
    scenario_id = first_scenario['id']
    
    # Count complete and incomplete activities for the first scenario
    completion_counts = activity.count_activities_by_completion(project_id, scenario_id)
    logger.info("Scenario ID: %s", scenario_id)
    logger.info("Completion Counts: %s", completion_counts)
    
    assert isinstance(completion_counts, dict)
    assert 'complete' in completion_counts
    assert 'incomplete' in completion_counts
    assert isinstance(completion_counts['complete'], int)
    assert isinstance(completion_counts['incomplete'], int)
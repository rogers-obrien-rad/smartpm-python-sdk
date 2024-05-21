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

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    return SmartPMClient(API_KEY, COMPANY_ID)

@pytest.fixture
def scenarios(client):
    return Scenarios(client)

@pytest.fixture
def projects(client):
    return Projects(client)

def test_get_scenarios(scenarios, projects):
    """Test retrieving scenarios for a specific project by its ID."""
    # Get a list of projects to use a valid project ID
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    # Retrieve scenarios for the first project
    project_scenarios = scenarios.get_scenarios(project_id)
    logger.info("Project ID: %s", project_id)
    
    # Pretty-print the project scenarios
    pretty_scenarios = json.dumps(project_scenarios, indent=4)
    logger.info("Project Scenarios: %s", pretty_scenarios)
    
    assert isinstance(project_scenarios, list)

def test_get_scenario_details(scenarios, projects):
    """Test retrieving details for a specific scenario by its ID."""
    # Get a list of projects to use a valid project ID
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    # Retrieve scenarios for the first project
    project_scenarios = scenarios.get_scenarios(project_id)
    logger.info("Project ID: %s", project_id)
    
    assert isinstance(project_scenarios, list)
    assert len(project_scenarios) > 0
    
    first_scenario = project_scenarios[0]
    scenario_id = first_scenario['id']
    
    # Retrieve scenario details for the first scenario
    scenario_details = scenarios.get_scenario_details(project_id, scenario_id)
    logger.info("Scenario ID: %s", scenario_id)
    
    # Pretty-print the scenario details
    pretty_details = json.dumps(scenario_details, indent=4)
    logger.info("Scenario Details: %s", pretty_details)
    
    assert isinstance(scenario_details, dict)

def test_get_percent_complete_curve(scenarios, projects):
    """Test retrieving percent complete curve for a specific scenario by its ID."""
    # Get a list of projects to use a valid project ID
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    # Retrieve scenarios for the first project
    project_scenarios = scenarios.get_scenarios(project_id)
    logger.info("Project ID: %s", project_id)
    
    assert isinstance(project_scenarios, list)
    assert len(project_scenarios) > 0
    
    first_scenario = project_scenarios[0]
    scenario_id = first_scenario['id']
    
    # Retrieve percent complete curve for the first scenario
    percent_complete_curve = scenarios.get_percent_complete_curve(project_id, scenario_id)
    logger.info("Scenario ID: %s", scenario_id)
    
    # Pretty-print the percent complete curve
    pretty_curve = json.dumps(percent_complete_curve, indent=4)
    logger.info("Percent Complete Curve: %s", pretty_curve)
    
    assert isinstance(percent_complete_curve, dict)

def test_get_earned_schedule_curve(scenarios, projects):
    """Test retrieving earned schedule curve for a specific scenario by its ID."""
    # Get a list of projects to use a valid project ID
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    # Retrieve scenarios for the first project
    project_scenarios = scenarios.get_scenarios(project_id)
    logger.info("Project ID: %s", project_id)
    
    assert isinstance(project_scenarios, list)
    assert len(project_scenarios) > 0
    
    first_scenario = project_scenarios[0]
    scenario_id = first_scenario['id']
    
    # Retrieve earned schedule curve for the first scenario
    earned_schedule_curve = scenarios.get_earned_schedule_curve(project_id, scenario_id)
    logger.info("Scenario ID: %s", scenario_id)
    
    # Pretty-print the earned schedule curve
    pretty_curve = json.dumps(earned_schedule_curve, indent=4)
    logger.info("Earned Schedule Curve: %s", pretty_curve)
    
    assert isinstance(earned_schedule_curve, dict)
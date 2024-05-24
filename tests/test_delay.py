import pytest
import os
import sys
import logging

# Add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from smartpm.client import SmartPMClient
from smartpm.endpoints.projects import Projects
from smartpm.endpoints.scenarios import Scenarios
from smartpm.endpoints.delay import Delay

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    return SmartPMClient(API_KEY, COMPANY_ID)

@pytest.fixture
def delay(client):
    return Delay(client)

@pytest.fixture
def scenarios(client):
    return Scenarios(client)

@pytest.fixture
def projects(client):
    return Projects(client)

def test_get_delay_table(delay, scenarios, projects):
    """Test retrieving the delay table for a specific project and scenario."""
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

    result = delay.get_delay_table(project_id, scenario_id)
    logger.info("Delay table for project_id: %s, scenario_id: %s: %s", project_id, scenario_id, result)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    first_entry = result[0]
    assert 'period' in first_entry
    assert 'scheduleName' in first_entry
    assert 'dataDate' in first_entry
    assert 'endDate' in first_entry
    assert 'endDateVariance' in first_entry
    assert 'criticalPathDelay' in first_entry

def test_delay_table_content(delay, scenarios, projects):
    """Test the content of the delay table entries."""
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
    result = delay.get_delay_table(project_id, scenario_id)
    logger.info("Delay table for project_id: %s, scenario_id: %s: %s", project_id, scenario_id, result)
    
    first_entry = result[0]
    
    assert isinstance(first_entry['period'], int)
    assert isinstance(first_entry['scheduleName'], str)
    assert isinstance(first_entry['dataDate'], str)
    assert isinstance(first_entry['endDate'], str)
    assert isinstance(first_entry['endDateVariance'], dict)
    assert isinstance(first_entry['criticalPathDelay'], dict)
    
    assert 'period' in first_entry['endDateVariance']
    assert 'cumulative' in first_entry['endDateVariance']
    assert 'period' in first_entry['criticalPathDelay']
    assert 'cumulative' in first_entry['criticalPathDelay']
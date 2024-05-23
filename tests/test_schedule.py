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
from smartpm.endpoints.projects import Projects
from smartpm.endpoints.scenarios import Scenarios
from smartpm.endpoints.schedule import Schedule

API_KEY = os.getenv("API_KEY")
COMPANY_ID = os.getenv("COMPANY_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    return SmartPMClient(API_KEY, COMPANY_ID)

@pytest.fixture
def schedule(client):
    return Schedule(client)

@pytest.fixture
def scenarios(client):
    return Scenarios(client)

@pytest.fixture
def projects(client):
    return Projects(client)

def test_get_schedule_quality(schedule, scenarios, projects):
    """Test retrieving schedule quality for a specific project and scenario."""
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

    result = schedule.get_schedule_quality(project_id, scenario_id)
    logger.info("Schedule Quality: %s", json.dumps(result, indent=4))
    
    assert isinstance(result, dict)
    assert 'metrics' in result
    assert 'grade' in result

def test_get_metric_by_name(schedule, scenarios, projects):
    """Test retrieving a specific metric by name from the schedule quality data."""
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
    metric_name = "RELATIONSHIPS_FINISH_TO_FINISH"
    
    schedule_quality_data = schedule.get_schedule_quality(project_id, scenario_id)
    metric = schedule.get_metric_by_name(schedule_quality_data, metric_name)
    
    logger.info("Metric: %s", json.dumps(metric, indent=4))
    
    assert isinstance(metric, dict)
    assert metric['name'] == metric_name

def test_get_schedule_grade(schedule, scenarios, projects):
    """Test retrieving the overall grade from the schedule quality data."""
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
    
    schedule_quality_data = schedule.get_schedule_quality(project_id, scenario_id)
    grade = schedule.get_schedule_grade(schedule_quality_data)
    
    logger.info("Grade: %s", json.dumps(grade, indent=4))
    
    assert isinstance(grade, dict)
    assert 'mark' in grade
    assert 'indicator' in grade

def test_get_schedule_compression(schedule, scenarios, projects):
    """Test retrieving schedule compression for a specific project and scenario."""
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
    result = schedule.get_schedule_compression(project_id, scenario_id)
    logger.info("Schedule Compression: %s", json.dumps(result, indent=4))
    
    assert isinstance(result, dict)
    assert 'dataDate' in result
    assert 'scheduleCompression' in result
    assert 'scheduleCompressionIndex' in result

import pytest
import os
import sys
import logging
from smartpm.exceptions import NoCommentsFoundError

# Add the package root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from smartpm.client import SmartPMClient
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
def projects(client):
    return Projects(client)

def test_get_projects(projects):
    """Test retrieving all projects without filters."""
    result = projects.get_projects()
    logger.info("Number of projects (unfiltered): %d", len(result))
    
    assert isinstance(result, list)
    assert len(result) > 0

def test_get_projects_filters(projects):
    """Test retrieving projects with a filter based on the as_of date."""
    as_of = '2023-01-01T12:00:00'
    result = projects.get_projects(as_of=as_of)
    logger.info("Number of projects (filtered): %d", len(result))
    
    assert isinstance(result, list)
    assert len(result) > 0

def test_get_project(projects):
    """Test retrieving a specific project by its ID."""
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    project_details = projects.get_project(project_id)
    logger.info("Project ID: %s", project_id)
    logger.info("Project Details: %s", project_details)
    
    assert 'id' in project_details
    assert project_details['id'] == project_id

def test_get_project_comments(projects):
    """Test retrieving comments for a specific project by its ID."""
    all_projects = projects.get_projects()
    logger.info("Number of projects: %d", len(all_projects))
    
    assert isinstance(all_projects, list)
    assert len(all_projects) > 0
    
    first_project = all_projects[0]
    project_id = first_project['id']
    
    try:
        project_comments = projects.get_project_comments(project_id)
        logger.info("Project ID: %s", project_id)
        logger.info("Project Comments: %s", project_comments)
        
        assert isinstance(project_comments, list)
    except NoCommentsFoundError as e:
        logger.info(e)
        assert str(e) == "No comments found for this project."

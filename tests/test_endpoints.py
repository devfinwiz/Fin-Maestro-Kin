# tests/test_endpoints.py
import pytest
import requests
from constants import ENDPOINTS

@pytest.fixture
def api_url():
    return "http://localhost:8000"  

@pytest.mark.parametrize("endpoint", ENDPOINTS)  
def test_endpoints(api_url, endpoint):
    response = requests.get(f"{api_url}{endpoint}")
    assert response.status_code == 200



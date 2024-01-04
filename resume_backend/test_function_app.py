import pytest
from function_app import http_trigger  # import your function
from azure.functions import HttpRequest

def test_http_trigger():
    # Setup
    req = HttpRequest(method='GET', url='http://localhost:7071/api/HttpTrigger', params={})
    
    # Exercise
    resp = http_trigger(req)

    # Verify
    assert resp.status_code == 200  # check if status code is 200

    # Cleanup - none necessary for this simple test

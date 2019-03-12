import pytest
import json


@pytest.mark.parametrize('path', (
    '/api',
))
def test_api_path(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/api/'


valid_request_data_single = {
    "attribute": "Total_Revenue",
    "count": 2,
    "id": 10000000,
    "year_range": {
        "end": 2016,
        "start": 1977
    }
}


@pytest.mark.parametrize('path', (
    '/api/similarstate/single',
))
def test_api_path(client, path):
    response = client.post(path, json=valid_request_data_single)
    assert response.data == b'[{"state_name": "KENTUCKY", "state_id": 180000000}, {"state_name": "CONNECTICUT", "state_id": 70000000}]\n'


valid_request_data_multi = {
    "attribute": [
        "Total_Revenue",
        "Total_Taxes"
    ],
    "count": 2,
    "id": 10000000,
    "year": 1997
}


@pytest.mark.parametrize('path', (
    '/api/similarstate/multi',
))
def test_api_path(client, path):
    response = client.post(path, json=valid_request_data_multi)
    assert response.data == b'[{"state_name": "SOUTH CAROLINA", "state_id": 410000000}, {"state_name": "OREGON", "state_id": 380000000}]\n'


@pytest.mark.parametrize('path', (
    '/api/similarstate/supported',
))
def test_api_path(client, path):
    response = json.loads(client.get(path).get_data(as_text=True))
    assert len(response['supported_attributes']) == 107

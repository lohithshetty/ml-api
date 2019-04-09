import pytest
import json

@pytest.mark.parametrize('path', (
    '/api',
))
def test_api_path(client, path):
    response = client.get(path)
    assert response.headers['Location'] == 'http://localhost/api/'

valid_request_data_single = {
    "attribute":1,
    "count": 2,
    "place_type":0,
    "normalize_by":1,
    "id": 10000000,
    "year_range": {
        "end": 2016,
        "start": 1977
    }
}


@pytest.mark.parametrize('path', (
    '/api/similar/single',
))
def test_similar_single(client, path):
    response = client.post(path, json=valid_request_data_single)
    assert response.data == b'[{"place_id": 20000000}]\n','[{"state_nam...: 70000000}]\n'


valid_request_data_multi = {
    "attribute": [
        1
    ],
    "count": 2,
    "id": 140000000,
    "place_type":0,
    "normalize_by":1,
    "year": 2000
}


@pytest.mark.parametrize('path', (
    '/api/similar/multi',
))
def test_similar_multi(client, path):
    response = client.post(path, json=valid_request_data_multi)
    assert response.data == b'[]\n'


@pytest.mark.parametrize('path', (
    '/api/similar/supported',
))
def test_supported_common(client, path):
    response = json.loads(client.get(path).get_data(as_text=True))
    assert len(response) == 80

@pytest.mark.parametrize('path', (
    '/api/similar/supported/0',
))
def test_supported_state(client, path):
    response = json.loads(client.get(path).get_data(as_text=True))
    assert len(response) == 327

@pytest.mark.parametrize('path', (
    '/api/similar/supported/1',
))
def test_supported_county(client, path):
    response = json.loads(client.get(path).get_data(as_text=True))
    assert len(response) == 120

@pytest.mark.parametrize('path', (
    '/api/similar/supported/2',
))
def test_supported_city(client, path):
    response = json.loads(client.get(path).get_data(as_text=True))
    assert len(response) == 105

# Negative test cases
@pytest.mark.parametrize('path', (
    '/api/similar/supported/100',
))
def test_supported_invalid(client, path):
    response = client.get(path)
    assert response.status_code == 400


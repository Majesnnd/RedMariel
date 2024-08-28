import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert b"Buy groceries" in response.data

def test_get_task(client):
    response = client.get('/tasks/1')
    assert response.status_code == 200
    assert b"Buy groceries" in response.data

def test_create_task(client):
    response = client.post('/tasks', json={"title": "New task"})
    assert response.status_code == 201
    assert b"New task" in response.data

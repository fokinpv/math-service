# pylint: disable=redefined-outer-name
import pytest
from starlette.testclient import TestClient

from app import config, main, solver


@pytest.fixture
def app():
    app_ = main.create_app()
    app_.solver = solver.Solver(
        max_workers=config.MAX_WORKERS,
        timeout=config.WORKER_TASK_TIMEOUT
    )
    return app_


@pytest.fixture
def client(app):
    return TestClient(app)


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_validation_error(client):
    resp = client.post('/api/factorial', json={'n': -1})
    assert resp.status_code == 422


def test_factorial(client):
    resp = client.post('/api/factorial', json={'n': 3})
    assert resp.status_code == 200

    payload = resp.json()
    assert payload['answer'] == 6


def test_fibonacci(client):
    resp = client.post('/api/fibonacci', json={'n': 3})
    assert resp.status_code == 200

    payload = resp.json()
    assert payload['answer'] == 3


def test_ackermann(client):
    resp = client.post('/api/ackermann', json={'m': 2, 'n': 1})
    assert resp.status_code == 200

    payload = resp.json()
    assert payload['answer'] == 5


def test_timeout(client):
    resp = client.post('/api/ackermann?timeout=0.01', json={'m': 3, 'n': 2})
    assert resp.status_code == 404

    payload = resp.json()
    assert payload['detail'] == 'TimeoutError'

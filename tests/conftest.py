import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities_module)
    yield
    activities_module.clear()
    activities_module.update(original)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

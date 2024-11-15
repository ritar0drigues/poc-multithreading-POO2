import pytest
from server import Server

@pytest.fixture
def server():
    return Server()
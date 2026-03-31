import pytest
from app import server as flask_app

# A fixture allows you to initialize and reuse the code across multiple tests
# A client fixture that can b eused across multiple tests to mimic an API 
# consumer(someone sending requests to your API/app server)
@pytest.fixture
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client

import pytest

from vizapp import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_object='vizapp.config.TestConfig', config_filename="test-config.cfg")
    with flask_app.test_client() as client:
        yield client

import pytest

from app import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()    # TODO - pass here debug configuration?
    with flask_app.test_client() as client:
        yield client

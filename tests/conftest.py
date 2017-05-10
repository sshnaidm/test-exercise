import os
import pytest
import sys
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from testex.app import app


@pytest.fixture
def client(request):
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    def teardown():
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])
    request.addfinalizer(teardown)
    return client

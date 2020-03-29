import pytest

from rest_api.database.models import Author, Book
from rest_api.app import app

routes_test_data = [
    ('/api/', 200),
    ('/non_exist_link', 404)
]


@pytest.mark.parametrize('url,expected_status_code', routes_test_data)
def test_routes(url, expected_status_code):
    c = app.test_client()
    print(dir(c))
    response = c.get(app.config["SERVER_NAME"]+url)
    assert response.status_code == expected_status_code

from fastapi.testclient import TestClient

from app.tests.conftest import test_app


class TestAppBasics:

    def test_read_openapi(self, test_app):
        """
        Swagger OpenAPI UI is available
        """
        response = test_app.get("/docs")
        assert response.status_code == 200
        assert '<title>{{ cookiecutter.project_name }} - Swagger UI</title>' in response.text
        assert '<!-- `SwaggerUIBundle` is now available on the page -->' in response.text

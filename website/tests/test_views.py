import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestStaticPages:
    def test_landing_page(self, client):
        url = reverse("website:landing_page")
        response = client.get(url)
        assert response.status_code == 200, "Should load the page."

from django.test import Client
from django.urls import reverse


class TestHomeView:
    client = Client()

    def test_home_connection(self) -> None:
        expected = 200
        response = self.client.get(reverse("home"))
        assert response.status_code == expected

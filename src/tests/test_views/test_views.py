import pytest
from django.test import Client
from django.urls import reverse

from streaming_app import models, views


class TestHomeView:
    client = Client()

    def test_home_connection(self) -> None:
        # Arrange
        expected = 200
        # Act
        response = self.client.get(reverse("home"))
        # Assert
        assert response.status_code == expected

    def test_content(self) -> None:
        view_title = "Home"
        response = self.client.get(reverse("home"))
        assert view_title in response.content.decode("utf-8")


@pytest.mark.django_db
class TestListSongsView:
    client = Client()

    def test_home_connection(self) -> None:
        # Arrange
        expected = 200
        # Act
        response = self.client.get(reverse("list_songs"))
        # Assert
        assert response.status_code == expected

    def test_content(self, song) -> None:
        # Arrange
        title = [views.ListAllSongs.title]
        fields = [
            field.verbose_name
            for field in models.Song._meta.get_fields()
            if field.verbose_name != "meta data"
        ]
        song_element = [
            str(song.id),
            str(song.title),
            str(song.audio_file),
            str(song.number_of_streams),
        ]
        expected = fields + song_element + title
        # Act
        response = self.client.get(reverse("list_songs"))
        result = response.content.decode("utf-8")
        # Assert
        for element in expected:
            assert element in result


@pytest.mark.django_db
class TestLoginView:
    client = Client()

    def test_login_connection(self) -> None:
        # Arrange
        expected = 200
        # Act
        response = self.client.get(reverse("login"))
        # Assert
        assert response.status_code == expected

    def test_login_content(self) -> None:
        # Arrange
        view_content = ["Log Into Streams", "User Name", "Email", "Password"]
        # Act
        response = self.client.get(reverse("login"))
        result = response.content.decode("utf-8")
        # Assert
        for content in view_content:
            assert content in result

    def test_login_view_logs_in(self, listener) -> None:
        # Arrange / Act
        assert listener.is_active is False
        self.client.post(
            "/login/",
            {
                "name": f"{listener.name}",
                "email": "",
                "password": f"{listener.password}",
            },
            follow=True,
        )
        # Act
        listener.refresh_from_db()
        assert listener.is_active is True
        # Assert

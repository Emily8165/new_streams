import pytest
from django.test import Client
from django.urls import reverse

from streaming_app import models, views


class TestHomeView:
    client = Client()

    def test_home_connection(self) -> None:
        expected = 200
        response = self.client.get(reverse("home"))
        assert response.status_code == expected

    def test_content(self) -> None:
        view_title = "Home"
        response = self.client.get(reverse("home"))
        assert view_title in response.content.decode("utf-8")


@pytest.mark.django_db
class TestListSongsView:
    client = Client()

    def test_home_connection(self) -> None:
        expected = 200
        response = self.client.get(reverse("list_songs"))
        assert response.status_code == expected

    def test_content(self, song) -> None:
        title = [views.ListAllSongs.title]
        fields = [field.verbose_name for field in models.Song._meta.get_fields()]
        song_element = [
            str(song.id),
            str(song.title),
            str(song.audio_file),
            str(song.number_of_streams),
        ]
        expected = fields + song_element + title
        response = self.client.get(reverse("list_songs"))
        result = {
            element.strip("\t")
            for element in response.content.decode("utf-8").split("\n")
            if "<" not in element
        }
        result.remove("")
        for r in result:
            assert r in expected

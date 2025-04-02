import pytest
from django.core.management import call_command

from streaming_app import models
from streaming_app.management.commands.get_album_data import Command


class TestCommand:
    def test_get_tokens(self) -> None:
        # Arrange/Act
        token = Command().get_tokens()
        assert type(token) is dict
        assert type(token["access_token"]) is str
        assert token["token_type"] == "Bearer"
        assert token["expires_in"] == 3600

    def test_get_album_data(self) -> None:
        # Act
        token = Command().get_tokens()["access_token"]
        command = Command().get_album_data(
            album_code="5vkqYmiPBYLaalcmjujWxK", token=token
        )
        # Assert
        breakpoint()
        assert type(command) is dict
        assert command["name"] == "In Rainbows"

    @pytest.mark.django_db
    def test_handle(self) -> None:
        call_command("get_album_data", "5vkqYmiPBYLaalcmjujWxK")

        assert models.Song.objects.get(title="Nude")

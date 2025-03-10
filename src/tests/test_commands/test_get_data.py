from streaming_app.management.commands.get_data import Command


class TestCommand:
    def test_get_tokens(self) -> None:
        # Arrange/Act
        token = Command().get_tokens()
        assert type(token) is dict
        assert type(token["access_token"]) is str
        assert token["token_type"] == "Bearer"
        assert token["expires_in"] == 3600

    def test_get_artist_data(self) -> None:
        # Arrange
        expected = {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb"
            },
            "followers": {"href": None, "total": 11497921},
            "genres": ["art rock", "alternative rock"],
            "href": "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb",
            "id": "4Z8W4fKeB5YxbusRsdQVPb",
            "images": [
                {
                    "url": "https://i.scdn.co/image/ab6761610000e5eba03696716c9ee605006047fd",
                    "height": 640,
                    "width": 640,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616100005174a03696716c9ee605006047fd",
                    "height": 320,
                    "width": 320,
                },
                {
                    "url": "https://i.scdn.co/image/ab6761610000f178a03696716c9ee605006047fd",
                    "height": 160,
                    "width": 160,
                },
            ],
            "name": "Radiohead",
            "popularity": 83,
            "type": "artist",
            "uri": "spotify:artist:4Z8W4fKeB5YxbusRsdQVPb",
        }
        token = Command().get_tokens()["access_token"]
        command = Command().get_artist_data(
            artist_code="4Z8W4fKeB5YxbusRsdQVPb", token=token
        )
        assert type(command) is dict
        assert command == expected

    def test_get_album_data(self) -> None:
        # Act
        token = Command().get_tokens()["access_token"]
        command = Command().get_album_data(
            album_code="5vkqYmiPBYLaalcmjujWxK", token=token
        )
        # Assert
        assert type(command) is dict
        assert command["name"] == "In Rainbows"

    def test_get_track_data(self) -> None:
        token = Command().get_tokens()["access_token"]
        command = Command().get_track_data(
            track_code="4T1iiabe7G0UjWQJCY6NE2", token=token
        )
        # Assert
        print(command)
        assert type(command) is dict
        assert command["name"] == "Videotape"

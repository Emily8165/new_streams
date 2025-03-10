import json
import os

import numpy as np
import requests
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from PIL import Image

from streaming_app.models import Artist, ArtistMetaData, Song, SongMetaData

load_dotenv()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("code", nargs="+", type=str)

    def get_tokens(self) -> None:
        try:
            id = os.getenv("SPOTIFY_CLIENT_ID")
            password = os.getenv("SPOITFY_CLIENT_SECRET")
            get_token = os.popen(
                f'curl -X POST "https://accounts.spotify.com/api/token" \
                -H "Content-Type: application/x-www-form-urlencoded" \
                -d "grant_type=client_credentials&client_id={id}&client_secret={password}"'
            )
            token_string = get_token.read().strip()
            token_json = json.loads(token_string)
            self.stdout.write(self.style.SUCCESS("Token Aquired!"))
        except Exception as exc:
            return self.stdout.write(
                self.style.ERROR(str(exc) + "tokens not generated")
            )
        return token_json

    def get_artist_data(self, artist_code: str, token) -> dict:
        request = os.popen(
            f'curl "https://api.spotify.com/v1/artists/{artist_code}" \
            -H "Authorization: Bearer  {token}"'
        )
        artist_string = request.read().strip()
        artist_json = json.loads(artist_string)
        self.stdout.write(self.style.SUCCESS(f"data found for {artist_json['name']}"))
        return artist_json

    def get_album_data(self, album_code: str, token: str) -> dict:
        request = os.popen(
            f'curl "https://api.spotify.com/v1/albums/{album_code}" \
            -H "Authorization: Bearer  {token}"'
        )
        album_string = request.read().strip()
        album_json = json.loads(album_string)

        self.stdout.write(self.style.SUCCESS(f"data found for {album_json['name']}"))
        return album_json

    def get_track_data(self, track_code: str, token: str) -> dict:
        try:
            request = os.popen(
                f'curl "https://api.spotify.com/v1/tracks/{track_code}" \
                -H "Authorization: Bearer  {token}"'
            )
            track_string = request.read().strip()
            track_json = json.loads(track_string)
            self.stdout.write(
                self.style.SUCCESS(f"data found for {track_json['name']}")
            )
        except Exception as exc:
            return self.stdout.write(self.style.SUCCESS(exc))
        return track_json

    def create_file(self, data: dict, file_name: str) -> None:
        profile_data = {data["artist"]}
        with open(os.getcwd() + f"/src/streaming_app/data/{file_name}.json") as file:
            json.dumps(data, file)

    def get_colour(self, image_url: str) -> tuple:
        i = Image.open(requests.get(image_url, stream=True).raw)
        np_image = np.array(i)
        average_color = np_image.mean(axis=(0, 1))
        average_color = tuple(map(int, average_color))

    def handle(self, *args, **options):
        tokens = self.get_tokens()
        try:
            track_data = self.get_track_data(artist_code=options["code"], token=tokens)
            artist_data = self.get_artist_data(artist_code=track_data["artist"]["id"], token=tokens)
            song_meta_data = SongMetaData.new(
                artists=track_data["artist"][0]["name"],
                record_label=track_data["album"]["label"],
                language=track_data["language_of_performance"],
                is_cover=False,
                release_date=track_data["album"]["release_date"],
                genre="",
                lyrics="",
                main_artwork_colour=track_data["album"]["images"][0]["url"],
                main_instrument="",
                track_type=track_data["type"],
                spotify_ref=track_data["id"],
            )
            song = Song.objects.create(
                title=track_data["name"],
                audio_file=track_data["external_urls"]["spotify"],
                number_of_streams=0,
                meta_data=song_meta_data,
            )
            artist_meta_data = ArtistMetaData.objects.create(
                number_of_songs=+1,
                genre = 
            )
            artist = Artist.objects.create(
                name=track_data["artists"]["name"],
            )
        except KeyError as key_error:
            return self.stdout.write(self.style.ERROR(key_error))
        self.stdout.write(self.style.SUCCESS)


{
    "album": {
        "album_type": "album",
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb"
                },
                "href": "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb",
                "id": "4Z8W4fKeB5YxbusRsdQVPb",
                "name": "Radiohead",
                "type": "artist",
                "uri": "spotify:artist:4Z8W4fKeB5YxbusRsdQVPb",
            }
        ],
        "external_urls": {
            "spotify": "https://open.spotify.com/album/5vkqYmiPBYLaalcmjujWxK"
        },
        "href": "https://api.spotify.com/v1/albums/5vkqYmiPBYLaalcmjujWxK",
        "id": "5vkqYmiPBYLaalcmjujWxK",
        "images": [
            {
                "url": "https://i.scdn.co/image/ab67616d0000b273de3c04b5fc750b68899b20a9",
                "width": 640,
                "height": 640,
            },
            {
                "url": "https://i.scdn.co/image/ab67616d00001e02de3c04b5fc750b68899b20a9",
                "width": 300,
                "height": 300,
            },
            {
                "url": "https://i.scdn.co/image/ab67616d00004851de3c04b5fc750b68899b20a9",
                "width": 64,
                "height": 64,
            },
        ],
        "name": "In Rainbows",
        "release_date": "2007-12-28",
        "release_date_precision": "day",
        "total_tracks": 10,
        "type": "album",
        "uri": "spotify:album:5vkqYmiPBYLaalcmjujWxK",
    },
    "artists": [
        {
            "external_urls": {
                "spotify": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb"
            },
            "href": "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb",
            "id": "4Z8W4fKeB5YxbusRsdQVPb",
            "name": "Radiohead",
            "type": "artist",
            "uri": "spotify:artist:4Z8W4fKeB5YxbusRsdQVPb",
        }
    ],
    "disc_number": 1,
    "duration_ms": 279634,
    "explicit": False,
    "external_ids": {"isrc": "GBSTK0700010"},
    "external_urls": {
        "spotify": "https://open.spotify.com/track/4T1iiabe7G0UjWQJCY6NE2"
    },
    "href": "https://api.spotify.com/v1/tracks/4T1iiabe7G0UjWQJCY6NE2",
    "id": "4T1iiabe7G0UjWQJCY6NE2",
    "is_local": False,
    "name": "Videotape",
    "popularity": 58,
    "preview_url": None,
    "track_number": 10,
    "type": "track",
    "uri": "spotify:track:4T1iiabe7G0UjWQJCY6NE2",
}

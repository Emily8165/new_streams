import json
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from streaming_app import models

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
        return token_json["access_token"]

    def get_track_data(self, track_code: str, token: str) -> None:
        try:
            request = os.popen(
                f'curl "https://api.spotify.com/v1/tracks/{track_code}" \
                -H "Authorization: Bearer  {token}"'
            )
            track_string = request.read().strip()
            track_json = json.loads(track_string)
            self.stdout.write(
                self.style.SUCCESS(f"data found for {track_json["artists"][0]["name"]}")
            )
        except KeyError:
            return self.stdout.write(
                self.style.ERROR("There is a problem with the song code try it again!")
            )

        return track_json

    def handle(self, *args, **options):
        tokens = self.get_tokens()
        data = self.get_track_data(token=tokens, track_code=options["code"][0])
        name = data["artists"][0]["name"]
        try:
            models.Song.objects.get(meta_data__spotify_ref=data["id"])
            return self.stdout.write(
                self.style.SUCCESS(
                    f"{data["name"]}, by {data["artists"][0]["name"]}, has already been uploaded!"
                )
            )
        except models.Song.DoesNotExist:
            pass
        artist = models.Artist.get_or_create_artist(
            name=name,
            genres="None",
            country="None",
            artist_key=data["artists"][0]["id"],
        )

        models.Song.get_or_create_song(
            title=data["name"],
            audio=None,
            number_of_streams=0,
            artist={
                "name": artist.name,
                "genres": artist.artist_meta_data.genres,
                "country": artist.artist_meta_data.country,
                "artist_key": artist.artist_meta_data.artist_key,
            },
            release_date=data["album"]["release_date"],
            record_label="INDEPENDENT",
            track_type=data["type"],
            spotify_ref=data["id"],
            popularity=data["popularity"],
        )
        try:
            models.Song.objects.get(meta_data__spotify_ref=data["id"])
            self.stdout.write(
                self.style.SUCCESS(
                    f"{data["name"]}, by {data["artists"][0]["name"]}, Found and saved!"
                )
            )
        except models.Song.DoesNotExist:
            self.stdout.write(self.style.ERROR("Something has gone wrong"))

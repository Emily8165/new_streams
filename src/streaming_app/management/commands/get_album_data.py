import json
import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()
from streaming_app import helper_functions, models


def handle_uploaded_file(f, file_path: str):
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class Command(BaseCommand):
    token = helper_functions.Tokens.get_tokens()

    def add_arguments(self, parser):
        parser.add_argument("code", nargs="+", type=str)

    def get_album_data(self, album_code: str, token: str) -> dict:
        request = os.popen(
            f'curl "https://api.spotify.com/v1/albums/{album_code}" \
            -H "Authorization: Bearer  {token}"'
        )
        album_string = request.read().strip()
        album_json = json.loads(album_string)
        self.stdout.write(
            self.style.SUCCESS(
                f"data found for {album_json["name"]} by {album_json["artists"][0]["name"]}"
            )
        )
        return album_json

    def handle(self, *args, **options):
        tokens = self.get_tokens()
        try:
            album_data = self.get_album_data(
                album_code=options["code"][0], token=tokens["access_token"]
            )
            artist = {
                "name": album_data["artists"][0]["name"],
                "genres": "None",
                "country": "None",
                "artist_key": album_data["artists"][0]["id"],
            }
            for track_num in range(album_data["total_tracks"]):
                if not os.path.exists(
                    os.getcwd()
                    + f"/src/streaming_app/data/private_data/songs/{album_data["artists"][0]["name"]}/{album_data["tracks"]["items"][track_num]["name"].replace(" ", "_")}"
                ):
                    audio = None
                    self.stdout.write(
                        self.style.WARNING(
                            "Cannot find song file. Will continue creating meta data object."
                        )
                    )
                else:
                    audio = (
                        os.getcwd()
                        + f"/src/streaming_app/data/private_data/songs/{album_data["artists"][0]["name"]}/{album_data["tracks"]["items"][track_num]["name"].replace(" ", "_")}"
                    )
                models.Song.get_or_create_song(
                    title=album_data["tracks"]["items"][track_num]["name"],
                    audio=audio,
                    number_of_streams=1,
                    artist=artist,
                )
        except KeyError as key_error:
            return self.stdout.write(self.style.ERROR(key_error))
        self.stdout.write(self.style.SUCCESS("Finished!"))

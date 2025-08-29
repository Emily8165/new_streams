from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from streaming_app import helper_functions, models

load_dotenv()


class Command(BaseCommand):
    token = helper_functions.Tokens.get_tokens()

    def add_arguments(self, parser):
        parser.add_argument("code", nargs="+", type=str)

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

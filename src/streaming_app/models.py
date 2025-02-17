import csv
import datetime
import json
import os

from django.db import models
from mutagen.mp3 import MP3

colours = (("red", "red"), ("blue", "blue"), ("green", "green"))
track = (("ALBUM", "ALBUM"), ("EP", "EP"), ("LP", "LP"), ("SINGLE", "SINGLE"))


def get_music_genres() -> list:
    with open(
        os.getcwd() + "/src/streaming_app/data/public_data/genres.json", "r"
    ) as openfile:
        return [(i, i) for i in json.load(openfile)]


def get_languages() -> dict:
    with open(
        os.getcwd() + "/src/streaming_app/data/public_data/languages.csv", "r"
    ) as csvfile:
        reader = csv.reader(csvfile)
        return ((line[0], line[1]) for line in reader)


def calculate_song_length(file: str) -> str:
    audio = MP3(file)
    t = int(audio.info.length)
    return datetime.time.strftime("%H:%M:%S", datetime.time.gmtime(t))


class SongMetaData(models.Model):
    artist_names = models.CharField(max_length=255)
    featured_artists = models.CharField(max_length=255, null=True)
    record_label = models.CharField(max_length=50, default="Independent")
    language = models.CharField(max_length=10, choices=get_languages())
    is_cover = models.BooleanField(default=False)
    release_date = models.DateField()
    genre = models.CharField(max_length=20, choices=get_music_genres())
    lyrics = models.TextField(null=True, blank=True)
    main_artwork_colour = models.CharField(max_length=5, choices=colours)
    BPM = models.PositiveIntegerField()
    main_instruments = models.CharField(max_length=255)
    track_type = models.CharField(max_length=6, choices=track)

    @property
    def song_length(self, song_name: str) -> str:
        return calculate_song_length(f"src/streaming_app/data/{song_name}")

    @property
    def song_age(self) -> datetime.timedelta:
        return datetime.date.today() - self.release_date


class Song(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="data/")
    number_of_streams = models.PositiveIntegerField()
    meta_data = models.ForeignKey(SongMetaData, on_delete=models.CASCADE)

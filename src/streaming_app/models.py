import csv
import datetime
import json

import numpy as np
import requests
from django.db import models
from django.utils import timezone
from mutagen.mp3 import MP3
from PIL import Image

track = (("ALBUM", "ALBUM"), ("EP", "EP"), ("LP", "LP"), ("SINGLE", "SINGLE"))


def get_music_genres() -> list:
    with open("src/streaming_app/data/genres.json", "r") as openfile:
        return [(i, i) for i in json.load(openfile)]


def get_languages() -> dict:
    with open("src/streaming_app/data/languages.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        return ((line[0], line[1]) for line in reader)


def calculate_song_length(file: str) -> str:
    audio = MP3(file)
    t = int(audio.info.length)
    return datetime.time.strftime("%H:%M:%S", timezone.now())


class ArtistMetaData(models.Model):
    genres = models.CharField(max_length=20, choices=get_music_genres())
    country = models.CharField(max_length=255)
    artist_key = models.CharField(max_length=25)

    @property
    def number_of_songs(self) -> int:
        return 


class Artist(models.Model):
    name = models.CharField(max_length=255)
    artist_meta_data = models.ForeignKey(ArtistMetaData, on_delete=models.CASCADE)


class SongMetaData(models.Model):
    artists = models.ForeignKey(Artist, on_delete=models.CASCADE, default=1)
    record_label = models.CharField(max_length=50, default="Independent")
    language = models.CharField(max_length=10, choices=get_languages())
    is_cover = models.BooleanField(default=False)
    release_date = models.DateField()
    genre = models.CharField(max_length=20, choices=get_music_genres())
    lyrics = models.TextField(null=True, blank=True)
    main_artwork_colour = models.CharField(max_length=12)
    main_instruments = models.CharField(max_length=255, null=True)
    track_type = models.CharField(max_length=6, choices=track)
    spotify_ref = models.CharField(max_length=32, default=1)

    @staticmethod
    def new(
        cls,
        artist: Artist,
        featured_artists: Artist,
        record_label: str,
        language: str,
        is_cover: bool,
        release_date: datetime.date,
        genre: str,
        lyrics: str,
        main_artwork_colour: str,
        BPM: int,
        main_instruments: str,
        track_type: str,
        spotify_ref: str,
    ):
        return SongMetaData.objects.create(
            artist=artist,
            featured_artists=featured_artists,
            record_label=record_label,
            language=language,
            is_cover=is_cover,
            release_date=release_date,
            genre=genre,
            lyrics=lyrics,
            main_artwork_colour=main_artwork_colour,
            BPM=BPM,
            main_instruments=main_instruments,
            track_type=track_type,
            spotify_ref=spotify_ref,
        )

    @property
    def song_length(self, song_name: str) -> str:
        return calculate_song_length(f"src/streaming_app/data/{song_name}")

    @property
    def song_age(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.release_date

    @property
    def BPM(self) -> int:
        return 0

    @property
    def artwork_colour(self, image_url) -> str:
        i = Image.open(requests.get(image_url, stream=True).raw)
        np_image = np.array(i)
        average_color_array = np_image.mean(axis=(0, 1))
        average_color = tuple(map(int, average_color_array))
        return average_color


class Song(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to="data/")
    number_of_streams = models.PositiveIntegerField()
    meta_data = models.ForeignKey(SongMetaData, on_delete=models.CASCADE)


class ListenerMetaData(models.Model):
    total_listening_time = models.TimeField(default=timezone.now())


class Listener(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    meta_data = models.ForeignKey(ListenerMetaData, on_delete=models.CASCADE, default=1)

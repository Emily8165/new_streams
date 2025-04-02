import csv
import datetime
import json
import os
import typing

import numpy as np
import requests
from django.db import models
from django.utils import timezone
from mutagen.mp3 import MP3
from PIL import Image

track = (("ALBUM", "ALBUM"), ("EP", "EP"), ("LP", "LP"), ("SINGLE", "SINGLE"))


class CreationError(Exception):
    pass


def get_music_genres() -> list:
    with open(os.getcwd() + "/src/streaming_app/data/genres.json", "r") as openfile:
        return [(i, i) for i in json.load(openfile)]


def get_languages() -> dict:
    with open(os.getcwd() + "/src/streaming_app/data/languages.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        return ((line[0], line[1]) for line in reader)


def calculate_song_length(file: str) -> str:
    with open(file, "rb") as f:
        audio = MP3(f)
        t = int(audio.info.length)
        return datetime.time.strftime("%H:%M:%S", timezone.now())


class ArtistMetaData(models.Model):
    genres = models.CharField(max_length=20, choices=get_music_genres())
    country = models.CharField(max_length=255, default="None")
    artist_key = models.CharField(max_length=25, blank=False, null=False, default=None)

    @property
    def number_of_songs(self) -> int:
        return

    @classmethod
    def new(
        cls,
        *,
        genres: str,
        country: str,
        artist_key: str,
    ) -> "ArtistMetaData":
        """
        Method is used to create an in memory model instance
        """
        instance = cls(
            genres=genres,
            country=country,
            artist_key=artist_key,
        )
        return instance


class Artist(models.Model):
    name = models.CharField(max_length=255)
    artist_meta_data = models.ForeignKey(ArtistMetaData, on_delete=models.CASCADE)

    @classmethod
    def new(
        cls,
        *,
        name: str,
        artist_meta_data: ArtistMetaData,
    ) -> "Artist":
        """
        Method is used to create an in memory model instance
        """
        instance = cls(
            name=name,
            artist_meta_data=artist_meta_data,
        )
        return instance

    @classmethod
    def get_or_create_artist(
        cls,
        name: str | None,
        genres: str | None,
        country: str | None,
        artist_key: str | None,
    ) -> "Artist":
        try:
            if name:
                existing_artist = Artist.objects.get(name=name)
            if artist_key:
                existing_artist = Artist.objects.get(
                    artist_meta_data__artist_key=artist_key
                )
            return existing_artist
        except Artist.DoesNotExist:
            if genres is None or country is None or name is None or artist_key is None:
                raise ValueError("Args cannot be none if creating an artist")
            new_artist_meta_data = ArtistMetaData.new(
                genres=genres,
                country=country,
                artist_key=artist_key,
            )
            new_artist_meta_data.save()
            new_artist = Artist.new(name=name, artist_meta_data=new_artist_meta_data)
            new_artist.save()
            return new_artist


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
    popularity = models.IntegerField(default=0)

    @classmethod
    def new(
        cls,
        artists: Artist,
        record_label: str,
        language: str,
        is_cover: bool,
        release_date: datetime.date,
        genre: str,
        lyrics: str,
        main_artwork_colour: str,
        main_instruments: str,
        track_type: str,
        spotify_ref: str,
        popularity: int,
    ) -> "SongMetaData":
        instance = cls(
            artists=artists,
            record_label=record_label,
            language=language,
            is_cover=is_cover,
            release_date=release_date,
            genre=genre,
            lyrics=lyrics,
            main_artwork_colour=main_artwork_colour,
            main_instruments=main_instruments,
            track_type=track_type,
            spotify_ref=spotify_ref,
            popularity=popularity,
        )
        return instance

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

    @classmethod
    def new(
        cls,
        title: str,
        audio_file: typing.IO,
        number_of_streams: int,
        meta_data: SongMetaData,
    ) -> "Song":
        instance = cls(
            title=title,
            audio_file=audio_file,
            number_of_streams=number_of_streams,
            meta_data=meta_data,
        )
        return instance

    @staticmethod
    def default_values() -> dict:
        date_str = "2020-01-01"
        date_format = "%Y-%m-%d"  # Corrected format
        date_value = datetime.datetime.strptime(date_str, date_format)
        return {
            "song": None,
            "artists": Artist.get_or_create_artist(
                name="unknown",
                genres="None",
                country="country",
                artist_key="artist_key",
            ),
            "record_label": "INDEPENDENT",
            "language": "ENG",
            "is_cover": False,
            "release_date": date_value,
            "genre": "rock",
            "lyrics": "",
            "main_artwork_colour": "RED",
            "main_instruments": "DRUMS",
            "track_type": "SINGLE",
            "spotify_ref": "REF",
            "popularity": 0,
        }

    @classmethod
    def get_or_create_song(
        cls,
        title: str,
        audio: typing.IO | None,
        number_of_streams: int | None,
        artist: dict | None,
        **kwargs,
    ) -> "Song":
        """
        - Returns and instance of a song if the song exists title searched for exists.
        - If the searched for title doesn't exist then it checks to see if the artist
            exists.
        - If the artist doesn't exist then it creates one.
        - Creates song meta data
        - Creates song
        returns created song.
        """
        try:
            if title:
                existing_song = Song.objects.get(title=title)
            return existing_song
        except Song.DoesNotExist:
            if artist is None:
                raise ValueError("Args cannot be none if creating an artist")

            for field in Artist._meta.get_fields() + ArtistMetaData._meta.get_fields():
                if field.name not in list(artist.keys()):
                    kwargs[str(field.name)] = None

            artists = Artist.get_or_create_artist(
                name=artist["name"],
                genres=artist["genres"],
                country=artist["country"],
                artist_key=artist["artist_key"],
            )

            for field in SongMetaData._meta.get_fields():
                if field.name not in list(kwargs.keys()):
                    kwargs[str(field.name)] = cls.default_values()[str(field.name)]

            new_song_meta_data = SongMetaData.new(
                artists=artists,
                record_label=kwargs["record_label"],
                language=kwargs["language"],
                is_cover=kwargs["is_cover"],
                release_date=kwargs["release_date"],
                genre=kwargs["genre"],
                lyrics=kwargs["lyrics"],
                main_artwork_colour=kwargs["main_artwork_colour"],
                main_instruments=kwargs["main_instruments"],
                track_type=kwargs["track_type"],
                spotify_ref=kwargs["spotify_ref"],
                popularity=kwargs["popularity"],
            )
            new_song_meta_data.save()
            new_song = Song.new(
                title=title,
                audio_file=audio,
                number_of_streams=number_of_streams,
                meta_data=new_song_meta_data,
            )
            new_song.save()
            return new_song


class ListenerMetaData(models.Model):
    total_listening_time = models.TimeField(default=timezone.now())


class Listener(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    meta_data = models.ForeignKey(ListenerMetaData, on_delete=models.CASCADE, default=1)

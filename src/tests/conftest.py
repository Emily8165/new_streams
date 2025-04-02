import datetime
import typing

import pytest

from streaming_app import models


@pytest.fixture
def date_value() -> str:
    date_str = "2020-01-01"
    date_format = "%Y-%m-%d"  # Corrected format
    value = datetime.datetime.strptime(date_str, date_format)
    return value


@pytest.fixture
def audio_file() -> typing.IO:
    with open("src/streaming_app/data/mp3_example.mp3", "rb") as file:
        return file


@pytest.fixture
def artist_meta_data() -> models.ArtistMetaData:
    return models.ArtistMetaData.objects.create(
        genres="genres", country="country", artist_key="artist_key"
    )


@pytest.fixture
def artist(artist_meta_data: models.ArtistMetaData) -> models.Artist:
    return models.Artist.objects.create(name="name", artist_meta_data=artist_meta_data)


@pytest.fixture
def song_meta_data(artist: models.Artist) -> models.SongMetaData:
    return models.SongMetaData.objects.create(
        artists=artist,
        record_label="Independent",
        is_cover=False,
        release_date=datetime.date.today(),
        genre="Alternative",
        lyrics=None,
        main_artwork_colour="RED",
        main_instruments="Guitar",
        track_type="SINGLE",
        spotify_ref="REF",
    )


@pytest.fixture
def song(song_meta_data: models.SongMetaData) -> models.Song:
    return models.Song.objects.create(
        title="test_song",
        audio_file="streaming_app/data/mp3_example.mp3",
        number_of_streams=0,
        meta_data=song_meta_data,
    )


@pytest.fixture
def listener_meta_data() -> models.ListenerMetaData:
    return models.ListenerMetaData.objects.create(
        total_listening_time=datetime.time(0, 0, 0)
    )


@pytest.fixture
def listener(listener_meta_data: models.ListenerMetaData) -> models.Listener:
    return models.Listener.objects.create(
        name="user",
        email="fake@fakemail.com",
        password="password",
        is_active=False,
        meta_data=listener_meta_data,
    )

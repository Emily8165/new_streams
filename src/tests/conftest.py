import datetime

import pytest

from streaming_app import models


@pytest.fixture
def song_meta_data() -> models.SongMetaData:
    return models.SongMetaData.objects.create(
        artist_names="test_artist",
        featured_artists=None,
        record_label="Independent",
        is_cover=False,
        release_date=datetime.date.today(),
        genre="Alternative",
        lyrics=None,
        main_artwork_colour="RED",
        BPM=100,
        main_instruments="Guitar",
        track_type="SINGLE",
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

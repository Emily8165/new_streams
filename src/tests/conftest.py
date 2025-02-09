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
def song(song_meta_data) -> models.Song:
    return models.Song.objects.create(
        title="test_song",
        audio_file="streaming_app/data/mp3_example.mp3",
        number_of_streams=0,
        meta_data=song_meta_data,
    )

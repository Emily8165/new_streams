import typing

import pytest

from streaming_app import models


class TestArtistMetaData:
    @pytest.mark.parametrize(
        "genre,country,artist_key",
        (
            (
                "rock",
                "UK",
                "artist_key1",
            ),
            (
                "pop",
                "DE",
                "artist_key2",
            ),
            (
                "jazz",
                "PO",
                "artist_key3",
            ),
        ),
    )
    @pytest.mark.django_db
    def test_new(
        self,
        genre: str,
        country: str,
        artist_key: str,
    ) -> None:
        instance = models.ArtistMetaData.new(
            genres=genre,
            country=country,
            artist_key=artist_key,
        )

        assert instance.genres == genre
        assert instance.country == country
        assert instance.artist_key == artist_key


class TestArtist:
    @pytest.mark.django_db
    def test_get_or_create_artist_returns_artist_when_artist_exists(
        self,
        artist: models.Artist,
    ) -> models.Artist:
        assert models.Artist.objects.get(name=artist.name)

        result = models.Artist.get_or_create_artist(
            name=artist.name, genres=None, country=None, artist_key=None
        )
        assert result.name == "name"
        assert result.artist_meta_data.genres == "genres"
        assert result.artist_meta_data.country == "country"
        assert result.artist_meta_data.artist_key == "artist_key"
        assert models.Artist.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_or_create_artist_creates_artist_when_artist_doesnt_exist(
        self,
    ) -> models.Artist:
        result = models.Artist.get_or_create_artist(
            name="name", genres="genres", country="country", artist_key="artist_key"
        )
        assert result.name == "name"
        assert result.artist_meta_data.genres == "genres"
        assert result.artist_meta_data.country == "country"
        assert result.artist_meta_data.artist_key == "artist_key"
        assert models.Artist.objects.all().count() == 1

    @pytest.mark.django_db
    def test_get_or_create_raises_correct_error(self) -> models.Artist:
        with pytest.raises(ValueError) as exc:
            models.Artist.get_or_create_artist(
                name="name", genres=None, country=None, artist_key=None
            )
            assert exc == "Args cannot be none if creating an artist"
        assert models.Artist.objects.all().count() == 0


class TestSongMetaData:
    @pytest.mark.django_db
    def test_song_new(self, audio_file: typing.IO, song_meta_data) -> None:
        result = models.Song.new(
            title="title",
            audio_file=audio_file,
            number_of_streams=1,
            meta_data=song_meta_data,
        )
        assert result.title == "title"

    @pytest.mark.django_db
    def test_get_or_create_song_when_song_exists(self, song: models.Song) -> None:
        result = models.Song.get_or_create_song(
            title=song.title, audio=None, number_of_streams=None, artist=None
        )
        assert result.title == song.title
        assert result.audio_file == song.audio_file
        assert result.number_of_streams == song.number_of_streams
        assert result.meta_data == song.meta_data

    @pytest.mark.django_db
    def test_get_or_create_song_when_song_does_not_exist(
        self, audio_file: typing.IO, artist: models.Artist, date_value
    ) -> None:
        artist_dict = {
            "name": artist.name,
            "genres": artist.artist_meta_data.genres,
            "country": artist.artist_meta_data.country,
            "artist_key": artist.artist_meta_data.artist_key,
        }
        result = models.Song.get_or_create_song(
            title="title",
            audio=audio_file,
            number_of_streams=1,
            artist=artist_dict,
            release_date=date_value,
            track_type="SINGLE",
            spotify_ref="REF",
        )
        assert result.title == "title"
        assert result.audio_file == audio_file
        assert result.number_of_streams == 1
        assert result.meta_data.artists.name == artist_dict["name"]

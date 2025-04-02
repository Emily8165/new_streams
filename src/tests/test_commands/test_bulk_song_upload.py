from io import StringIO

import mock
import pytest
from django.core.management import call_command

from streaming_app import models


class TestCommand:
    @pytest.mark.django_db
    def test_handle(self) -> None:
        out = StringIO()
        mock_data = (
            i
            for i in [
                [
                    "Code",
                    "title",
                    "artist",
                    "production_rating",
                    "emily_rating",
                ],
                ["70LcF31zb1H0PyJoS1Sx1r", "Creep", "Radiohead", "10.0", "10.0"],
            ]
        )
        with mock.patch(
            "streaming_app.management.commands.upload_bulk_song_list.csv.reader",
            return_value=mock_data,
        ):
            call_command("upload_bulk_song_list")

        assert models.Artist.objects.first().name == "Radiohead"
        assert models.Song.objects.first().title == "Creep"

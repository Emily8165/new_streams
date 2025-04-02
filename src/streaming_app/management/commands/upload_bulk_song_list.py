import csv
import os

import requests
from django.core.management import call_command
from django.core.management.base import BaseCommand

from streaming_app import models


class IncorrectCodeError(Exception):
    pass


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        with open(
            os.getcwd() + "/src/streaming_app/data/private_data/spotify_codes.csv", "r"
        ) as file:
            csvFile = csv.reader(file)
            next(csvFile)
            bad_requests = {}
            for lines in csvFile:
                try:
                    models.Song.objects.get(meta_data__spotify_ref=lines[0])
                    self.stdout.write(
                        self.style.WARNING(
                            f"{lines[0]} | {lines[1]} | {lines[2]} has already been uploaded"
                        )
                    )
                    continue
                except models.Song.DoesNotExist:
                    pass
                if (
                    requests.get(
                        f"https://open.spotify.com/track/{lines[0]}"
                    ).status_code
                    != 200
                ):
                    bad_requests[f"{lines[0]}"] = lines[1:]
                    continue

                call_command("get_single_track", f"{lines[0]}")
            if bad_requests:
                print("I found there errors: \n")
                for bad_request in bad_requests:
                    self.stdout.write(
                        self.style.ERROR(f"{bad_request, bad_requests[bad_request]}")
                    )

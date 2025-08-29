import json
import os


class Tokens:
    def get_tokens(self) -> None:
        try:
            id = os.getenv("SPOTIFY_CLIENT_ID")
            password = os.getenv("SPOITFY_CLIENT_SECRET")
            get_token = os.popen(
                f'curl -X POST "https://accounts.spotify.com/api/token" \
                    -H "Content-Type: application/x-www-form-urlencoded" \
                    -d "grant_type=client_credentials&client_id={id}&client_secret={password}"'
            )
            token_string = get_token.read().strip()
            token_json = json.loads(token_string)
            print("Token Aquired!")
        except Exception:
            return "tokens not generated"
        return token_json

    def get_track_data(self, track_code: str) -> None:
        try:
            request = os.popen(
                f'curl "https://api.spotify.com/v1/tracks/{track_code}" \
                -H "Authorization: Bearer {self.get_tokens()}"'
            )
            track_string = request.read().strip()
            track_json = json.loads(track_string)
            print(f"data found for {track_json["artists"][0]["name"]}")
        except KeyError:
            return "There is a problem with the song code try it again!"
        return track_json

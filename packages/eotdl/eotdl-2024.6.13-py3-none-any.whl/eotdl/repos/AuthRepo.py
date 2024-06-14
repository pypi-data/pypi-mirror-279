from pathlib import Path
import os
import json
import jwt


class AuthRepo:
    def __init__(self):
        self.algorithms = ["RS256"]
        self.base_path = str(Path.home()) + "/.cache/eotdl/"
        os.makedirs(self.base_path, exist_ok=True)
        self.creds_path = self.base_path + "creds.json"

    def save_creds(self, data):
        with open(self.creds_path, "w") as f:
            json.dump(data, f)
        return self.creds_path

    def load_creds(self):
        if os.path.exists(self.creds_path):
            with open(self.creds_path, "r") as f:
                creds = json.load(f)
            if not "id_token" in creds and not "api_key" in creds:
                return None
            if "api_key" in creds and creds["api_key"] != os.getenv(
                "EOTDL_API_KEY", None
            ):
                return None
            return creds
        return None

    def decode_token(self, token_data):
        return jwt.decode(
            token_data["id_token"],
            algorithms=self.algorithms,
            options={"verify_signature": False},
        )

    def logout(self):
        os.remove(self.creds_path)

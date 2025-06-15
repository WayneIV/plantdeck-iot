"""Identify plants using the Plant.id API."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class PlantIdentifierConfig:
    api_key: str | None = None
    api_url: str = "https://api.plant.id/v2/identify"


class PlantIdentifier:
    """Client for the Plant.id identification API."""

    def __init__(self, config: PlantIdentifierConfig | None = None) -> None:
        self.config = config or PlantIdentifierConfig()
        if not self.config.api_key:
            self.config.api_key = os.environ.get("PLANT_ID_API_KEY", "")
        if not self.config.api_key:
            raise RuntimeError("PLANT_ID_API_KEY not provided")

    def identify(self, image_path: str) -> List[str]:
        """Return a list of probable plant names given an image path."""
        with open(image_path, "rb") as f:
            files = {"images": f}
            headers = {"Api-Key": self.config.api_key}
            response = requests.post(self.config.api_url, files=files, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        suggestions = data.get("suggestions", [])
        names = [s.get("plant_name", "") for s in suggestions]
        return names


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python plant_identifier.py <image_path>")
        raise SystemExit(1)
    pid = PlantIdentifier()
    result = pid.identify(sys.argv[1])
    print("\n".join(result))

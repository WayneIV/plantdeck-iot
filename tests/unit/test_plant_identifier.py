import builtins
from unittest import mock

import pathlib
import sys

import pytest

# Ensure project root is on sys.path for imports
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from software.services.plant_identifier_service.plant_identifier import (
    PlantIdentifier,
    PlantIdentifierConfig,
)


def test_identify_makes_request(tmp_path):
    img = tmp_path / "img.jpg"
    img.write_bytes(b"test")

    response_data = {"suggestions": [{"plant_name": "Rose"}]}
    with mock.patch("requests.post") as post:
        post.return_value.json.return_value = response_data
        post.return_value.raise_for_status.return_value = None
        identifier = PlantIdentifier(PlantIdentifierConfig(api_key="k"))
        names = identifier.identify(str(img))

    assert names == ["Rose"]
    assert post.called

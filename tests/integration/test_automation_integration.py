import pathlib
import sys
from unittest import mock

import pytest
import requests

# Ensure project root on path
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from software.services.sensor_service import server as sensor_server
from software.services.actuator_service import server as actuator_server
from software.services.automation_service.automation import (
    AutomationConfig,
    AutomationController,
)


class _Resp:
    """Minimal response object mimicking ``requests.Response``."""

    def __init__(self, flask_response):
        self.status_code = flask_response.status_code
        self._json = flask_response.get_json()

    def json(self):
        return self._json

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


@pytest.fixture
def sensor_client():
    return sensor_server.app.test_client()


@pytest.fixture
def actuator_client():
    actuator_server.state["last_action"] = None
    return actuator_server.app.test_client()


@pytest.fixture
def controller(sensor_client, actuator_client, patch_requests, mock_identifier_class):
    cfg = AutomationConfig(
        sensor_url="http://testserver/api/sensors",
        actuator_url="http://testserver/api/actuators",
        check_interval=0.0,
    )
    return AutomationController(cfg)


@pytest.fixture(autouse=True)
def patch_requests(sensor_client, actuator_client):
    def fake_get(url, *args, **kwargs):
        resp = sensor_client.get("/api/sensors")
        return _Resp(resp)

    def fake_post(url, *args, **kwargs):
        resp = actuator_client.post(
            "/api/actuators", json=kwargs.get("json", {})
        )
        return _Resp(resp)

    with mock.patch("requests.get", side_effect=fake_get), mock.patch(
        "requests.post", side_effect=fake_post
    ):
        yield


@pytest.fixture(autouse=True)
def mock_identifier_class():
    class Dummy:
        def __init__(self, *a, **kw):
            pass

        def identify(self, *a, **kw):
            return ["Mock"]

    with mock.patch(
        "software.services.automation_service.automation.PlantIdentifier",
        Dummy,
    ):
        yield


def test_low_and_high_trigger_actions(controller):
    # Low moisture should turn watering on
    with mock.patch(
        "software.services.sensor_service.server.random.uniform", return_value=0.1
    ):
        controller.step()
    assert actuator_server.state["last_action"] == "water_on"

    # High moisture should turn watering off
    with mock.patch(
        "software.services.sensor_service.server.random.uniform", return_value=0.9
    ):
        controller.step()
    assert actuator_server.state["last_action"] == "water_off"


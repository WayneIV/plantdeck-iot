"""Simple automation controller for Plant Deck."""
from __future__ import annotations

import time
from dataclasses import dataclass

import requests

from software.services.plant_identifier_service.plant_identifier import PlantIdentifier


@dataclass
class AutomationConfig:
    sensor_url: str = "http://localhost:5000/api/sensors"
    actuator_url: str = "http://localhost:5000/api/actuators"
    camera_image: str = "snapshot.jpg"
    check_interval: float = 10.0


class AutomationController:
    def __init__(self, config: AutomationConfig | None = None) -> None:
        self.config = config or AutomationConfig()
        self.identifier = PlantIdentifier()

    def read_sensors(self) -> dict:
        try:
            response = requests.get(self.config.sensor_url, timeout=2)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return {}

    def send_actuator(self, action: str) -> None:
        try:
            requests.post(self.config.actuator_url, json={"action": action}, timeout=2)
        except requests.RequestException:
            print("Failed to send command", action)

    def step(self) -> None:
        sensors = self.read_sensors()
        moisture = sensors.get("moisture", 1.0)
        if moisture < 0.3:
            self.send_actuator("water_on")
        else:
            self.send_actuator("water_off")

        try:
            plant_names = self.identifier.identify(self.config.camera_image)
            print("Identified plant:", ", ".join(plant_names))
        except Exception as e:  # broad except ok for script
            print("Identification failed:", e)

    def run(self) -> None:
        while True:
            self.step()
            time.sleep(self.config.check_interval)


if __name__ == "__main__":
    AutomationController().run()

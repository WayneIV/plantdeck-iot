import time
from dataclasses import dataclass

import cv2
import numpy as np
import requests


@dataclass
class PlantMonitorConfig:
    camera_index: int = 0
    actuator_url: str = "http://localhost:5000/api/actuators"
    check_interval: float = 5.0  # seconds


def analyze_green_ratio(frame: np.ndarray) -> float:
    """Return ratio of green pixels in the frame."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    return float(np.sum(mask)) / (mask.size * 255)


def send_actuator_command(url: str, action: str) -> None:
    try:
        requests.post(url, json={"action": action}, timeout=2)
    except requests.RequestException:
        print("Failed to send command", action)


class PlantMonitor:
    def __init__(self, config: PlantMonitorConfig | None = None) -> None:
        self.config = config or PlantMonitorConfig()
        self.cap = cv2.VideoCapture(self.config.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened")

    def step(self) -> None:
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        ratio = analyze_green_ratio(frame)
        action = "water_on" if ratio < 0.1 else "water_off"
        send_actuator_command(self.config.actuator_url, action)

    def run(self) -> None:
        try:
            while True:
                self.step()
                time.sleep(self.config.check_interval)
        finally:
            self.cap.release()


if __name__ == "__main__":
    monitor = PlantMonitor()
    monitor.run()

# Plant Deck

Smart Plant Monitoring and Automation System.

## Services

- **camera_service** - Captures images using OpenCV and analyses green foliage levels.
- **plant_identifier_service** - Uses the Plant.id API to identify plants from images. Set `PLANT_ID_API_KEY` to use it.
- **sensor_service** - Provides soil moisture readings via `/api/sensors`.
- **actuator_service** - Receives watering commands via `/api/actuators`.
- **automation_service** - Polls sensors and triggers actuators based on moisture and identification results.

## Quick Start

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Start the mock hardware services in separate terminals:

```bash
python software/services/sensor_service/server.py
python software/services/actuator_service/server.py
```

3. Run the automation controller:

```bash
PLANT_ID_API_KEY=your-key python software/services/automation_service/automation.py
```

4. (Optional) Run the web interface:

```bash
cd web
npm install
npm test
```

The automation service will periodically read moisture data and command the actuator service to turn watering on or off.

# Plant Deck

Smart Plant Monitoring and Automation System.

## Camera Service

The `camera_service` captures images using OpenCV and analyzes foliage health. Based on the analysis it sends commands to the actuator service to adjust watering automatically.

## Plant Identifier Service

The `plant_identifier_service` uses the online Plant.id API to identify plant species from captured images. Set the `PLANT_ID_API_KEY` environment variable to use this service.

## Automation Service

The `automation_service` coordinates sensors, plant identification, and actuators to maintain optimal conditions.

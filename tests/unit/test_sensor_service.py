import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from software.services.sensor_service.server import app


def test_get_sensors():
    client = app.test_client()
    resp = client.get('/api/sensors')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'moisture' in data
    assert 0.0 <= data['moisture'] <= 1.0

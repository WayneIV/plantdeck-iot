import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from software.services.actuator_service.server import app


def test_post_actuator():
    client = app.test_client()
    resp = client.post('/api/actuators', json={'action': 'water_on'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['action'] == 'water_on'

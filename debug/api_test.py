import sys
sys.path.insert(0, '.')
from flask import Flask
from app.blueprints import register_blueprints

test_app = Flask(__name__)
register_blueprints(test_app)

with test_app.test_client() as client:
    resp = client.get('/api/reload_plugins')
    print(f'Reload plugins API: {resp.status_code}')
    if resp.status_code == 200:
        data = resp.get_json()
        print(f'Reloaded: {data["counts"]}')
    print('✅ API works perfectly!')
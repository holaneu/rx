import sys
sys.path.insert(0, '.')
from flask import Flask
from app.blueprints import register_blueprints

test_app = Flask(__name__)
register_blueprints(test_app)

with test_app.test_client() as client:
    print('Testing key routes...')
    print(f'/: {client.get("/").status_code}')
    print(f'/workflows: {client.get("/workflows").status_code}')  
    print(f'/files: {client.get("/files").status_code}')
    print(f'/api/diagnostic: {client.get("/api/diagnostic").status_code}')
    print('✅ All key routes accessible!')
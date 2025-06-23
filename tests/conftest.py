import pytest
from flask import session
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.secret_key = 'test_secret'  # Necesario para sesiones

    with flask_app.test_client() as client:
        with client.session_transaction() as sess:
            sess['usuario'] = 'Maru Maru'         # Usuario simulado
            sess['rol'] = 'administrador'        # Rol permitido
        yield client
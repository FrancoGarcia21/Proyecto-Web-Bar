import pytest
from controllers.usuario import cargar_usuario, verificar_clave, obtener_un_usuario, verificar_nacimiento, mensajes_usuario

def test_cargar_usuario_exitoso(client):
    # Datos válidos, simulo el envío desde formulario
    data = {
        'dni': '12345678',
        'nombre': 'Juan Pérez',
        'fecha_nacimiento': '2000-01-01',
        'puesto': 'cajero',
        'estado': 'activo',
        'clave': 'Clave123'
    }

    # Ejecuta la solicitud POST a la ruta
    response = client.post('/usuario/cargar', data=data, follow_redirects=True)

    # Verifica que la redirección fue exitosa
    assert response.status_code == 200

    # Verifica que el mensaje de éxito esté presente en la respuesta
    assert b'ok' in response.data
    
# def test_cargar_usuario_error_dni(client):
#     # Datos con DNI inválido
#     data = {
#         'dni': '1234', # dni corto deberia fallar y no devolcer un status 200
#         'nombre': 'Juan Pérez',
#         'fecha_nacimiento': '2000-01-01',
#         'puesto': 'cajero',
#         'estado': 'activo',
#         'clave': 'Clave123'
#     }

#     # Ejecuta la solicitud POST a la ruta
#     response = client.post('/usuario/cargar', data=data, follow_redirects=True)

#     # Verificao que el mensaje de error esté  en la respuesta
#     assert b'El DNI ingresado no es v\xc3\xa1lido' in response.data
    
def test_verificar_clave(client):
    # Datos con clave inválida (sin mayúsculas)

    verificar_clave('clave123')  # Clave sin mayúsculas
    assert verificar_clave('clave123') == "Clave_sin_mayuscula"
    verificar_clave('CLAVE123')  # Clave sin minúsculas 
    assert verificar_clave('CLAVE123') == "Clave_sin_minuscula"
    verificar_clave('clave')  # Clave corta
    assert verificar_clave('clave') == "Clave_corta"
    verificar_clave('123456')  # Clave sin letras

    
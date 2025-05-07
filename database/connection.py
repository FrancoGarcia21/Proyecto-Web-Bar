import psycopg2 
import os

def get_connection():
    try:
        conexion = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'bar_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres')
        )
        return conexion
    except psycopg2.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

from database.connection import get_connection
from datetime import datetime
import random

def cargar_venta(dni_usuario, valor_total):
  """ Cargar una venta confirmada """
  conexion = get_connection()
  if conexion is None:
        return False
  
  # Busco ultima venta, asigno el id por si es la primera, consulto si no es la primera asigno a la variable el id de la ultima venta mas 1
  ultima_venta = buscar_ultima_venta()
  id_ultima_venta = 1
  
  if not ultima_venta or not ultima_venta.get('success'):
    return False

  if ultima_venta['venta'] is not None:
    id_ultima_venta = ultima_venta['venta'][0] + 1
  
   # obtengo la fecha actual
  fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
  #forma de pago, hacer un random que tire entre 0, 1 o 2, si es cero es efectivo, si es 1 tarjeta de credito y si es 2 tarjeta de debito
  formas = {0: 'Efectivo', 1: 'Tarjeta de Crédito', 2: 'Tarjeta de Débito'}
  forma_pago = formas.get(random.randint(0, 2))
  
  try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO public."ventas" (id_venta, dni_usuario, valor_total, fecha_venta, forma_pago)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_ultima_venta ,dni_usuario ,valor_total , fecha_actual, forma_pago ))
        conexion.commit()
        cursor.close()
        conexion.close()
        return id_ultima_venta
  except Exception as e:
        print("Error al cargar usuario:", e)
        return None

################# Funcion para cargar el detalle de venta
def cargar_detalle_venta(id_venta, id_producto, cantidad, precio_unitario):
    """ Cargar el detalle de una venta """
    conexion = get_connection()
    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO public."detalle_venta" (id_venta, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """, (id_venta, id_producto, cantidad, precio_unitario))
        conexion.commit()
        cursor.close()
        conexion.close()
        return True
    except Exception as e:
        print("Error al cargar detalle de venta:", e)
        return False

#################  Función para buscar la ultima venta
def buscar_ultima_venta():
    """ Buscar la última venta registrada """
    conexion = get_connection()
    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM public."ventas" ORDER BY id_venta DESC LIMIT 1')
        ultima_venta = cursor.fetchone()
        cursor.close()
        conexion.close()
        return {
            "success": True,
            "venta": ultima_venta  # este va a dar none si no hay ventas 
            }
    except Exception as e:
        print("Error al buscar la última venta:", e)
        return False 
  

from database.connection import get_connection

def cargar_venta():
  """ Cargar una venta confirmada """
  conexion = get_connection()
  if conexion is None:
        return False
      
  # try:
  #       cursor = conexion.cursor()
  #       cursor.execute("""
  #           INSERT INTO public."venta" (dni_usuario, valor_total, )
  #           VALUES (%s, %s, %s, %s, %s, %s)
  #       """, (, , , , , ))
  #       conexion.commit()
  #       cursor.close()
  #       conexion.close()
  #       return True
  # except Exception as e:
  #       print("Error al cargar usuario:", e)
  #       return False
  
  ################## 

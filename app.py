from flask import Flask,render_template#, session,flash, redirect, url_for
from dotenv import load_dotenv

from routes.stock import stock_bp
from routes.venta import venta_bp
from routes.usuario import usuario_bp
from routes.informe import informe_bp
from routes.login import login_bp

from utils.decoradores import login_required

load_dotenv()

app = Flask(__name__)

# Esta palabra se utiliza para FLASH, maneja las sesiones
app.secret_key = 'proyectoBar2025'

# Registrar Blueprints
app.register_blueprint(stock_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(informe_bp)
app.register_blueprint(login_bp)

@app.route('/')
@login_required
def home():
    """ Función principal muestra la página de inicio """

    mensaje = '<div class="bg-blue-100 border border-blue-300 text-blue-800 px-6 py-4 rounded-md shadow-md mt-6 text-center text-lg font-semibold"><h1> BIENVENIDO Desde aquí vas a poder gestionar stock, ventas, informes y usuarios.</h1></div>'
    return render_template('base.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)

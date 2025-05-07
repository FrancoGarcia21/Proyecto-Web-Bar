# from flask import Flask, render_template, url_for

# app = Flask(__name__)


# @app.route('/')
# def home():
#     return render_template('base.html')  # Esto busca el archivo en /templates


# if __name__ == '__main__':
#     app.run(debug=True)

# # RUTAS PROVISORIAS


# @app.route('/stock')
# def stock():
#     return render_template('stock.html')


# @app.route('/venta')
# def venta():
#     return render_template('venta.html')


# @app.route('/informe')
# def informe():
#     return render_template('informe.html')


# @app.route('/usuarios')
# def usuarios():
#     return render_template('usuarios.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

from flask import Flask, render_template, url_for

from dotenv import load_dotenv
load_dotenv()

from routes.stock import stock_bp
from routes.venta import venta_bp
from routes.usuario import usuario_bp
from routes.informe import informe_bp
from routes.login import login_bp


app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(stock_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(informe_bp)
app.register_blueprint(login_bp)

@app.route('/')
def home():
    """ Función principal muestra la página de inicio """
    mensaje = "BIENVENIDO Desde aquí vas a poder gestionar stock, ventas, informes y usuarios."
    return render_template('base.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)

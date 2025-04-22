from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')  # Esto busca el archivo en /templates


if __name__ == '__main__':
    app.run(debug=True)

# RUTAS PROVISORIAS


@app.route('/stock')
def stock():
    return render_template('stock.html')


@app.route('/venta')
def venta():
    return render_template('venta.html')


@app.route('/informe')
def informe():
    return render_template('informe.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/login')
def login():
    return render_template('login.html')

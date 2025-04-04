from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    print(url_for('stock'))
    print(url_for('venta'))
    print(url_for('informe'))
    print(url_for('usuarios')
          )
    return render_template('home.html')  # Esto busca el archivo en /templates


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

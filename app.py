from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Bienvenido al sistema gestor de bar!"

if __name__ == '__main__':
    app.run(debug=True)

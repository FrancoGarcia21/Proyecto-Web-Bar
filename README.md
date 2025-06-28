# 🍻 PROYECTO WEB - GESTOR DE BAR

Este es un sistema web desarrollado en **Flask** + **PostgreSQL** para gestionar productos, usuarios y ventas en un bar. Soporta roles diferenciados (administrador y vendedor) y cuenta con interfaz web. Incluye restauración de base de datos y configuración por variables de entorno.

---

## 🚀 Requisitos previos

- Python 3.9 o superiord
- PostgreSQL instalado (v13+ recomendado)
- Git
- pgAdmin o consola `psql` para restaurar base de datos

---

## 🔧 Instalación paso a paso

### 1. Clonar el repositorio

en bash
git clone https://github.com/FrancoGarcia21/Proyecto-Web-Bar.git
cd PROYECTO-WEB-BAR


### 2. Crear y activar entorno virtual
Crear y activar entorno virtual
python -m venv venv

# En Windows
.\venv\Scripts\activate

# En Linux/macOS
source venv/bin/activate

###3. Instalar dependencias - Se instalar las siguientes dependencias
pip install -r requirements.txt
blinker==1.9.0
click==8.1.8
colorama==0.4.6
Flask==3.1.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
Werkzeug==3.1.3

### 4 Configuracion - Crear un archivo .env con el siguiente contendio
FLASK_ENV=development
DEBUG=true
SECRET_KEY=clave_segura_1234

DB_HOST=localhost
DB_PORT=5432
DB_NAME="nombre de la base datos"
DB_USER=postgres
DB_PASSWORD="tu contraseña"

### 5 Restaurar base de datos El archivo de backup se encuentra en:
PROYECTO-WEB-BAR/ESTRUCTURABD/BaseDatosWebBar.backup
Para restaurar con pgAdmin:
  1-Abrí pgAdmin y conectate a tu servidor.

  2-Creá una base de datos nueva llamada Bar-Web-BD.

  3-Clic derecho sobre la base → Restore.

  4-En "Format", seleccioná Custom or tar.

  5-Seleccioná el archivo BaseDatosWebBar.backup.

  6-Hacé clic en Restore.

  ---

🧪 Tecnologías utilizadas
Flask 3.1

PostgreSQL

HTML, CSS, JavaScript (vanilla)

Jinja2

python-dotenv








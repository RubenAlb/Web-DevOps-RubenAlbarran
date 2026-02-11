import mysql.connector 
from mysql.connector import Error

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'informatica.iesquevedo.es',
    'port': 3333,
    'user': 'root',
    'password': '1asir',
    'database': 'Ruben',
    'ssl_disabled': True,
    'autocommit': False
}

# Conexión global (para compatibilidad con código antiguo)
try:
    database = mysql.connector.connect(**DB_CONFIG)
    if database.is_connected():
        print("✓ Conexión exitosa a la base de datos")
except Error as e:
    print(f"⚠ Error al conectar a la base de datos: {e}")
    raise

def get_db_connection():
    """Obtener una nueva conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"⚠ Error al conectar a la base de datos: {e}")
        raise

def init_db():
    """Inicializar la base de datos (llamado al arrancar la app)"""
    print("✓ Base de datos inicializada")
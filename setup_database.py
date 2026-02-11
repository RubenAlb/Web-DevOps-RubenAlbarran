"""
Script para crear la tabla de usuarios en la base de datos
"""
from data.database import database

def crear_tabla_usuarios():
    cursor = database.cursor()
    
    # Crear tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    print("✓ Tabla 'usuarios' creada exitosamente")
    
    # Verificar si ya existe el usuario admin
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        # Crear usuario de prueba (admin/admin123)
        cursor.execute("""
            INSERT INTO usuarios (username, password, email) VALUES 
            ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oo1qWv3OqWa2', 'admin@example.com')
        """)
        database.commit()
        print("✓ Usuario de prueba 'admin' creado exitosamente")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("⚠ El usuario 'admin' ya existe en la base de datos")
    
    cursor.close()
    print("\n¡Configuración completada!")

if __name__ == "__main__":
    crear_tabla_usuarios()

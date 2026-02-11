"""
Script para crear las tablas de tags en la base de datos
Ejecuta: python setup_tags.py
"""
import mysql.connector
from data.database import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Crear tabla tags
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(50) UNIQUE NOT NULL,
        color VARCHAR(7) DEFAULT '#007bff',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("[OK] Tabla tags creada")
    
    # Crear tabla intermedia carreras_tags
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carreras_tags (
        carrera_id INT NOT NULL,
        tag_id INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (carrera_id, tag_id),
        FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
    )
    """)
    print("[OK] Tabla carreras_tags creada")
    
    # Insertar datos de ejemplo
    cursor.execute("""
    INSERT IGNORE INTO tags (nombre, color) VALUES 
    ('Motos', '#dc3545'),
    ('Coches', '#28a745'),
    ('Rally', '#ffc107'),
    ('Circuito', '#17a2b8'),
    ('Historico', '#6c757d'),
    ('Endurance', '#e83e8c'),
    ('GT', '#fd7e14'),
    ('F1', '#20c997')
    """)
    print(f"[OK] {cursor.rowcount} etiquetas insertadas")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Sistema de tags instalado correctamente")
    
except Exception as e:
    print(f"[ERROR] {e}")

"""
Script para asignar etiquetas a las carreras existentes
"""
import mysql.connector
from data.database import DB_CONFIG

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Primero, obtener algunas carreras
    cursor.execute("SELECT id, nombre FROM carreras LIMIT 20")
    carreras = cursor.fetchall()
    
    print(f"[INFO] Encontradas {len(carreras)} carreras")
    
    if not carreras:
        print("[ERROR] No hay carreras en la base de datos")
        exit()
    
    # Obtener los tags
    cursor.execute("SELECT id, nombre FROM tags")
    tags = cursor.fetchall()
    print(f"[INFO] Encontradas {len(tags)} etiquetas")
    
    # Crear algunas relaciones de ejemplo
    # Asignar varios tags a diferentes carreras
    relaciones = []
    
    for i, (carrera_id, carrera_nombre) in enumerate(carreras):
        # Asignar 2-4 tags aleatorios a cada carrera
        if i % 3 == 0:  # Cada 3ra carrera: Coches + Circuito
            relaciones.extend([(carrera_id, tags[1][0]), (carrera_id, tags[3][0])])
        elif i % 3 == 1:  # Otra: Rally + Historico
            relaciones.extend([(carrera_id, tags[2][0]), (carrera_id, tags[4][0])])
        else:  # Otra: F1 + GT + Endurance
            relaciones.extend([(carrera_id, tags[7][0]), (carrera_id, tags[6][0]), (carrera_id, tags[5][0])])
    
    # Insertar las relaciones (IGNORE para evitar duplicados)
    for carrera_id, tag_id in relaciones:
        try:
            cursor.execute(
                "INSERT INTO carreras_tags (carrera_id, tag_id) VALUES (%s, %s)",
                (carrera_id, tag_id)
            )
        except:
            pass  # Ignorar si ya existe
    
    conn.commit()
    
    # Mostrar resumen
    cursor.execute("SELECT COUNT(*) FROM carreras_tags")
    total_relaciones = cursor.fetchone()[0]
    
    print(f"[OK] {total_relaciones} relaciones creadas en total")
    print(f"[OK] Tags asignados a {len(carreras)} carreras")
    
    # Mostrar algunas relaciones de ejemplo
    cursor.execute("""
        SELECT c.nombre, t.nombre, t.color
        FROM carreras_tags ct
        JOIN carreras c ON ct.carrera_id = c.id
        JOIN tags t ON ct.tag_id = t.id
        LIMIT 10
    """)
    
    print("\n[EJEMPLO] Primeras 10 relaciones:")
    for carrera, tag, color in cursor.fetchall():
        print(f"  - {carrera} -> {tag} ({color})")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"[ERROR] {e}")

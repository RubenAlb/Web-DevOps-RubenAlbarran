"""
Script para verificar y corregir TODA la base de datos
Ejecuta: python fix_complete.py
"""
import mysql.connector
from data.database import database

def fix_everything():
    print("="*70)
    print("  🔧 VERIFICACIÓN Y CORRECCIÓN COMPLETA DE LA BASE DE DATOS")
    print("="*70)
    
    try:
        cursor = database.cursor(dictionary=True)
        
        # ======= 1. VERIFICAR TABLAS EXISTENTES =======
        print("\n📋 PASO 1: Verificando tablas existentes...")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [list(t.values())[0] for t in tables]
        
        print(f"✅ Encontradas {len(table_names)} tablas:")
        for table in table_names:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            count = cursor.fetchone()['count']
            print(f"   • {table}: {count} registros")
        
        # ======= 2. VERIFICAR/AGREGAR COLUMNA ROL =======
        print("\n👤 PASO 2: Verificando columna 'rol' en usuarios...")
        cursor.execute("DESCRIBE usuarios")
        columns = [col['Field'] for col in cursor.fetchall()]
        
        if 'rol' not in columns:
            print("   ⚠️  Columna 'rol' NO existe. Agregando...")
            cursor.execute("ALTER TABLE usuarios ADD COLUMN rol VARCHAR(20) DEFAULT 'usuario'")
            database.commit()
            print("   ✅ Columna 'rol' agregada exitosamente")
        else:
            print("   ✅ Columna 'rol' ya existe")
        
        # ======= 3. ACTUALIZAR ROLES DE USUARIOS =======
        print("\n🔑 PASO 3: Actualizando roles de usuarios...")
        cursor.execute("UPDATE usuarios SET rol = 'admin' WHERE username = 'admin'")
        cursor.execute("UPDATE usuarios SET rol = 'usuario' WHERE username != 'admin'")
        database.commit()
        print("   ✅ Roles actualizados")
        
        # ======= 4. VERIFICAR/CREAR TABLA FAVORITOS =======
        print("\n⭐ PASO 4: Verificando tabla favoritos...")
        if 'favoritos' not in table_names:
            print("   ⚠️  Tabla 'favoritos' NO existe. Creando...")
            cursor.execute("""
                CREATE TABLE favoritos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT NOT NULL,
                    carrera_id INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_favorito (usuario_id, carrera_id)
                )
            """)
            database.commit()
            print("   ✅ Tabla 'favoritos' creada")
        else:
            print("   ✅ Tabla 'favoritos' ya existe")
        
        # ======= 5. VERIFICAR TABLA COMENTARIOS =======
        print("\n💬 PASO 5: Verificando estructura de comentarios...")
        if 'comentarios' in table_names:
            cursor.execute("DESCRIBE comentarios")
            com_columns = {col['Field']: col['Type'] for col in cursor.fetchall()}
            print("   ✅ Tabla comentarios existe con campos:")
            for field, type_ in com_columns.items():
                print(f"      • {field} ({type_})")
        else:
            print("   ⚠️  Tabla comentarios NO existe. Creando...")
            cursor.execute("""
                CREATE TABLE comentarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT NOT NULL,
                    carrera_id INT NOT NULL,
                    comentario TEXT NOT NULL,
                    valoracion INT DEFAULT 5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                    FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE CASCADE
                )
            """)
            database.commit()
            print("   ✅ Tabla comentarios creada")
        
        # ======= 6. INSERTAR COMENTARIOS DE EJEMPLO SI NO HAY =======
        print("\n📝 PASO 6: Verificando comentarios de ejemplo...")
        cursor.execute("SELECT COUNT(*) as count FROM comentarios")
        if cursor.fetchone()['count'] == 0:
            print("   ⚠️  No hay comentarios. Insertando ejemplos...")
            comentarios = [
                (1, 1, '¡Increíble circuito! Las curvas son un verdadero desafío.', 5),
                (1, 2, 'Una carrera legendaria con mucha historia.', 5),
                (2, 1, 'Spa-Francorchamps es simplemente espectacular.', 5),
            ]
            for com in comentarios:
                try:
                    cursor.execute("""
                        INSERT INTO comentarios (carrera_id, usuario_id, comentario, valoracion)
                        VALUES (%s, %s, %s, %s)
                    """, com)
                except:
                    pass
            database.commit()
            print("   ✅ Comentarios de ejemplo insertados")
        else:
            cursor.execute("SELECT COUNT(*) as count FROM comentarios")
            count = cursor.fetchone()['count']
            print(f"   ✅ Ya existen {count} comentarios")
        
        # ======= 7. MOSTRAR RESUMEN FINAL =======
        print("\n" + "="*70)
        print("  📊 RESUMEN FINAL")
        print("="*70)
        
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        print(f"👥 Usuarios: {cursor.fetchone()['count']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM carreras")
        print(f"🏁 Carreras: {cursor.fetchone()['count']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM comentarios")
        print(f"💬 Comentarios: {cursor.fetchone()['count']}")
        
        cursor.execute("SELECT COUNT(*) as count FROM favoritos")
        print(f"⭐ Favoritos: {cursor.fetchone()['count']}")
        
        print("\n👥 USUARIOS:")
        cursor.execute("SELECT id, username, email, rol FROM usuarios")
        usuarios = cursor.fetchall()
        for u in usuarios:
            emoji = "👑" if u['rol'] == 'admin' else "👤"
            print(f"   {emoji} {u['username']} ({u['email']}) - Rol: {u['rol']}")
        
        print("\n🔑 CREDENCIALES DE ACCESO:")
        print("   • Admin: admin / admin123")
        print("   • Usuario: ruben / alumno1")
        
        print("\n" + "="*70)
        print("✅ ¡BASE DE DATOS COMPLETAMENTE CONFIGURADA!")
        print("="*70)
        print("\n🚀 PRÓXIMO PASO:")
        print("   1. Guarda todos los archivos (Ctrl+S)")
        print("   2. El servidor debería recargar automáticamente")
        print("   3. Prueba: http://127.0.0.1:8000/carreras/14")
        print("   4. Inicia sesión con: admin / admin123")
        
        cursor.close()
        
    except mysql.connector.Error as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_everything()

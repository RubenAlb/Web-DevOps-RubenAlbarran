"""
Repositorio para gestionar tags (etiquetas) en la base de datos
"""

class TagRepository:
    
    def get_all_tags(self, db):
        """Obtiene todas las etiquetas disponibles"""
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tags ORDER BY nombre")
        tags = cursor.fetchall()
        cursor.close()
        return tags
    
    def get_tag_by_id(self, db, tag_id: int):
        """Obtiene una etiqueta por su ID"""
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tags WHERE id = %s", (tag_id,))
        tag = cursor.fetchone()
        cursor.close()
        return tag
    
    def get_tags_by_carrera(self, db, carrera_id: int):
        """Obtiene todas las etiquetas de una carrera"""
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.* FROM tags t
            JOIN carreras_tags ct ON t.id = ct.tag_id
            WHERE ct.carrera_id = %s
            ORDER BY t.nombre
        """, (carrera_id,))
        tags = cursor.fetchall()
        cursor.close()
        return tags
    
    def get_carreras_by_tag(self, db, tag_id: int):
        """Obtiene todas las carreras que tienen una etiqueta específica"""
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.* FROM carreras c
            JOIN carreras_tags ct ON c.id = ct.carrera_id
            WHERE ct.tag_id = %s
            ORDER BY c.nombre
        """, (tag_id,))
        carreras = cursor.fetchall()
        cursor.close()
        return carreras
    
    def crear_tag(self, db, nombre: str, color: str = '#007bff'):
        """Crea una nueva etiqueta"""
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tags (nombre, color) VALUES (%s, %s)",
            (nombre, color)
        )
        db.commit()
        tag_id = cursor.lastrowid
        cursor.close()
        return tag_id
    
    def actualizar_tag(self, db, tag_id: int, nombre: str, color: str):
        """Actualiza una etiqueta existente"""
        cursor = db.cursor()
        cursor.execute(
            "UPDATE tags SET nombre = %s, color = %s WHERE id = %s",
            (nombre, color, tag_id)
        )
        db.commit()
        cursor.close()
    
    def eliminar_tag(self, db, tag_id: int):
        """Elimina una etiqueta (y todas sus relaciones por CASCADE)"""
        cursor = db.cursor()
        cursor.execute("DELETE FROM tags WHERE id = %s", (tag_id,))
        db.commit()
        cursor.close()
    
    def agregar_tag_a_carrera(self, db, carrera_id: int, tag_id: int):
        """Asocia una etiqueta a una carrera"""
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO carreras_tags (carrera_id, tag_id) VALUES (%s, %s)",
                (carrera_id, tag_id)
            )
            db.commit()
            cursor.close()
            return True
        except Exception as e:
            # Ya existe la relación, ignorar
            cursor.close()
            return False
    
    def quitar_tag_de_carrera(self, db, carrera_id: int, tag_id: int):
        """Elimina la asociación entre una carrera y una etiqueta"""
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM carreras_tags WHERE carrera_id = %s AND tag_id = %s",
            (carrera_id, tag_id)
        )
        db.commit()
        cursor.close()

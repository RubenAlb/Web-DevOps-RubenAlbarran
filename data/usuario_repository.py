from domain.model.Usuario import Usuario
import bcrypt


class UsuarioRepository:

    def get_by_username(self, db, username: str) -> Usuario:
        """Obtiene un usuario por su nombre de usuario"""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE username = %s", (username,))
        usuario_db = cursor.fetchone()
        cursor.close()
        
        if usuario_db:
            rol = usuario_db[5] if len(usuario_db) > 5 else 'usuario'
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], rol)
        return None

    def get_by_id(self, db, user_id: int) -> Usuario:
        """Obtiene un usuario por su ID"""
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE id = %s", (user_id,))
        usuario_db = cursor.fetchone()
        cursor.close()
        
        if usuario_db:
            rol = usuario_db[5] if len(usuario_db) > 5 else 'usuario'
            return Usuario(usuario_db[0], usuario_db[1], usuario_db[2], usuario_db[3], rol)
        return None

    def crear_usuario(self, db, username: str, password: str, email: str) -> Usuario:
        """Crea un nuevo usuario con contraseña hasheada"""
        # Hashear la contraseña
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Usuarios (username, password, email) VALUES (%s, %s, %s)",
            (username, password_hash.decode('utf-8'), email)
        )
        db.commit()
        user_id = cursor.lastrowid
        cursor.close()
        
        return Usuario(user_id, username, password_hash.decode('utf-8'), email)

    def verificar_password(self, password: str, password_hash: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

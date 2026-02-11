class Usuario:
    def __init__(self, id: int, username: str, password: str, email: str, rol: str = 'usuario'):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.rol = rol
        self.is_admin = (rol == 'admin')  # Propiedad derivada

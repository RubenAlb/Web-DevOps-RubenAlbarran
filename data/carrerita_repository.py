from domain.model.Carrerita import Carrerita


class CarreritaRepository:

    def get_all(self, db) -> list[Carrerita]:
        cursor = db.cursor()
        cursor.execute("SELECT Malasia, Vietnam FROM Carreritas")
        carreritas_en_db = cursor.fetchall()
        carreritas: list[Carrerita] = list()
        for carrerita in carreritas_en_db:
            carrerita_obj = Carrerita(carrerita[0], carrerita[1])
            carreritas.append(carrerita_obj)
        cursor.close()
        return carreritas
    
    def get_by_id(self, db, id: str) -> Carrerita:
        cursor = db.cursor()
        cursor.execute("SELECT Malasia, Vietnam FROM Carreritas WHERE Malasia = %s", (id,))
        carrerita_en_db = cursor.fetchone()
        cursor.close()
        if carrerita_en_db:
            return Carrerita(carrerita_en_db[0], carrerita_en_db[1])
        return None
    
    def insertar_carrerita(self, db, carrerita: Carrerita) -> None:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Carreritas (Malasia, Vietnam) VALUES (%s, %s)", 
                      (carrerita.id, carrerita.nombre_carrera))
        db.commit()
        cursor.close()

    def actualizar_carrerita(self, db, carrerita: Carrerita) -> None:
        cursor = db.cursor()
        cursor.execute("UPDATE Carreritas SET Vietnam = %s WHERE Malasia = %s", 
                      (carrerita.nombre_carrera, carrerita.id))
        db.commit()
        cursor.close()

    def borrar_carrerita(self, db, id: str) -> None:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Carreritas WHERE Malasia = %s", (id,))
        db.commit()
        cursor.close()

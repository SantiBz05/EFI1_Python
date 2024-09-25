from app import db
from models import Marca



class MarcaRepository:
    """
    Va a ser la clase encargada de manejar el modelado en la DB.
    """

    def get_all(self):
        return Marca.query.all()
    
    def create(self, nombre, fabricante):
        nueva_marca = Marca(
            nombre=nombre,
            fabricante_id=fabricante,
        )
        db.session.add(nueva_marca)
        db.session.commit()
        return nueva_marca
    
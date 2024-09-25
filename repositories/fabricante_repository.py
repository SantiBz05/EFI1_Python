from app import db
from models import Fabricante



class FabricanteRepository:
    """
    Va a ser la clase encargada de manejar el modelado en la DB.
    """

    def get_all(self):
        return Fabricante.query.all()
    
    def create(self, nombre, origen):
        nuevo_fabricante = Fabricante(
            nombre=nombre,
            origen=origen,
        )
        db.session.add(nuevo_fabricante)    
        db.session.commit()
        return nuevo_fabricante
    
    def active(self):
        return Fabricante.query.filter_by(activo=True).all()
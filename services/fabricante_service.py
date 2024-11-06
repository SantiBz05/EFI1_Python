from repositories.fabricante_repository import FabricanteRepository


class FabricanteService:
    def __init__(self, fabricante_repository: FabricanteRepository):
        self._fabricante_repository = fabricante_repository

    def get_all(self):
        return self._fabricante_repository.get_all()

    def create(self, nombre, origen):
        return self._fabricante_repository.create(nombre, origen)

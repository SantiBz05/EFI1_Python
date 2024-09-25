from repositories.marca_repository import MarcaRepository

class MarcaService:
    def get_all(self):
        repository = MarcaRepository()
        return repository.get_all()
    
    def create(self, nombre):
        repository = MarcaRepository
        return repository.create(nombre)
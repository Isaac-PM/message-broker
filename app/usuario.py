import hashlib

class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.id = self.generar_id()

    def generar_id(self):
        # Generar un hash único basado en el nombre del usuario
        hash_object = hashlib.sha256(self.nombre.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig

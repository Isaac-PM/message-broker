class Tema:
    def __init__(self, id):
        self.id = id
        self.lista_publicaciones = []

    def agregar_publicacion(self, string):
        if len(self.lista_publicaciones) < 15:
            self.lista_publicaciones.append(string)
            print("La publicacion se agregó correctamente.")
        else:
            print("No se puede agregar más publicaciones. La lista está llena.")

    def mostrar_publicaciones(self):
        if len(self.lista_publicaciones) > 0:
            print("lista_publicaciones:")
            for string in self.lista_publicaciones:
                print(string)
        else:
            print("La lista de publicaciones está vacía.")

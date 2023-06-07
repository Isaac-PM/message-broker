import threading
from time import sleep

class Usuario:
    def __init__(self, id, tipo, suscripciones):
        self.id = id
        self.tipo = tipo
        self.suscripciones = suscripciones
        self.mensajes = []
        self.mensajes_lock = threading.Lock()

    def notificar(self, mensaje):
        with self.mensajes_lock:
            self.mensajes.append(mensaje)

class Tema:
    def __init__(self, id):
        self.id = id
        self.cola_mensajes = []
        self.suscriptores = []
        self.cola_mensajes_lock = threading.Lock()
        self.notificar = threading.Thread(target=self.notificar_suscriptores)
        self.notificar.daemon = True # Para que se detenga cuando se cierre el programa.
        self.notificar.start()
        
    def push_mensaje(self, string):
        with self.cola_mensajes_lock:
            if len(self.cola_mensajes) < 5:
                self.cola_mensajes.append(string)
                print(f"[TEMA {self.id}] El mensaje se agregó correctamente.")
                return True
            print(f"[TEMA {self.id}] No se pueden agregar más mensajes, la lista está llena.")
            return False
    
    def pop_mensaje(self):
        if len(self.cola_mensajes) > 0:
            return self.cola_mensajes.pop(0)
        return None
    
    def notificar_suscriptores(self):
        while True:
            with self.cola_mensajes_lock:
                if len(self.cola_mensajes) > 0:
                    mensaje = self.pop_mensaje()
                    for suscriptor in self.suscriptores:
                        if str(self.id) in suscriptor.suscripciones:
                            suscriptor.notificar(mensaje)
            sleep(1)

class Mensaje:
    def __init__(self, identificador, id_tema, id_usuario_emisor, contenido):
        self.identificador = identificador
        self.id_tema = id_tema
        self.id_usuario_emisor = id_usuario_emisor
        self.contenido = contenido
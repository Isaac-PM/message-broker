import grpc
import protocol_pb2
import protocol_pb2_grpc
import logging
import threading
from concurrent import futures
from tema import Tema

lock = threading.Lock()
Tema1 = Tema(1)
Usuarios = []

class MensajeServicer(protocol_pb2_grpc.MensajeServicer):
    def sesion(self, request, context):
        tipo = request.tipo
        idUsuario = request.idUsuario
        tipoUsuario = request.tipoUsuario
        suscripciones = request.suscripciones
        estado = -1
        if tipo == 1:
            with lock:
                Usuarios.append(idUsuario)
                print(f"{idUsuario} ha iniciado sesión correctamente.")

        response = protocol_pb2.SesionResponse(estado=estado)
        return response 
    
    def enviarMensaje(self, request, context):
        identificador = request.identificador
        idTema = request.idTema
        idUsuarioEmisor = request.idUsuarioEmisor
        contenido = request.contenido
        estado = 200 # si el estado es 200
        Tema1.agregar_publicacion(contenido)
        Tema1.mostrar_publicaciones()
        response = protocol_pb2.MensajeResponse(identificador=identificador, idUsuarioEmisor=idUsuarioEmisor, estado=estado)
        return response
    
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protocol_pb2_grpc.add_MensajeServicer_to_server(MensajeServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Servidor iniciado en el puerto " + port)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()


from concurrent.futures import thread
import grpc
import protocol_pb2
import protocol_pb2_grpc
import logging
import threading
from concurrent import futures
from datetime import datetime
from obj import Usuario, Tema, Mensaje

usuarios_lock = threading.Lock()
archivo_lock = threading.Lock()
tema1_lock = threading.Lock()
tema2_lock = threading.Lock()
tema3_lock = threading.Lock()

Tema1 = Tema(1)
Tema2 = Tema(2)
Tema3 = Tema(3)

usuarios = []

def escribir_archivo(data):
    with archivo_lock:
        with open("log.txt", "a") as archivo: 
            archivo.write(data + "\n")

class MensajeServicer(protocol_pb2_grpc.MensajeServicer):
    def sesion(self, request, context):
        tipo = request.tipo
        idUsuario = request.idUsuario
        tipoUsuario = request.tipoUsuario
        suscripciones = request.suscripciones.split(",")
        estado = 503
        
        if tipo == 1:
            with usuarios_lock:
                ids_usuarios = [usuario.id for usuario in usuarios]
                if idUsuario not in ids_usuarios:
                    usuario = Usuario(idUsuario, tipoUsuario, suscripciones)
                    usuarios.append(usuario)
                    if "1" in suscripciones:
                        with tema1_lock:
                            Tema1.suscriptores.append(usuario)
                    if "2" in suscripciones:
                        with tema2_lock:
                            Tema2.suscriptores.append(usuario)
                    if "3" in suscripciones:
                        with tema3_lock:
                            Tema3.suscriptores.append(usuario)
                    estado = 200
        elif tipo == 2:
            with usuarios_lock:
                ids_usuarios = [usuario.id for usuario in usuarios]
                if idUsuario in ids_usuarios:
                    usuarios.remove(idUsuario)
                    estado = 200
        
        cadena_log = f'{str(datetime.now().strftime("%d/%m/%Y:%H:%M:%S"))} '\
        f'[{"INICIO DE SESION" if tipo == 1 else "CERRAR SESION"}] '\
        f'ID Usuario: {idUsuario} '\
        f'Tipo usuario: {"Productor" if tipoUsuario == 1 else "Suscriptor"} '\
        f'Estado: {estado}'
        hilo_archivo = threading.Thread(target=escribir_archivo, args=(cadena_log,))
        hilo_archivo.start()
        hilo_archivo.join()

        response = protocol_pb2.SesionResponse(estado=estado)
        return response 
    
    def enviarMensaje(self, request, context):
        identificador = request.identificador
        idTema = request.idTema
        idUsuarioEmisor = request.idUsuarioEmisor
        contenido = request.contenido
        estado = 200
        mensaje = Mensaje(identificador, idTema, idUsuarioEmisor, contenido)
        if idTema == 1:
            with tema1_lock:
                Tema1.switch_lock()
                Tema1.push_mensaje(mensaje)
                Tema1.switch_lock()
        elif idTema == 2:
            with tema2_lock:
                Tema2.switch_lock()
                Tema2.push_mensaje(mensaje)
                Tema2.switch_lock()
        elif idTema == 3:
            with tema3_lock:
                Tema3.switch_lock()
                Tema3.push_mensaje(mensaje)
                Tema3.switch_lock()
        else:
            estado = 503
        cadena_log = f'{str(datetime.now().strftime("%d/%m/%Y:%H:%M:%S"))} '\
        f'[ENVIAR MENSAJE] '\
        f'ID Usuario: {idUsuarioEmisor} '\
        f'ID Tema: {idTema} '\
        f'Contenido: {contenido} '\
        f'Estado: {estado}'
        hilo_archivo = threading.Thread(target=escribir_archivo, args=(cadena_log,))
        hilo_archivo.start()
        hilo_archivo.join()
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


"""
Servidor gRPC que sigue un patrón publicador/suscriptor.

Author: Isaac Fabián Palma Medina y Karla Verónica Quiros Delgado
Date: June 8, 2023
"""

import grpc
import protocol_pb2
import protocol_pb2_grpc
import logging
import threading
import signal
from concurrent import futures
from datetime import datetime
from concurrent.futures import thread
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
    """Utiliza un lock para evitar que se escriba en un archivo de texto al mismo tiempo.

    Args:
        data (string): Cadena de texto a escribir en el archivo.
    """
    with archivo_lock:
        with open("log.txt", "a") as archivo: 
            archivo.write(data + "\n")

class MensajeServicer(protocol_pb2_grpc.MensajeServicer):
    def sesion(self, request, context):
        """Inicia o cierra una sesión de usuario.

        Args:
            request (request): Es enviado por un cliente.

        Returns:
            SesionResponse: Es enviado al cliente, contiene si el inicio o cierre de sesión fue exitoso o no (estado).
        """
        tipo = request.tipo
        idUsuario = request.idUsuario
        tipoUsuario = request.tipoUsuario
        suscripciones = request.suscripciones.split(", ")
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
                else:
                    estado = 409
        elif tipo == 2:
            with usuarios_lock:
                ids_usuarios = [usuario.id for usuario in usuarios]
                if idUsuario in ids_usuarios:
                    usuario = usuarios[ids_usuarios.index(idUsuario)]
                    usuarios.remove(usuario)
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
        """Envía un mensaje a un tema.

        Args:
            request (MensajeRequest): Es enviado por un cliente (productor).

        Returns:
            MensajeResponse: Es enviado al cliente, contiene si el envío del mensaje fue exitoso o no (estado).
        """
        identificador = request.identificador
        idTema = request.idTema
        idUsuarioEmisor = request.idUsuarioEmisor
        contenido = request.contenido
        estado = 200
        mensaje = Mensaje(identificador, idTema, idUsuarioEmisor, contenido)
        if idTema == 1:
            with tema1_lock:
                ingresado = Tema1.push_mensaje(mensaje)
                if not ingresado: estado = 503
        elif idTema == 2:
            with tema2_lock:
                ingresado = Tema2.push_mensaje(mensaje)
                if not ingresado: estado = 503
        elif idTema == 3:
            with tema3_lock:
                ingresado = Tema3.push_mensaje(mensaje)
                if not ingresado: estado = 503
        else:
            estado = 400
        cadena_log = f'{str(datetime.now().strftime("%d/%m/%Y:%H:%M:%S"))} '\
        f'[ENVIAR MENSAJE] '\
        f'ID Mensaje: {identificador} '\
        f'ID Usuario: {idUsuarioEmisor} '\
        f'ID Tema: {idTema} '\
        f'Contenido: {contenido} '\
        f'Estado: {estado}'
        hilo_archivo = threading.Thread(target=escribir_archivo, args=(cadena_log,))
        hilo_archivo.start()
        hilo_archivo.join()
        response = protocol_pb2.MensajeResponse(identificador=identificador, idUsuarioEmisor=idUsuarioEmisor, estado=estado)
        return response
    
    def escuchar(self, request, context):
        """Escucha por los mensajes de un tema, para un usuario en específico.

        Args:
            request (EscuchaRequest): Es enviado por el cliente (suscriptor).

        Returns:
            EscuchaResponse: Es enviado al cliente, contiene los mensajes que se enviaron al usuario, en todos los temas a los que está suscrito.
        """
        idUsuario = request.idUsuario
        estado = 200
        mensajes = []
        mensajes_struct = []
        with usuarios_lock:
            ids_usuarios = [usuario.id for usuario in usuarios]
            if idUsuario in ids_usuarios:
                usuario = usuarios[ids_usuarios.index(idUsuario)]
                mensajes = usuario.mensajes
                if len(mensajes) > 0:
                    setattr(usuario, 'mensajes', [])
                    for mensaje in mensajes:
                        cadena_log = f'{str(datetime.now().strftime("%d/%m/%Y:%H:%M:%S"))} '\
                        f'[MENSAJE ENVIADO] '\
                        f'ID Usuario receptor: {idUsuario} '\
                        f'ID Mensaje: {mensaje.identificador} '
                        hilo_archivo = threading.Thread(target=escribir_archivo, args=(cadena_log,))
                        hilo_archivo.start()
                        hilo_archivo.join()
                        mensajes_struct = [protocol_pb2.MensajeStruct(
                            identificador=mensaje.identificador,
                            idTema=int(mensaje.id_tema),
                            idUsuarioEmisor=mensaje.id_usuario_emisor,
                            contenido=mensaje.contenido
                        ) for mensaje in mensajes]
                else:
                    estado = 400
        response = protocol_pb2.EscuchaResponse(estado=estado, mensajes=mensajes_struct)
        return response

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    protocol_pb2_grpc.add_MensajeServicer_to_server(MensajeServicer(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Servidor iniciado en el puerto " + port)
    print("Presione Ctrl + C para detener el servidor...")

    def signal_handler(sig, frame):
        print('Deteniendo servidor...')
        server.stop(0)
        exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()


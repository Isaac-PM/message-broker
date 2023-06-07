import grpc
import protocol_pb2
import protocol_pb2_grpc
import logging
import re
import hashlib
import time
import os
from time import sleep
from concurrent import futures

def sesion(_tipo, _idUsuario, _tipoUsuario, _suscripciones):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = protocol_pb2_grpc.MensajeStub(channel)
        response = stub.sesion(protocol_pb2.SesionRequest(tipo =_tipo, idUsuario = _idUsuario, tipoUsuario = _tipoUsuario, suscripciones = _suscripciones))
    return response.estado

def escucharMensajes(_idUsuario):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = protocol_pb2_grpc.MensajeStub(channel)
        response = stub.escuchar(protocol_pb2.EscuchaRequest(idUsuario = _idUsuario))
        if response.estado == 200:
            for mensaje in response.mensajes:
                print(f">>>>>>>>>> Mensaje recibido en el tema {mensaje.idTema} <<<<<<<<<<")
                print("Emisor:", mensaje.idUsuarioEmisor)
                print("Contenido:", mensaje.contenido)
                print()

def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def enviarMensaje(_idUsuarioEmisor):
    print(">>>>>>>>>> Enviar un mensaje <<<<<<<<<<")
    print("\tDigite el contenido del mensaje:")
    _contenido = input()
    _idTema = -1

    while _idTema != 1 and _idTema != 2 and _idTema != 3:
        print("\tDigite el identificador del tema (1 al 3):")
        _idTema = int(input())
    
    hash = hashlib.md5()
    hash.update(_contenido.encode('utf-8'))
    _identificador = hash.hexdigest()
    _identificador += str(int(time.time() * 1000)) + str(_idTema)
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = protocol_pb2_grpc.MensajeStub(channel)
        response = stub.enviarMensaje(protocol_pb2.MensajeRequest(identificador = _identificador, idTema = _idTema, idUsuarioEmisor = _idUsuarioEmisor, contenido = _contenido))
    if response.estado == 200:
        print(f"[{_idUsuarioEmisor} : {_identificador}] Tema: {_idTema}, Contenido: {_contenido}")
        print("Mensaje enviado con éxito, enter para continuar.")
    else:
        print("Error al enviar el mensaje, enter para continuar.")
    input()

def menu_cliente():
    print(">>>>>>>>>> Cliente gRPC <<<<<<<<<<")
    print("\tDigite su nombre de usuario:")
    idUsuario = input()

    tipoUsuario = ""
    while tipoUsuario != "1" and tipoUsuario != "2":
        print("\tDigite el tipo de usuario (1 = Productor, 2 = Suscriptor):")
        tipoUsuario = input()
    
    tipoUsuario = int(tipoUsuario)
    suscripciones = ""
    if tipoUsuario == 2:
        patron = r'^(1|2|3)(,\s(1|2|3))*$' # Pendiente procesar en el servidor.
        suscripciones = ""
        while not re.match(patron, suscripciones):
            print("\tDigite las suscripciones (números del 1 al 3, separados por comas y un espacio):")
            suscripciones = input()
    
    estado = sesion(1, idUsuario, tipoUsuario, suscripciones) # El tipo 1 indica que es una solicitud de inicio de sesión.
    if estado == 200:
        print("Sesión iniciada con éxito, enter para continuar.")
        input()

        if tipoUsuario == 1: # Productor.
            cerrarSesion = False
            while not cerrarSesion:
                limpiar_pantalla()
                print(">>>>>>>>>> Menú productor <<<<<<<<<<")
                print("\tEnviar un mensaje (1)")
                print("\tCerrar sesión (2)")
                print("\tDigite la opción deseada:")
                opcion = int(input())
                if opcion == 1:
                    limpiar_pantalla()
                    enviarMensaje(idUsuario)
                elif opcion == 2:
                    cerrarSesion = True
                else:
                    print("Opción inválida, enter para continuar.")
                    input()
        else: # Suscriptor.
            limpiar_pantalla()
            print(">>>>>>>>>> Menú consumidor <<<<<<<<<<")
            print(f"Escuchando mensajes en el (los) tema(s) {suscripciones}...")
            print("Presione Ctrl + C para cerrar sesión.")
            print()
            while True:
                escucharMensajes(idUsuario)
                sleep(2)
    
        estado = sesion(2, idUsuario, tipoUsuario, suscripciones) # El tipo 2 indica que es una solicitud de cierre de sesión.
        if estado == 200: print("Sesión cerrada con éxito.")
        else: print("Error al cerrar sesión, se detuvo la aplicación.")
        exit()
        
    elif estado == 409:
        print("Se detectó un nombre de usuario duplicado, intente de nuevo.")
        exit()

if __name__ == '__main__':
    logging.basicConfig()
    menu_cliente()

II Proyecto de Sistemas Operativos
Isaac Fabián Palma Medina y Karla Verónica Quiros Delgado

Instrucciones de uso:

1. Abrir la carpeta del proyecto (MessageBroker) en una terminal compatible con caracteres especiales, además asegurarse de poseer Python debidamente instalado.
2. Ejecutar el comando source env/Scripts/activate para incluir las librerías del entorno virtual.
3. Ejecutar el comando pip install grpcio grpcio-tools para adquirir las funcionalidades de gRPC.
4. Ejecutar el comando cd app.
5. Iniciar el servidor usando la versión de Python disponible (python, python3, python.exe, etc.) -> python servidor.py
6. Para ejecutar el cliente, abrir la carpeta en otra(s) terminal(es), y el comando source env/Scripts/activate
7. Ejecutar nuevamente el comando cd app en la terminal.
8. Iniciar el cliente usando la versión de Python disponible (python, python3, python.exe, etc.) -> python cliente.py

Referencias:

- ByteMonk. (2022, 28 mayo). Publisher Subscriber Pattern | Pub Sub | System Design [Vídeo]. YouTube. https://www.youtube.com/watch?v=algmP8MGeL4 
- gRPC. (2023, 15 febrero). Basics tutorial. gRPC.io. https://grpc.io/docs/languages/python/basics/ 
- gRPC Community. (s. f.). GitHub - grpc/grpc: The C based gRPC (C++, Python, Ruby, Objective-C, PHP, C#). GitHub. https://github.com/grpc/grpc 
- Manchanda, N. (s. f.). Implementing gRPC In Python: A Step-by-step Guide. https://www.velotio.com/engineering-blog/grpc-implementation-using-python Protocol Buffers Documentation. (s. f.). 
- Language Guide (proto 3). https://protobuf.dev/programming-guides/proto3/ 
- Szabo, G. (s. f.). Signal handling: Catch Ctrl-C in Python. Code Maven. https://code-maven.com/catch-control-c-in-python

Notas:

- Toda la documentación de los archivos Python cumple con el estándar PEP 257 @ https://peps.python.org/pep-0257/
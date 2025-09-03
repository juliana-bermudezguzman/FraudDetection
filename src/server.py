import socket
import threading
import time
import csv
from datetime import datetime

# Define el host y el puerto
host = "0.0.0.0"
port = 5050

# Lee el archivo
# Ruta del archivo CSV a enviar

archivo = 'Fraud.csv'
delimitador = ','  # Delimitador utilizado en el archivo CSV

# Crea el socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula el socket al host y puerto
sock.bind((host, port))

# Escucha por conexiones entrantes
sock.listen()

# Función para enviar una línea de texto por el socket
def send_line(line, client_socket):

    mensaje = '22523,2022-11-20 00:00:00+00:00,24,Twitter Web App,"How to buy $SOT on PinkSale?\xf0\x9f\xa4\x94 \nHave you been confused about how to buy tokens on PinkSale by the most simple steps?\n\xf0\x9f\x91\x89Follow the below-detailed video to purchase $SOT on PinkSale. \n\xf0\x9f\x92\xb0 Buy here - limited quantities: https://t.co/3aLmaiFibc\n#SoccerCrypto #football #worldcup2022 https://t.co/mVVYvrDQMZ",neutral\n'

    #client_socket.sendall(mensaje.encode())
    client_socket.send((line).encode('utf-8')) 


# Función que maneja cada conexión de cliente
def manejar_cliente(client_socket, client_address):
    print(f"Cliente conectado desde {client_address}")
    while True:
        try:
            with open('Fraud.csv' , newline='') as file:
                reader = csv.reader(file)
		    # Leer la primera línea para tener una referencia de tiempo inicial
                line = next(reader)
                line = next(reader)
                primera_fecha_str = line[1]  # Segunda columna del archivo CSV
                print (primera_fecha_str)
                # Enviar la línea por el socket
   #             line = delimitador.join(line[:-2]) +",\"" + line[4]+"\"," + line[5]+"\n"
   #              send_line(line, client_socket)
                for line in sorted(reader, key=lambda x: x[1]):
                    print(line)
                    line = delimitador.join(line[:]) +"\n"

                    # Enviar la línea por el socket
                    send_line(line, client_socket)
                    # print(f'Se envía el stream:\n{line}')

                print(f'Fin del envio {client_address}')
                client_socket.close()
		    
	  
        except ConnectionResetError: 
		# Manejar cualquier excepción para permitir la reconexión del cliente
            print(f'Error: {e}')

    client_socket.close()
    print(f"Cliente desconectado desde {client_address}")

# Acepta conexiones entrantes y maneja cada cliente en un hilo separado
while True:
    print(f"Esperando ....")

    client, address = sock.accept()
    t = threading.Thread(target=manejar_cliente, args=(client, address))
    t.start()

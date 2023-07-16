import socket
import random

HOST = 'localhost'  # Endereço IP do servidor
PORT = 8007  # Porta que o servidor está escutando

def gerar_string(comprimento):
    #Retorna uma string de comprimento especificado
    
    return 'a' * comprimento

def handle_connection(conn, addr):
    try:
        data = conn.recv(1024).decode()
        print(f"Número enviado pelo cliente: {data}")
        if len(data) > 10:
            string = gerar_string(len(data)) + 'FIM'
            conn.sendall(string.encode())
        else:
            if int(data) % 2 == 0:
                print(f"{data} O seu número é par")
                conn.sendall('PAR'.encode())
            else:
                print(f"{data} O seu número é impar")
                conn.sendall('IMPAR'.encode())
    except Exception as e:
        print(f"Erro ocorreu no cliente {addr}: {str(e)}")
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Servidor escutando em {HOST}:{PORT}...')
    while True:
        conn, addr = s.accept()
        handle_connection(conn, addr)
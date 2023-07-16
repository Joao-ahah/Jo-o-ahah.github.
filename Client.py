import socket
import time
import random
import PySimpleGUI as sg

HOST = 'localhost'  # Endereço IP do servidor
PORT = 8007  # Porta que o servidor está escutando

# Define a interface
layout = [
    [sg.Text('Gerar Número', font='Arial', size=(20,1)), sg.Button('Gerar', font='Arial')],
    [sg.Text('Número Gerado:', font='Arial', size=(20,1)), sg.Text('', font='Arial', size=(40,1), key='generated')],
    [sg.Text('Enviar Número', font='Arial', size=(20,1)), sg.Input(size=(30,1), font='Arial', key='number'), sg.Button('Enviar', font='Arial')],
    [sg.Text('Resposta do Servidor', font='Arial', size=(20,1)), sg.Text('', font='Arial', size=(60,1), key='response')]
]

window = sg.Window('Interface do Cliente', layout)

def generate_number():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # Gera um número aleatório com até 30 casas
        num = str(random.randint(1, 10**30))
        
        s.sendall(num.encode())
        data = s.recv(1024).decode()
        
        print(f'String enviado do servidor: {data} ')
        window['generated'].update(num)
        window['response'].update(f'Resposta do servidor: {data} ')

generate_automatically = False

while True:
    event, values = window.read(timeout=10000)
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'Gerar':
        num = str(random.randint(1, 10**30))
        window['generated'].update(num)
        generate_automatically = True
        
    if event == 'Enviar':
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                
                num = window['number'].get()
                s.sendall(num.encode())
                data = s.recv(1024).decode()

                print(f'Resposta do servidor: {data} ')
                window['response'].update(f'Resposta do servidor: {data} ')
        except:
            sg.popup_error('Não foi possível enviar os dados para o servidor')
    
    if generate_automatically:
        generate_number()

window.close()

import threading
import socket

clients = []
managers = {"Financeiro": None, "Logistica": None, "Atendimento": None}

def handle_client(client_socket, address):
    global clients, managers
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                area, question = message.split(":", 1)
                if area in managers and managers[area]:
                    managers[area].send(f"[Cliente {address[0]}] Pergunta: {question.strip()}".encode())
                    client_socket.send(f"[Sucesso] Sua dúvida foi enviada para o gerente de {area}.".encode())
                else:
                    client_socket.send(f"[Erro] Nenhum gerente disponível para {area} no momento.".encode())
            else:
                break
        except:
            clients.remove(client_socket)
            break
    client_socket.close()

def handle_manager(manager_socket, area):
    while True:
        try:
            message = manager_socket.recv(1024).decode()
            if message:
                broadcast(f"[{area} Gerente] Resposta: {message.strip()}", manager_socket)
            else:
                break
        except:
            managers[area] = None
            break
    manager_socket.close()

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message.encode())

def start_server():
    global managers
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(10)
    print("Servidor rodando na porta 5555...\n")

    while True:
        client_socket, address = server.accept()
        print(f"Nova conexão de {address[0]}:{address[1]}")

        role = client_socket.recv(1024).decode()
        if role in managers:  # É um gerente para uma área específica
            managers[role] = client_socket
            print(f"Gerente de {role} conectado.")
            manager_thread = threading.Thread(target=handle_manager, args=(client_socket, role))
            manager_thread.start()
        else:  # É um cliente
            clients.append(client_socket)
            print("Cliente conectado.")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    start_server()

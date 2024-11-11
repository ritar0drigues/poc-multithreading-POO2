import socket
import threading

# Estrutura para armazenar clientes e gerentes por área
clients = {"Financeiro": [], "Logistica": [], "Atendimento": []}
managers = {"Financeiro": None, "Logistica": None, "Atendimento": None}
messages = []  # Histórico de todas as mensagens trocadas

def handle_client(client_socket, address, area):
    print(f"[Servidor] Cliente conectado na área {area} de {address}")
    clients[area].append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"[Servidor] Mensagem recebida: {message}")
                # Registro no histórico do servidor
                messages.append(f"[Cliente {address[0]}:{address[1]} em {area}] Pergunta: {message}")
                
                if message == "concluido1234":
                    print(f"[Servidor] Cliente {address} desconectou da área {area}.")
                    clients[area].remove(client_socket)
                    client_socket.send("Conexão encerrada.".encode())
                    break
                
                # Encaminha a mensagem para o gerente da área
                if managers[area]:
                    managers[area].send(f"[Cliente {address[0]}:{address[1]}] Pergunta: {message}".encode())
                    client_socket.send(f"Sua dúvida foi enviada para o gerente de {area}.".encode())
                else:
                    client_socket.send(f"[Erro] Nenhum gerente disponível para {area} no momento.".encode())
            else:
                break
        except Exception as e:
            print(f"[Erro Cliente] {e}")
            clients[area].remove(client_socket)
            break
    client_socket.close()

def handle_manager(manager_socket, area):
    print(f"[Servidor] Gerente de {area} conectado.")
    managers[area] = manager_socket

    while True:
        try:
            message = manager_socket.recv(1024).decode()
            if message:
                print(f"[Servidor] Mensagem do gerente: {message}")
                messages.append(f"[Gerente de {area}] Resposta: {message}")
                
                if message == "concluido1234":
                    print(f"[Servidor] Gerente de {area} desconectado.")
                    managers[area] = None
                    manager_socket.send("Conexão encerrada.".encode())
                    break

                # Enviar resposta para todos os clientes da área
                for client in clients[area]:
                    client.send(f"[Gerente de {area}] Resposta: {message}".encode())
                
                # Confirmação para o gerente
                manager_socket.send("Resposta enviada aos clientes.".encode())
            else:
                break
        except Exception as e:
            print(f"[Erro Gerente] {e}")
            managers[area] = None
            break
    manager_socket.close()

def start_area_server(area, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))  # Escuta em toda a rede local
    server.listen(5)
    print(f"Servidor de {area} rodando na porta {port}...\n")

    while True:
        client_socket, address = server.accept()
        role = client_socket.recv(1024).decode()
        
        if role == "gerente":
            manager_thread = threading.Thread(target=handle_manager, args=(client_socket, area))
            manager_thread.start()
        elif role == "cliente":
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address, area))
            client_thread.start()

if __name__ == "__main__":
    threading.Thread(target=start_area_server, args=("Financeiro", 5555)).start()
    threading.Thread(target=start_area_server, args=("Logistica", 5556)).start()
    threading.Thread(target=start_area_server, args=("Atendimento", 5557)).start()

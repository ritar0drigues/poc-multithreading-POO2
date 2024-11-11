import socket
import threading

#Estrutura para armazenamento de clientes e gerentes por área
clients = {"Administrador": [], "Logistica": [], "Atendimento": []}
managers = {"Administrador": None, "Logistica": None, "Atendimento": None}
messages = [] #Lista para armazenamento do histórico de todas as mensagens trocadas

#Função para lidar com a comunicação de um cliente: recebendo as mensagens do cliente e as encaminhando para o gerente da área correspondente, se disponível.
def handle_client(client_socket, address, area):
    print(f"[Servidor] Cliente conectado na área {area} de {address}")
    clients[area].append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"[Servidor] Mensagem recebida: {message}")
                #Registro no histórico do servidor
                messages.append(f"[Cliente {address[0]}:{address[1]} em {area}] Pergunta: {message}")
                
                #Condição em caso de desconexão do cliente
                if message == "concluido1234":
                    print(f"[Servidor] Cliente {address} desconectou da área {area}.")
                    clients[area].remove(client_socket)
                    client_socket.send("Conexão encerrada.".encode())
                    break
                
                #Encaminhamento da mensagem para o gerente da área, se disponível
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

#Função para lidar com a comunicação de um gerente: recebendo as mensagens do gerente e as distribuindo para todos os clientes da área correspondente.
def handle_manager(manager_socket, area):
    print(f"[Servidor] Gerente de {area} conectado.")
    managers[area] = manager_socket

    while True:
        try:
            message = manager_socket.recv(1024).decode()
            if message:
                #Registro da resposta no histórico
                print(f"[Servidor] Mensagem do gerente: {message}")
                messages.append(f"[Gerente de {area}] Resposta: {message}")
                
                #Condição em caso de desconexão do gerente
                if message == "concluido1234":
                    print(f"[Servidor] Gerente de {area} desconectado.")
                    managers[area] = None
                    manager_socket.send("Conexão encerrada.".encode())
                    break

                #Envio da resposta para todos os clientes da área
                for client in clients[area]:
                    client.send(f"[Gerente de {area}] Resposta: {message}".encode())
                
                #Confirmação do envio para o gerente
                manager_socket.send("Resposta enviada aos clientes.".encode())
            else:
                break
        except Exception as e:
            print(f"[Erro Gerente] {e}")
            managers[area] = None
            break
    manager_socket.close()

#Função para iniciar o servidor para uma área específica, escutando em uma porta dedicada: aceitando as conexões tanto de clientes quanto de gerentes e criando threads separadas para tratá-los.
def start_area_server(area, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port)) #Permite que o servidor escute em toda a rede local
    server.listen(5)
    print(f"Servidor de {area} rodando na porta {port}...\n")

    while True:
        client_socket, address = server.accept()
        role = client_socket.recv(1024).decode()
        
        #Identificando se é um gerente ou um cliente conectando e iniciando uma thread apropriada
        if role == "gerente":
            manager_thread = threading.Thread(target=handle_manager, args=(client_socket, area))
            manager_thread.start()
        elif role == "cliente":
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address, area))
            client_thread.start()

if __name__ == "__main__":
    #Iniciando o servidor para cada área em uma porta diferente, usando threads para cada uma
    threading.Thread(target=start_area_server, args=("Administrador", 5555)).start()
    threading.Thread(target=start_area_server, args=("Logistica", 5556)).start()
    threading.Thread(target=start_area_server, args=("Atendimento", 5557)).start()

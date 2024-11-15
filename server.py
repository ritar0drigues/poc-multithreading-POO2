import socket
import threading

#Estrutura para armazenamento de clientes e gerentes por área
clients = {"Administrador": [], "Logistica": [], "Atendimento": [], "TestArea": []}
managers = {"Administrador": None, "Logistica": None, "Atendimento": None, "TestArea": None}

messages = [] #Lista para armazenamento do histórico de todas as mensagens trocadas

class Server:
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
                        managers[area].send(f"{message}".encode())
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
                    messages.append(f"{message}")
                    
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
                    # Atualizar este bloco em handle_manager
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
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Permite reutilização de portas
        server.bind(('localhost', port))
        server.listen(5)

        print(f"Servidor de {area} rodando na porta {port}...\n")

        while True:
            try:
                client_socket, address = server.accept()
                role = client_socket.recv(1024).decode()

                # Verifica se o comando para encerrar o servidor foi enviado
                if role == "shutdown_server":
                    print(f"[Servidor {area}] Encerrando servidor...")
                    for client in clients[area]:
                        client.close()  # Fecha todas as conexões de clientes
                    if managers[area]:
                        managers[area].close()  # Fecha a conexão do gerente, se existir
                    server.close()  # Fecha o socket do servidor
                    break

                if role == "gerente":
                    manager_thread = threading.Thread(target=Server.handle_manager, args=(client_socket, area))
                    manager_thread.start()
                elif role == "cliente":
                    client_thread = threading.Thread(target=Server.handle_client, args=(client_socket, address, area))
                    client_thread.start()
            except Exception as e:
                print(f"[Erro Servidor {area}] {e}")
                server.close()
                break



if __name__ == "__main__":
    #Iniciando o servidor para cada área em uma porta diferente, usando threads para cada uma
    threading.Thread(target=Server.start_area_server, args=("Administrador", 5555)).start()
    threading.Thread(target=Server.start_area_server, args=("Logistica", 5556)).start()
    threading.Thread(target=Server.start_area_server, args=("Atendimento", 5557)).start()
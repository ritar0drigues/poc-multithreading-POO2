import socket
import threading

#Função para recebimento de mensagens enviadas pelos clientes: loop contínuo que escuta mensagens até que o servidor ou o gerente finalize a conexão. Exibe a mensagem recebida e finaliza a conexão se a mensagem for "Conexão encerrada.".
def receive_messages(manager_socket):
    while True:
        try:
            #Recebimento da mensagem do servidor (ou de um cliente encaminhada pelo servidor)
            message = manager_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
                #Em caso do servidor encerrar a conexão, interrompe o loop
                if message == "Conexão encerrada.":
                    print("[Sistema] Conexão finalizada pelo servidor.")
                    break
            else:
                #Em caso de nenhuma mensagem ser recebida, encerra a função
                break
        except:
             #Em caso de erro, encerra a função
            break

#Função para enviar respostas do gerente para os clientes: permite ao gerente enviar respostas continuamente até que ele envie "concluido1234", que finaliza a conexão.
def send_messages(manager_socket):
    while True:
        #Solicitação para que o gerente insira a resposta
        response = input("Digite sua resposta: ")
        manager_socket.send(response.encode())
        #Encerramento da função se a resposta for "concluido1234"
        if response == "concluido1234":
            break

#Função principal para iniciar a conexão do gerente com a área de suporte escolhida: exibe um menu para o gerente selecionar a área que ele deseja gerenciar e se conecta ao servidor correspondente.
def start_manager():
    print("Escolha a área de suporte que você gerenciará:")
    print("1. Financeiro")
    print("2. Logística")
    print("3. Atendimento")
    area_choice = input("Digite o número da área: ")

    #Definição das áreas e portas correspondentes
    areas = {"1": ("Financeiro", 5555), "2": ("Logistica", 5556), "3": ("Atendimento", 5557)}
    area, port = areas.get(area_choice, (None, None))

    #Validação da escolha da área
    if area is None:
        print("[Erro] Escolha inválida.")
        return

    #Criação e conecção do socket do gerente à área escolhida
    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.connect(('localhost', port))
    manager_socket.send("gerente".encode()) #Envio de uma identificação ao servidor

    print(f"\nVocê está gerenciando a área de {area}.\n")

    #Inicialização das threads para enviar e receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(manager_socket,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(manager_socket,))
    send_thread.start()

if __name__ == "__main__":
    #Inicialização do programa do gerente
    start_manager()
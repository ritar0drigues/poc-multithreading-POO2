import socket
import threading

#Função para recebimento de mensagens do servidor: loop contínuo que escuta mensagens do servidor até que o evento 'stop_event' seja acionado. Se a mensagem for "Conexão encerrada.", finaliza a conexão.
def receive_messages(client_socket, stop_event):
    while not stop_event.is_set():
        try:
            #Recebimento da mensagem do servidor
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
                #Em caso do servidor encerrar a conexão, ativa o evento de parada
                if message == "Conexão encerrada.":
                    print("[Sistema] Conexão finalizada pelo servidor.")
                    stop_event.set()  
                    break
            else:
                #Se não houver recebimento, encerra a função
                break
        except:
            #Em caso de erro, encerra a função
            break

#Função para envio de mensagens do cliente para o servidor: permite ao usuário digitar perguntas até que o evento 'stop_event' seja acionado. Se a mensagem for "sair1234", finaliza a conexão.
def send_messages(client_socket, stop_event):
    while not stop_event.is_set():
        #Solicitação para que o usuário insira sua pergunta
        question = input("Digite sua dúvida (ou 'sair1234' para encerrar): ")
        client_socket.send(question.encode())
        #Encerramento da função se o usuário digitar "sair1234"
        if question == "sair1234":
            stop_event.set() 
            break

#Função para se conectar a uma área específica de suporte: conecta-se ao servidor na porta especificada e inicia threads para envio e recebimento de mensagens.
def connect_to_area(area, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    client_socket.send("cliente".encode()) #Envio de uma identificação ao servidor

    print(f"Conectado à área de {area}.")
    
    #Evento para sinalização que as threads devem parar
    stop_event = threading.Event()
    
    #Inicialização das threads para receber e enviar mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, stop_event))
    send_thread = threading.Thread(target=send_messages, args=(client_socket, stop_event))
    receive_thread.start()
    send_thread.start()

    #Aguardamento das duas threads finalizarem
    receive_thread.join()
    send_thread.join()
    client_socket.close()

#Função principal que exibe um menu para o usuário escolher a área de suporte: conecta-se à área escolhida ou permite encerrar o programa.
def start_client():
    while True:
        #Exibição das opções de área de suporte
        print("\nEscolha a área de suporte que deseja acessar:")
        print("1. Financeiro")
        print("2. Logística")
        print("3. Atendimento")
        print("4. Sair do programa")
        area_choice = input("Digite o número da área: ")

        #Definição das áreas e portas correspondentes
        areas = {"1": ("Financeiro", 5555), "2": ("Logistica", 5556), "3": ("Atendimento", 5557)}
        area, port = areas.get(area_choice, (None, None))

        if area is None:
            if area_choice == "4":
                print("Encerrando o programa.")
                break #Encerramento do programa
            else:
                print("[Erro] Escolha inválida.")
                continue

        #Conecta-se à área selecionada
        connect_to_area(area, port)
        print(f"Desconectado da área de {area}. Voltando ao menu principal...\n")

if __name__ == "__main__":
    #Inicialização do cliente
    start_client()

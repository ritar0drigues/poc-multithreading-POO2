import socket
import threading

def receive_messages(client_socket, stop_event):
    while not stop_event.is_set():
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
                if message == "Conexão encerrada.":
                    print("[Sistema] Conexão finalizada pelo servidor.")
                    stop_event.set()  # Signal to stop
                    break
            else:
                break
        except:
            break

def send_messages(client_socket, stop_event):
    while not stop_event.is_set():
        question = input("Digite sua dúvida (ou 'sair1234' para encerrar): ")
        client_socket.send(question.encode())
        if question == "sair1234":
            stop_event.set()  # Signal to stop
            break

def connect_to_area(area, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    client_socket.send("cliente".encode())

    print(f"Conectado à área de {area}.")
    
    # Event to signal threads to stop
    stop_event = threading.Event()
    
    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, stop_event))
    send_thread = threading.Thread(target=send_messages, args=(client_socket, stop_event))
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()
    client_socket.close()

def start_client():
    while True:
        print("\nEscolha a área de suporte que deseja acessar:")
        print("1. Financeiro")
        print("2. Logística")
        print("3. Atendimento")
        print("4. Sair do programa")
        area_choice = input("Digite o número da área: ")

        areas = {"1": ("Financeiro", 5555), "2": ("Logistica", 5556), "3": ("Atendimento", 5557)}
        area, port = areas.get(area_choice, (None, None))

        if area is None:
            if area_choice == "4":
                print("Encerrando o programa.")
                break
            else:
                print("[Erro] Escolha inválida.")
                continue

        # Connect to the selected area
        connect_to_area(area, port)
        print(f"Desconectado da área de {area}. Voltando ao menu principal...\n")

if __name__ == "__main__":
    start_client()

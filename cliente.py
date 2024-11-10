import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print("\n[Servidor]:", message)
            else:
                break
        except:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.send("cliente".encode())  # Informando ao servidor que é um cliente

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        print("\nEscolha uma área de suporte:")
        print("1. Financeiro")
        print("2. Logística")
        print("3. Atendimento")
        area_choice = input("Digite o número da área desejada: ")

        areas = {"1": "Financeiro", "2": "Logistica", "3": "Atendimento"}
        area = areas.get(area_choice, "Invalido")
        
        if area == "Invalido":
            print("[Erro] Escolha inválida. Tente novamente.")
            continue
        
        question = input("Digite sua dúvida: ")
        client_socket.send(f"{area}: {question}".encode())

if __name__ == "__main__":
    start_client()

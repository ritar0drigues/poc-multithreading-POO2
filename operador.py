import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
                if message == "Conexão encerrada.":
                    print("[Sistema] Conexão finalizada pelo servidor.")
                    break
            else:
                break
        except:
            break

def send_messages(client_socket):
    while True:
        question = input("Digite sua dúvida: ")
        client_socket.send(question.encode())
        if question == "concluido1234":
            break

def start_client():
    print("Escolha a área de suporte que deseja acessar:")
    print("1. Financeiro")
    print("2. Logística")
    print("3. Atendimento")
    area_choice = input("Digite o número da área: ")

    areas = {"1": ("Financeiro", 5555), "2": ("Logistica", 5556), "3": ("Atendimento", 5557)}
    area, port = areas.get(area_choice, (None, None))

    if area is None:
        print("[Erro] Escolha inválida.")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    client_socket.send("cliente".encode())

    print(f"Conectado à área de {area}.")
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()

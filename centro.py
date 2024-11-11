import socket
import threading

def receive_messages(manager_socket):
    while True:
        try:
            message = manager_socket.recv(1024).decode()
            if message:
                print(f"\n{message}")
                if message == "Conexão encerrada.":
                    print("[Sistema] Conexão finalizada pelo servidor.")
                    break
            else:
                break
        except:
            break

def send_messages(manager_socket):
    while True:
        response = input("Digite sua resposta: ")
        manager_socket.send(response.encode())
        if response == "concluido1234":
            break

def start_manager():
    print("Escolha a área de suporte que você gerenciará:")
    print("1. Financeiro")
    print("2. Logística")
    print("3. Atendimento")
    area_choice = input("Digite o número da área: ")

    areas = {"1": ("Financeiro", 5555), "2": ("Logistica", 5556), "3": ("Atendimento", 5557)}
    area, port = areas.get(area_choice, (None, None))

    if area is None:
        print("[Erro] Escolha inválida.")
        return

    manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    manager_socket.connect(('localhost', port))
    manager_socket.send("gerente".encode())

    print(f"\nVocê está gerenciando a área de {area}.\n")
    receive_thread = threading.Thread(target=receive_messages, args=(manager_socket,))
    receive_thread.start()
    send_thread = threading.Thread(target=send_messages, args=(manager_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_manager()
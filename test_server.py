import pytest
import socket
import threading
from server import Server

TEST_PORT = 6000
TEST_AREA = "TestArea"

@pytest.fixture
def setup_server():
    """Configuração do servidor para o teste."""
    server_thread = threading.Thread(target=Server.start_area_server, args=(TEST_AREA, TEST_PORT), daemon=True)
    server_thread.start()
    yield
    server_thread.join(timeout=0.5)  # Timeout para evitar travamento

def create_client(role, message=None):
    """Cria um cliente socket simulando gerente ou cliente."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)  # Timeout para evitar travamentos
    client_socket.connect(('localhost', TEST_PORT))
    client_socket.send(role.encode())  # Envia o papel (gerente ou cliente)
    if message:
        client_socket.send(message.encode())
    return client_socket

def test_message_exchange(setup_server):
    """Teste de troca de mensagens entre cliente e gerente."""
    manager = create_client("gerente")
    client = create_client("cliente")
    
    # Cliente envia mensagem
    client.send("Teste de mensagem do cliente".encode())
    client_response = client.recv(1024).decode()
    assert "Sua dúvida foi enviada" in client_response

    # Gerente responde
    manager.send("Resposta do gerente".encode())
    manager_response = manager.recv(1024).decode()
    assert "Teste de mensagem do cliente" in manager_response


def test_shutdown_server(setup_server):
    """Teste de encerramento do servidor."""
    control_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_client.connect(('localhost', TEST_PORT))
    control_client.send("shutdown_server".encode())  # Envia o comando especial
    control_client.close()

def test_client_disconnect(setup_server):
    """Teste de desconexão do cliente."""
    client = create_client("cliente")
    client.send("Teste de mensagem do cliente".encode())
    client.send("concluido1234".encode())  # Comando para encerrar conexão
    response = client.recv(1024).decode()
    assert "[Erro] Nenhum gerente disponível para TestArea no momento." in response
    client.close()

def test_manager_disconnect(setup_server):
    """Teste de desconexão do gerente."""
    manager = create_client("gerente")
    manager.send("Teste inicial do gerente".encode())
    manager.send("concluido1234".encode())  # Comando para encerrar conexão
    response = manager.recv(1024).decode()
    assert "" in response
    manager.close()

def test_no_manager_available(setup_server):
    """Teste de mensagem de erro quando não há gerente disponível."""
    client = create_client("cliente")
    client.send("Mensagem sem gerente disponível".encode())
    response = client.recv(1024).decode()
    assert "[Erro] Nenhum gerente disponível" in response
    client.close()

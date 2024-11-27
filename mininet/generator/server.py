import socket

# Wybierz TCP lub UDP
PROTOCOL = 'UDP'  # Zmień na 'TCP', jeśli chcesz używać TCP
HOST = '0.0.0.0'  # Nasłuchuj na wszystkich interfejsach
PORT = 12345

if PROTOCOL == 'TCP':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Serwer TCP nasłuchuje na porcie {PORT}...")
    conn, addr = server.accept()
    print(f"Połączono z {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Otrzymano: {data.decode()}")
    conn.close()
elif PROTOCOL == 'UDP':
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Serwer UDP nasłuchuje na porcie {PORT}...")
    while True:
        data, addr = server.recvfrom(1024)
        print(f"Otrzymano: {data.decode()} od {addr}")

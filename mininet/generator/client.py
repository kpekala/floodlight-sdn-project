import socket
import time
import threading
import keyboard  # pip install keyboard

# Wybierz TCP lub UDP
PROTOCOL = 'UDP'  # Zmień na 'TCP', jeśli chcesz używać TCP
SERVER_IP = '10.0.0.1'  # Adres IP serwera (zmień na adres h1 w Mininecie)
PORT = 12345

def send_packets(client, packet_prefix, delay=1):
    """Funkcja wysyłająca pakiety w nieskończoność."""
    packet_number = 1
    try:
        while True:
            message = f"{packet_prefix} {packet_number}"
            if PROTOCOL == 'UDP':
                client.sendto(message.encode(), (SERVER_IP, PORT))
            elif PROTOCOL == 'TCP':
                client.send(message.encode())
            print(f"Wysłano: {message}")
            packet_number += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\nPrzerwano wysyłanie pakietów.")

def burst_packets(client, packet_prefix, burst_size=100):
    """Funkcja wysyłająca serię pakietów po wywołaniu."""
    for i in range(burst_size):
        message = f"{packet_prefix} B{str(i+1).zfill(3)}"
        if PROTOCOL == 'UDP':
            client.sendto(message.encode(), (SERVER_IP, PORT))
        elif PROTOCOL == 'TCP':
            client.send(message.encode())
        print(f"Wysłano (burst): {message}")

# Główna funkcja klienta
if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if PROTOCOL == 'UDP' else socket.SOCK_STREAM)
    if PROTOCOL == 'TCP':
        client.connect((SERVER_IP, PORT))
    print(f"Rozpoczęto wysyłanie pakietów do {SERVER_IP}:{PORT}")

    # Uruchom podstawowy ruch w osobnym wątku
    threading.Thread(target=send_packets, args=(client, "Pakiet", 1), daemon=True).start()

    print("Naciśnij Ctrl + Shift + R, aby uruchomić dodatkowy ruch (burst 100 pakietów).")
    
    try:
        while True:
            if keyboard.is_pressed("ctrl+shift+r"):
                print("\nUruchamianie dodatkowego ruchu!")
                burst_packets(client, "Dodatkowy")
                time.sleep(1)  # Chwila przerwy, aby uniknąć wielokrotnego uruchomienia
    except KeyboardInterrupt:
        print("\nZakończono działanie klienta.")
    finally:
        client.close()
        print("Socket zamknięty.")

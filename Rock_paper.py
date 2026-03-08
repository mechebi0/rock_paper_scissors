import socket
import threading


# Receive thread: Listens for messages from server
def receive_messages(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"\n[Server {addr[0]}:{addr[1]}]: {message}")
        except Exception as e:
            print(f"Receive error: {e}")
            break


# Send thread: User inputs messages to send to server
def send_messages(sock, server_addr):
    while True:
        try:
            message = input("\nYou (Client): ")
            if message.lower() == 'quit':
                break
            sock.sendto(message.encode('utf-8'), server_addr)
        except Exception as e:
            print(f"Send error: {e}")
            break


# Main client logic
if __name__ == "__main__":
    server_ip = input("Enter Server IP: ")
    server_port = int(input("Enter Server Port: "))
    server_addr = (server_ip, server_port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Client connecting to {server_ip}:{server_port}")

    # Send first message to "connect"
    initial_message = "Client connected!"
    sock.sendto(initial_message.encode('utf-8'), server_addr)

    # Start threads for continuous chat
    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    send_thread = threading.Thread(target=send_messages, args=(sock, server_addr))

    receive_thread.daemon = True
    send_thread.daemon = True
    receive_thread.start()
    send_thread.start()

    # Keep main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nClient shutting down.")
        sock.close()
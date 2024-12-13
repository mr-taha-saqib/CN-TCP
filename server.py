import socket
import os

def main():
    # Server setup
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5001))  # Bind to all interfaces on port 5001
    server.listen(5)
    print("Server listening on port 5001")

    while True:
        conn, addr = server.accept()
        print(f"Client connected from {addr}")

        filename = conn.recv(1024).decode()  # Receive the filename from the client
        print(f"Requested file: {filename}")

        if os.path.isfile(filename):
            conn.send(b"EXISTS " + str(os.path.getsize(filename)).encode())  # Send file size
            with open(filename, 'rb') as f:
                bytes_to_send = f.read(1024) 
                while bytes_to_send:
                    conn.send(bytes_to_send)  # Send chunk to client
                    bytes_to_send = f.read(1024)
            print("File transfer complete.")
        else:
            conn.send(b" File not found unfortunately.")  # Send error message if file doesn't exist
        conn.close() 

if __name__ == "__main__":
    main()
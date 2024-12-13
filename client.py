import socket
import time

def main():
    # Client setup
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5001))  # Connect to the server on localhost and port 5001

    filename = input("File to download: ")
    client.send(filename.encode())  # Send filename to the server

    response = client.recv(1024).decode()  # Receive response from server
    if response.startswith("EXISTS"):
        filesize = int(response.split()[1])  # Get file size from response
        print(f"File found. Size: {filesize} bytes")

        with open('downloaded_' + filename, 'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                bytes_data = client.recv(1024)  
                if not bytes_data:
                    break
                f.write(bytes_data)  
                bytes_received += len(bytes_data)

                # Print the contents of the received data (assuming it's text)
                print(bytes_data.decode(errors='ignore'), end='') 

                time.sleep(2)  

        print("\nFile downloaded successfully.")
    else:
        print(response)  # Print error message if file not found

    client.close()  # Close connection with the server

if __name__ == "__main__":
    main()
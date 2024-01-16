# client.py
import socket
import time

def extract_content_within_quotes(command):
    start_index = command.find('"')
    end_index = command.rfind('"')

    if start_index != -1 and end_index != -1:
        return command[start_index + 1:end_index]
    else:
        return ""


def msgToRequest(msg):
    attr_list = msg.split(' ')
    cmd = attr_list[0]
    method = ""
    url = ""
    request_body = ""

    if cmd == "echo":
        # Extract content within double quotes
        content_within_quotes = extract_content_within_quotes(msg)

        # Create request body for the "echo" command
        request_body = f'{{"content": "{content_within_quotes}"}}'
        method = "PUT"
        url = attr_list[-1]
    elif cmd == "ls":
        method = "GET"
    elif cmd == "more":
        method = "GET"
        url = attr_list[1]
    elif cmd == "rm":
        method = "DELETE"
        url = attr_list[1]
    else:
        method = "FOO"

    return f"""{method} /{url} HTTP/1.0\r\nHost: 127.0.0.1:8080\r\n\r\n{request_body}"""



if __name__ == "__main__":
    try:
        # Client configuration
        HOST, PORT = "127.0.0.1", 8080

        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((HOST, PORT))

                # Send a request to the server
                msg = input("Please Command: ")
                request = msgToRequest(msg)
                print(request)
                client_socket.sendall(request.encode('utf-8'))

                # Receive and print the response from the server
                response = client_socket.recv(1024).decode('utf-8')
                print("Received response:", response)

            # Pause for 2 seconds before allowing another iteration
            time.sleep(2)

    except ConnectionResetError as e:
        print(e)
    except Exception as e:
        print(e)
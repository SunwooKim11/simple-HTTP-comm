# server.py
import socket
import os
import json
import time

# method to deal with Put request
def put_data(query, request_body):
    try:
        request_body = json.loads(request_body)
        new_content = request_body['content']

        BASEDIR = os.getcwd()
        if BASEDIR.find("db") <0:
            BASEDIR+="/db"
        PATH = BASEDIR + query + ".txt"

        print(BASEDIR, query)
        print(PATH)
        # if 'query' exists in db. Update content.
        # if not, Create new file, of which name is 'query'.
        #   And it has a content from request_body.
        if os.path.isfile(PATH):
            status = "200 OK"
        else:
            status = "201 Created"

        with open(PATH, 'w') as f:
            f.write(new_content)

        return status, str(new_content)

    except Exception as e:
        return "500 Internal Server Error" , str(e)

# method to deal with Delete request
def delete_data(query):
    try:
        BASEDIR = os.getcwd()
        if BASEDIR.find("db") <0:
            BASEDIR+="/db"
        PATH = BASEDIR + query + ".txt"

        print(BASEDIR, query)
        print(PATH)

        if os.path.isfile(PATH):
            content = ""
            with open(PATH, 'rt') as f:
                content = f.readlines()
            os.remove(PATH)
            return "200 OK", content
        else:
            return "404 Not Found", ""
    except Exception as e:
        return "500 Internal Server Error", str(e)
# method to deal with Get request
def read_data(query):
    try:
        BASEDIR = os.getcwd()
        if BASEDIR.find("db") <0:
            BASEDIR+="/db"
        PATH = BASEDIR + query
        print(BASEDIR)
        print(query)
        # if client cmd == 'ls', to see file list of db
        if query == "/":
            # https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
            os.chdir(PATH)
            dic_info = filter(os.path.isfile, os.listdir(PATH))
            dic_info = [os.path.basename(f) for f in dic_info]  # Extract only file names
            dic_info.sort(key=lambda x: os.path.getmtime(os.path.join(PATH, x)))
            for i in range(len(dic_info)):
                mtime = str(time.ctime(os.path.getmtime(os.path.join(PATH,dic_info[i]))))
                dic_info[i] = mtime + " " + dic_info[i]
            print(dic_info)

            # Format the response for "ls" command
            response_body = '\n'.join(dic_info)

            return "200 OK", response_body

        # if client cmd == 'more', to see content in the file.
        PATH += '.txt'
        if os.path.isfile(PATH):
            with open(PATH, 'rt') as f:
                response_body = ''.join(f.readlines())

            return "200 OK", response_body
        else:
            return "404 Not Found", ""
    except Exception as e:
        return "500 Internal Server Error: " + str(e), ""


def handle_request(request):
    try:
        # Extract method path from the request
        tmp = request.split('\r\n')
        method = tmp[0].split(' ')[0]
        query = tmp[0].split(' ')[1]
        request_body = tmp[-1]
        status = ""
        response_body = ""

        if method == "GET":
            status, response_body = read_data(query)
        elif method == "DELETE":
            status, response_body = delete_data(query)
        elif method == "PUT":
            status, response_body = put_data(query, request_body)
        else:
            status, response_body = "400 Bad Request", ""

        # Return the formatted response
        return f'HTTP/1.1 {status}\r\n\r\n{response_body}'
    except IndexError:
        status, response_body = "400 Bad Request", ""
        return f'HTTP/1.1 {status}\r\n\r\n{response_body}'



if __name__ == "__main__":
    try:
        # Server configuration
        HOST, PORT = "127.0.0.1", 8080

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen(1)
            print(f"Server listening on {HOST}:{PORT}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")

                try:
                    # Receive data from the client
                    request = client_socket.recv(1024).decode('utf-8')
                    print("Received request:", request)

                    # Process the request and generate a response
                    response = handle_request(request)

                    # Send the response back to the client
                    print(response)
                    client_socket.send(response.encode('utf-8'))

                except BrokenPipeError:
                    print("Client disconnected unexpectedly.")

                finally:
                    # Close the connection with the client
                    client_socket.close()
                    # break  # Break out of the server loop after handling one request

    except ConnectionResetError as e:
        print(e)
    except Exception as e:
        print(e)
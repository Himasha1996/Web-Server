import socket
import threading


HOST, PORT = '127.0.0.1', 8080
directory = 'kelly'

H_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

print("<<<<<<<<<< WEB SERVER >>>>>>>>>>")
def run():
    try:
        print(str(HOST) + ":" + str(PORT) + " is starting")
        H_Socket.bind((HOST,PORT))
        print("Server is started")
        connection()

    except OSError:
        print("Sorry, Host and/or port already in use")
        shutdown()

def shutdown():
    try:
        print("Shutting down the server")
        H_Socket.shutdown(socket.SHUT_RDWR)  
    except Exception:
        print("Shut down can not be done")
        
def connection():
    print ("Waiting for New connection")
    H_Socket.listen(3)  # 3 invalid connections before termination
    while True:
        (conn, addr) = H_Socket.accept()
        print("client - ", conn)
        print("address - ", addr)
         # conn - socket to client
         # addr - client's address
        print("Got connection from:", addr)
 
        threading.Thread(target=RequestHandler, args=(conn,)).run()  
       
def RequestHandler(conn):
    while True:
        try:
            request = conn.recv(1024).decode()
            if not request:
                break
        except Exception as e:
            print("Request timed out")
            break
        print(request)

        try:
            requestedFile = request.split(' ')[1]
            requestedFile = requestedFile.split('?')[0]

            if requestedFile == "/":
                requestedFile = "/index.html"  # load index file as default

            file_path = directory + requestedFile
            file_type = requestedFile.split('.')[1]

            file = open(file_path, 'rb')
            response= file.read()
            file.close()
            
            header = gen_headers(200, file_type)

        except FileNotFoundError:
            header = gen_headers(404, file_type)
            response = b"Error 404 - File Not Found"
        except UnboundLocalError as e:  
            print(e)
            header = gen_headers(400, '')
            response= b"Malformed request"
        except IndexError as e:  # no extension
            print("Requested ")
            header = gen_headers(400, '')
            response= b"Malformed request"
        

        r = header.encode()
        r += response

        conn.sendall(r)
        conn.close()
        break

def gen_headers(code, file_type):   # code - response code

    h = ''    # h = header
    if code == 200:
        h += 'HTTP/1.1 200 OK\n'
    elif code == 404:
        h += 'HTTP/1.1 404 Not Found\n'
    elif code == 400:
        h += 'HTTP/1.1 400 Bad Request\n'

    if file_type == 'jpg' or file_type == 'jpeg':
        h += 'Content-Type: image/jpeg\n'
    elif file_type == 'htm' or file_type == 'html':
        h += 'Content-Type: text/html\n'
    elif file_type == 'png':
        h += 'Content-Type: image/png\n'
    elif file_type == 'js':
        h += 'Content-Type: text/js\n'
    elif file_type == 'css':
        h += 'Content-Type: text/css\n'
    elif file_type == 'mp4':
        h += 'Content-Type: video/mpeg \n'


    h += 'Connection: close\n\n'
    return h


run()  # Calling run function to run the server

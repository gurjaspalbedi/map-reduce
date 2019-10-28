import sys
import socket

#REFERENCES
#https://realpython.com/python-csv/
#https://realpython.com/python-sockets/
#https://cs.lmu.edu/~ray/notes/pythonnetexamples/
#https://realpython.com/read-write-files-python/
#https://realpython.com/python-sockets/

#AF_INET - IPv4 and SOCK_STREAM - TCP
def mem_client(multiclient = False, something = True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connecting to the server at port 9899
        sock.connect(('localhost', 9899))
        if not multiclient:
            print('Operations you can do\n 1. set <key> <size>\n <pyaload>\n 2. get <KEY>\n')
        # Client kept alive for multiple get and set requests
        while True:
            
            line = sys.stdin.readline()
            if not line:
                break
          
            sock.sendall(f'{line}'.encode('utf-8'))
            while True:
                data = sock.recv(1024)
                print(data.decode("utf-8"), end='')
                if len(data) < 1024:
                    break
if __name__ == "__main__":
    mem_client()
import sys, socket, selectors

def read(soc):
    data = soc.recv(10000)
    print(data.decode().strip("\n"))

def send(d):
    data = d.readline()
    s.sendall(data.encode())

HOST, PORT = sys.argv[1],  int(sys.argv[2])

sel = selectors.DefaultSelector()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(False)
sel.register(sys.stdin, selectors.EVENT_READ, send)
sel.register(s, selectors.EVENT_READ, read)

while True:
    events = sel.select()
    for key, mask in events:
        key.data(key.fileobj)

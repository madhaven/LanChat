from threading import Thread, Lock
from socket import *
from time import ctime
lock=Lock()
termcode='TERMINATE'
checkstr='tryzSOCKTEST'
defport=45565

class server(Thread):
    def __init__(self, *args): #first argument be port to host server
        #initialize stuff
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.clients=[]
        #selecting a port
        if len(args)==0:
            for x in range(45565, 55565):
                try:
                    self.sock.bind(('', x))
                    break
                except Exception as e: pass#print(e)
                finally: self.port=x
        if len(args)==1:
            self.port=args[0]
            self.sock.bind((gethostbyname(gethostname()), self.port))
        with lock: print('\nConnect client to \n IP : %s\nport: %d'%(gethostbyname(gethostname()), self.port))
    def run(self):
        message=''
        while True:
            #print('entered server loop')###'''
            data, addr=self.sock.recvfrom(1024)###
            #print('received message')###'''
            if str(data)[2:2+len(checkstr)]==checkstr:
                #print('checkstring detected')###'''
                self.sock.sendto(bytes(checkstr, 'utf-8'), addr)
                #with lock: print('checkfrom', addr)###'''
                continue
            elif addr not in self.clients:
                #print('address registration')###'''
                self.clients.append(addr)
                message=ctime()[11:-5]+' : CONNECTED < '+str(data)[2:-1]+' '+str(addr)###'''
                with lock: print(message)
            elif str(data)[2:2+len(termcode)]==termcode:
                #print('termcode detected')###'''
                self.clients.remove(addr)
                message=ctime()[11:-5]+' : DISCONNECTED < '+str(data)[3+len(termcode):-1]+' '+str(addr)###
                with lock:
                    print(message)
                    #print(self.clients)
            else:
                #print('allgood4')###'''
                message=ctime()[11:-5]+' : '+str(data)[2:-1]#+' '+str(addr)###'''
                with lock: print(message)
            try:
                #print('broadcasting messages')###'''
                for x in self.clients:
                    if x != addr:
                        self.sock.sendto(bytes(message, 'utf-8'), (x[0], x[1]+1))#initiate hostclient thread to send messages to clients.
            except Exception as e:print(e)
            if not self.clients: break;
        self.sock.close()

class clientserver(Thread):
    def __init__(self, *args):#argument one to be port
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.sock.bind((args[0], args[1]))
        #print('clientserver initialized')
    def run(self):
        while True:
            data, addr=self.sock.recvfrom(1024)
            with lock: print(str(data)[2:-1])
            
class client(Thread):
    def __init__(self, *args): #first argument be tuple with ip and port
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.username=input('Select a username : ')
        if len(args)==0:
            self.ip=input('Enter host\'s ip : ')
            if not self.ip:
                self.sock.close()
                exit()
            self.port=None            
            for x in range(45565, 55565):
                #input('all fine ?')
                if servexists(self.sock, self.ip, x, username=self.username, timeout=0.5):
                    self.port=x;
                    #print('PORT SELECTED')###
                    break
        if len(args)==1: self.ip, self.port=args[0][0], args[0][1]
        #print('ip and port :', self.ip, self.port);input()
        self.sock.sendto(bytes(self.username, 'utf-8'), (self.ip, self.port))
    def run(self):
        #print('Connect host to \n IP : %s\nport: %d ...'%(gethostbyname(gethostname()), self.sock.getsockname()[1]+1))###
        self.listener=clientserver(gethostbyname(gethostname()), self.sock.getsockname()[1]+1)
        self.listener.start()
        while True:
            data=input()
            if not data:
                #print("no data detected : ")###
                self.sock.sendto(bytes(termcode+' '+self.username, 'utf-8'), (self.ip, self.port))
                break;
            else: self.sock.sendto(bytes(data+' < '+self.username, 'utf-8'), (self.ip, self.port))
        #print("waiting for clientserver thread termination")###
        self.listener.join(2)
        #print('clienserver terminated')###
        self.sock.close()
    
def servexists(clientsock, ip, port, username='anonymous', timeout=1):
    clientsock.sendto(bytes(checkstr+' '+username, 'utf-8'), (ip, port))
    clientsock.settimeout(timeout)
    if str(clientsock.recvfrom(1024)[0])[2:-1]==checkstr:
        #print('servexists@'+str(port));input()###
        return True
    #print('serverdontexst@'+str(port));input()###
    return False

try:
    if '1' in input('1. Begin conversation\n2. Join conversation\n\n'): x=server();x.start()
    else: x=client();x.start()
    x.join()
    close()
except Exception as e:
    print('\nAn error has occured.\n', e, '\nContact @_mad_haven', sep='')
    input()

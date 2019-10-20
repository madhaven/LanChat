from threading import Thread, Lock
from socket import *
from time import ctime, sleep
from os import system
lock=Lock()
termcode='TERMINATE'
checkstr='TryzSOCKTEST'
defport=45565

class server(Thread):
    def __init__(self, *args): #first argument be port to host server
        #initialize stuff
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.clients=[] #all messages to server would be forwarded to all the clients saved in this list
        
        #selecting a port
#        if len(args)==0:
        for x in range(45565, 55565):
            try:
                self.sock.bind(('', x))
                self.port=x
                break
            except Exception as e: pass#print(e)
#        if len(args)==1:
#            self.port=args[0]
#            self.sock.bind(('', self.port))
        with lock: print('Connect to Master IP : %s'%gethostbyname(gethostname()))#, self.port))
    def run(self):
        serverclient=client(gethostbyname(gethostname()), self.port).start() #starts a client for the master user as well
        message=''
        while True:
#            print('entered server loop')###'''
            data, addr=self.sock.recvfrom(1024)
#            print('received message')###'''
            if str(data)[2:2+len(checkstr)]==checkstr: #for client initialization and confirmation
#                print('checkstring detected')###'''
                self.sock.sendto(bytes(checkstr, 'utf-8'), addr)
                #with lock: print('checkfrom', addr)###'''
                continue
            elif addr not in self.clients:
#                print('address registration')###'''
                self.clients.append(addr)
                message=ctime()[11:-5]+' : CONNECTED < '+str(data)[2:-1]+' '+str(addr)###'''
#                with lock: print(message)
            elif str(data)[2:2+len(termcode)]==termcode: #when users leave
#                print('termcode detected')###'''
                self.clients.remove(addr)
                message=ctime()[11:-5]+' : DISCONNECTED < '+str(data)[3+len(termcode):-1]+' '+str(addr)###
#                with lock:print(message);#print(self.clients)
            else:
                message=ctime()[11:-5]+' : '+str(data)[2:-1]#+' '+str(addr)###'''
#                with lock: print(message)
            try:
#                print('broadcasting messages')###'''
                for x in self.clients:
                    if x != addr:
                        self.sock.sendto(bytes(message, 'utf-8'), (x[0], x[1]+1))#initiate hostclient thread to send messages to clients.
            except Exception as e:print('Error while broadcast', e)
            self.sock.close()
            self.sock=socket(2, 2)
            self.sock.bind(('', self.port))
            if not self.clients: break;
        try: serverclient.join(1.0)
        except: pass
        try: self.sock.close()
        except: pass

class clientserver(Thread):
    def __init__(self, *args):#argument one to be port
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.sock.bind(('', args[0]))
#        print('clientserver initialized : ', gethostbyname(gethostname()), args[0])
    def run(self):
        while True:
            data, addr=self.sock.recvfrom(1024)
            if str(data)[2:2+len(termcode)]==termcode: break
            with lock: print(str(data)[2:-1])
        self.sock.close()
            
class client(Thread):
    def __init__(self, *args): #first argument be ip and port
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.username='admin'#input('Select a username : ')
        print('\nHello %s, Send messages to the network now. Send a blank text to Exit.\n'%self.username)
        if len(args)==1: self.ip=args[0]
        if len(args) in [0, 1]:
            for x in range(45565, 55565):
                #input('all fine ?')
                if servexists(self.sock, self.ip, x, username=self.username, timeout=0.5):
                    self.port=x;
                    #print('PORT SELECTED')###
                    break
        if len(args)==2: self.ip, self.port=args[0], args[1]
        #input('ip and port :', self.ip, self.port)
        system('title LANCHAT '+self.username+'@'+self.ip+':'+str(self.port))
        self.sock.sendto(bytes(self.username, 'utf-8'), (self.ip, self.port))
    def run(self):
        #print('Connect host to \n IP : %s\nport: %d ...'%(gethostbyname(gethostname()), self.sock.getsockname()[1]+1))###
        self.listener=clientserver(self.sock.getsockname()[1]+1)
        self.listener.start()
        while True:
            data=input()
            if not data:
                #print("no data detected : ")###
                self.sock.sendto(bytes(termcode+' '+self.username, 'utf-8'), (self.ip, self.port))
                break;
            else: self.sock.sendto(bytes(data+' < '+self.username, 'utf-8'), (self.ip, self.port))
        #print("waiting for clientserver thread termination")###
        self.sock.sendto(bytes(termcode, 'utf-8'), (gethostbyname(gethostname()), self.sock.getsockname()[1]+1))
        self.listener.join(1.0)
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
#    servorclient = input('Enter ip of Master\nPress Enter to start Master on this system\n')
#    if servorclient =='': 
    x=server('admin');x.start()
#    else: x=client(servorclient);x.start()
    x.join()
except Exception as e:
    print('\nAn error has occured.\n', e, '\nContact @_mad_haven', sep='')
    input()

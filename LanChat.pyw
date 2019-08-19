try:
    from tkinter import *
    from tkinter import messagebox, simpledialog
except:
    input('It appears, Tkinter Graphics is not installed into the python path. Please use the CLI version of this program.')
    exit()
from threading import Thread, Lock
from socket import *
from time import ctime, sleep
from os import system
lock=Lock()
termcode='TERMINATE'
checkstr='TryzSOCKTEST'
defport=45565
printqueue=[]

class server(Thread):#manages all messages
    def __init__(self, *args): #first argument be port to host server
        #initialize stuff
        Thread.__init__(self)
        self.sock=socket(2, 2)
        self.clients=[] #all messages to server would be forwarded to all the clients saved in this list
        self.daemon=True;
        
        #selecting a port
        if len(args)==0:
            for x in range(45565, 55565):
                try:
                    self.sock.bind(('', x))
                    self.port=x
                    break
                except Exception as e: pass#print(e)
        if len(args)==1:
            self.port=args[0]
            self.sock.bind(('', self.port))
        self.CONNECTTOTHISIP=gethostbyname(gethostname())
    def run(self):
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
#                self.sock.sendto(bytes(self.clients, 'utf-8'), addr)
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
        
def servexists(clientsock, ip, port, username='anonymous', timeout=1):
    clientsock.sendto(bytes(checkstr+' '+username, 'utf-8'), (ip, port))
    clientsock.settimeout(timeout)
    if str(clientsock.recvfrom(1024)[0])[2:-1]==checkstr: return True
    return False

class clientserver(Thread):
    def __init__(self, *args, root=None):#args=ip, master
        Thread.__init__(self)
        #Frame.__init__(self, root)
        self.port=args[0]
        self.root=root
#        print('clientserver initialized')
    def run(self):
        global printqueue
        while True:
            self.sock=socket(2, 2)
            self.sock.bind(('', self.port))
#            print('clientserver started')
            data, addr=self.sock.recvfrom(1024)
            self.sock.close()
            if str(data)[2:2+len(termcode)]==termcode: break
            printqueue.insert(0, str(data)[2:-1])
#            print(str(data)[2:-1])

class app(Frame):
    def __init__(self, root=None):
        self.root=root
        Frame.__init__(self, root)
        self.stuff()
    def output(self, st, color='grey', end='\n'):
#        print('IM RECEIVING SHIT')
        self.text1.config(state='normal')
        self.text1.insert(END, st+end)
        self.text1.config(state='disabled')
        self.text1.see('end')
        self.text2.focus()
    def checkqueue(self):
        global printqueue
        while printqueue:
            self.output(printqueue.pop())
#        self.output('IMAGINE QUEUE HAS BEEN OUTPUTTED')
#        messagebox.showinfo('TEST', 'OUT THE CHECKQUEUE LOOP')
        self.theafter=self.root.after(10, self.checkqueue)
    def thequit(self):
        try:self.sock.close();
        except:pass
        try:self.listener.join(1.0)
        except:pass
        try:self.theserver.join()
        except:pass
        self.destroy()
        quit()
    def clientinput(self, event):
        text=self.text2.get();
#        print('Enter detected :', text)
        self.text2.delete(0, len(text))
        self.output(text)
        if not text:
            self.sock.sendto(bytes(termcode+' '+self.username, 'utf-8'), (self.masterip,self.port))
            self.text2.config(state='disabled')
            #TERMINATE CLIENTSERVER
            self.sock.sendto(bytes(termcode, 'utf-8'), (gethostbyname(gethostname()), self.sock.getsockname()[1]+1))
            self.listener.join(1.0)
            self.root.after_cancel(self.theafter)
            self.sock.close()
            self.thequit()
        else: self.sock.sendto(bytes(text+' < '+self.username, 'utf-8'), (self.masterip, self.port))
        
    def stuff(self):
        self.root.title('LANCHAT')
        self.root.minsize(400, 100)
        self.top=Frame(self.root, background='grey')
        self.text2=Entry(self.root)
        self.text2.bind('<Return>', self.clientinput)

        self.text2.pack(side=BOTTOM, fill=BOTH, expand=False)
        self.top.pack(side=TOP, fill=BOTH, expand=True)

        self.text1=Text(self.top, background='grey')
        self.scroll=Scrollbar(self.top)
        self.text1.config(yscrollcommand=self.scroll.set)
        self.text1.config(state="disabled")
        self.scroll.config(command=self.text1.yview)

        self.text1.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll.pack(side=RIGHT, fill=Y)
        
    def themain(self):
        try:
            self.root.focus_set()
            servorclient=simpledialog.askstring('Configure Master', 'Enter IP of Master\nPress Enter to start Master on this system', parent=self.root)
            self.masterip=servorclient
            if servorclient==None: quit()
            elif servorclient=='':
                self.theserver=server();self.theserver.start()
                self.masterip=self.theserver.CONNECTTOTHISIP
                self.output('Connect to Master IP : %s'%self.masterip)
            self.sock=socket(2, 2)
            self.username=simpledialog.askstring('Username', 'Select a username', parent=self.root)
            messagebox.showinfo('', 'Hello %s, Send messages to the network now. Send a blank text to Exit.\n'%self.username)
            self.text2.focus_set()
            
            #select a port
            for x in range(45565, 55565):
                if servexists(self.sock, self.masterip, x, username=self.username, timeout=0.5):
                    self.port=x;
                    break
            self.root.title('LANCHAT '+self.username+'@'+self.masterip+':'+str(self.port))
            self.sock.sendto(bytes(self.username, 'utf-8'), (self.masterip, self.port))

#                INITIATE CLIIENTSERVER
#                print('yoma', gethostbyname(gethostname()), self.sock.getsockname()[1]+1, str(self))
#                messagebox.showinfo('TEST', 'BEFORE CLIENT SERVER INITIALIZATION')
            self.listener=clientserver(self.sock.getsockname()[1]+1, root=self)
#                messagebox.showinfo('TEST', 'AFTER CLIENTSERVER INITIALIZATION')
            self.listener.start()
#                messagebox.showinfo('TEST', 'CLIENTSERVER LISTENER STARTED')
            self.checkqueue()
#                messagebox.showinfo('TEST', 'CHECKING FOR PRINTQUEUE')
                
        except Exception as e:
            messagebox.showerror('Error', 'An error has occured.\n'+str(e)+'\nContact @_mad_haven')
#            print('bleh')
            quit()
try:
    theroot=Tk()
    th=app(theroot)
    th.themain()
    th.pack()
    theroot.mainloop()
    exit()
except Exception as e:print(e)

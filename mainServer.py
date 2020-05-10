import socket,random,threading,signal,os,sys
from _thread import *
import randomQuestions as rq,utilities as util,ClientHealthItems as chi

port=25000
userScore, pid, users = [ 0 for i in range(3)], [], []
clientThread = threading.Lock()
ans, i = [], 0

def Question(cs,l,i):
    playerInfo=cs.recv(1024)
    print('Online Users are :')
    user,pid,users=chi.clientHealth(util.legible(playerInfo))
    print(pid)
    print('Current thread name is : '+ str(threading.currentThread().getName())+'. The user ' +str(user)+ ' runs on port : ')
    if not playerInfo :
        print('BYE!! SEE YOU NEXT TIME :)')
        clientThread.release()
    player=int(threading.currentThread().getName())
    while True:
        for j in range(3):
            l[j].set()
        qa=rq.randQuestion(i)
        que,correctAnswer=qa[0],qa[1]
        print('Current thread name is : '+ str(threading.currentThread().getName())+". Question given is : " + que)
        print(ans)
        cs.send(str.encode(user+' has scored '+str(userScore[player])+'. Next question is : ')+str.encode(que))
        if(len(ans)==0):
            l[player].clear()
            for u in range(3):
                if u!=player :
                    l[u].wait()
            ans.append( util.legible(cs.recv(1024)))
            print('Answer received is : '+ ans[0])
            if(ans[0] == 'BUZZ'):
                print('Buzzer not pressed..')
            elif(ans[0] == 'NA'):
                print ('Current thread name is : '+ str(threading.currentThread().getName())+'.  No answer ')
            elif(ans[0] == correctAnswer):
                print ('Current thread name is : '+ str(threading.currentThread().getName())+'.  Correct answer ')
                userScore[player]+=1
            elif(ans[0] != correctAnswer):
                print ('Current thread name is : '+ str(threading.currentThread().getName())+'.  Wrong answer ')
                userScore[player]-=0.5
            ans.pop()
        if(max(userScore)>=5 or i>30):
            winner=users[userScore.index(max(userScore))]
            if (i > 30) or (userScore[0]==userScore[1] and userScore[0]==userScore[2]):
                cs.send(str.encode('Quiz is Tied!!'))
            else:
                cs.send(str.encode(' '+str(winner)+' won the game!'))
            for x in pid:
                try:
                    os.kill(x, signal.SIGUSR2)
                except ProcessLookupError:
                    print('GAME OVER')
                    return 
            return
        cs.send(str.encode(' You are playing..'))
        for x in pid:
            try:
                os.kill(x, signal.SIGUSR1)
            except ProcessLookupError:
                print('GAME OVER')
                return 
        i+=1

def quizLoop(i):
    server=socket.socket()
    try:
        server.bind(('',port))
        print('Server Connected to port : ',port)
    except:
        print('Oops :( Your port looks busy..')
        exit()
    server.listen(3)
    print('Server listens at port : ',port)
    addr=0
    t,c=[],[]
    while(True):
        cs,addr=server.accept()
        print('Connected to client at : ',str(addr))
        c.append(cs)
        print('The no. of clients connected are : ',str(len(c)))
        #clientThread.acquire()
        if(len(c)==3):
            l=[threading.Event() for i in range(3)]
            print(l)
            t.append(threading.Thread(target=Question,args=(c[0],l,i),name='0'))
            t.append(threading.Thread(target=Question,args=(c[1],l,i),name='1'))
            t.append(threading.Thread(target=Question,args=(c[2],l,i),name='2'))
            t[0].start()
            t[1].start()
            t[2].start()
            t[0].join()
            t[1].join()
            t[2].join()
            exit()
        print('The no. of threads are : ',str(len(t)))
        print('The thread IDs are : ',str(t))
quizLoop(i)

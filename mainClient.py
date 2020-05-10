import sys,socket,random,time,os,signal
import timing as t,utilities as util

userName=input('Enter your User Name : ')
serverName,serverPort='127.0.0.1',25000

userPort=random.choice([9800+i for i in range(500)])

def yes(userChoice):
    return userChoice.lower()=='yes'

def createQuestion(main):
    return ''.join(i for i in main)

def createOption(main):
    return ''.join(i for i in [main[j] for j in range(main.rfind('0')+1,len(main))])

def receive_signal(signum,stack):
    pass

def loser(signum,stack):
    pass

def winner(signum,stack):
    pass

def gameLoop():
    s=[]
    notQuit=True
    while(notQuit):
        print('Hi! '+userName+'. Do you want play the quiz? Enter a yes if you want to join the fun')
        userChoice=input()
        if not yes(userChoice):
            notQuit=False
            print('The game is over')
        else:
            client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((serverName,serverPort))
            print('Welcome to the Quiz!!')
            print('Ready'.title()),
            print('Get set'.title()),
            print('Answer'.title())
            client.send(str.encode(userName+' is running on process '+str(os.getpid())))
            i=0
            while(True):
                scores=[]
                main=util.legible(client.recv(42))
                print()
                print(createQuestion(main))
                print()
                print('Hit 1 for setting the buzzer within 10 seconds..')
                ans='BUZZ'
                if(t.buzzer()):
                    print('You pressed the buzzer')
                    ans='NA'
                    ans=t.ansWithinTime()
                    print('Your Answer is : ',ans)
                    if ans == 'NA':
                        print("Your time's up!!!Wait for the next question..")
                else:
                    print("#####YOUR TIME'S UP!!#####")
                client.send(str.encode(ans))
                print()
                finalResult=util.legible(client.recv(18))
                print(finalResult,flush=True)
                if(not ' You are playing..' in finalResult ):
                	exit()
signal.signal(signal.SIGUSR1, receive_signal)
signal.signal(signal.SIGUSR2, winner)

gameLoop()
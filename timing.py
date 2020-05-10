import sys,select

def buzzer():
    print('You have 10 seconds to press the buzzer..')
    i,o,e=select.select([sys.stdin], [], [], 10)
    if(i):
        return sys.stdin.readline().strip()
        #return 1
    else:
        return 0

def ansWithinTime():
    print('You have 10 seconds to give your answer..')
    i,o,e=select.select([sys.stdin], [], [], 10)
    if(i):
        return sys.stdin.readline().strip()
        #return 'ASD'
    else:
        return 'NA' 
import random

N=100

def randQuestion(i):
    pos=i
    question=str(N) + ' + '+ str(i)
    ans=str(N+i)
    return question,ans

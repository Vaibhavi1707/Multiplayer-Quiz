userPort,users=[],[]

def userName(playerInfo):
    return ''.join(i for i in [playerInfo[j] for j in range(playerInfo.find(' '))])

def clientPort(playerInfo):
    return int(''.join(i for i in [playerInfo[j] for j in range(playerInfo.rfind(' '),len(playerInfo))])) 

def clientHealth(playerInfo):
    user=userName(playerInfo)
    users.append(user)
    userPort.append(clientPort(playerInfo))
    return user,userPort,users
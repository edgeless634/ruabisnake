#!/usr/bin/env python
#-*- coding:utf8 -*-
import os
import time
import random
snake=[(3,1),(2,1),(1,1)]
dire=1
diretohanzi="右下左上"
#右 下 左 上
di=[0,1,0,-1] 
dj=[1,0,-1,0]
mplength,mpwidth=10,10
applei,applej=4,4
#mpchar="口回田果　"
mpchar=["\033[1;42m　\033[0m","\033[1;45m　","\033[1;44m　","\033[1;43m　","\033[1;47m　"]
showMpTime=0.016 #地图刷新的最短时间
clearCommand="cls" if os.name=="nt" else "clear"

def mptotype(i,j):
    if (i,j) in snake:
        return 1 if snake.index((i,j))==0 else 2 #snake's head jor body
    elif i==applei and j==applej:
        return 3 #apple
    elif min(i,j)<1 or i>mplength or j>mpwidth:
        return 0 #empty
    else:
        return 4 #air

def printmp():
    os.system(clearCommand)
    print(mpchar[0]*(mplength+2))
    for i in range(1,mplength+1):
        print(mpchar[0],end="")
        for j in range(1,mpwidth+1):
            print(mpchar[mptotype(i,j)],end="")
        print(mpchar[0])
    print(mpchar[0]*(mplength+2))

def stallForTime():
    '''
    在够不到果子的时候苟命
    基本思路:
    1.找到头部能够得到,且离尾部最近的身体
    2.计算那段身子到周围几个空位的距离
    3.往离那段身子最远的空位走(尽量贴墙)
    '''
    queue=[(0,0),snake[0]]
    queh=0
    target=(0,0)
    mxtarget=0
    while queh<len(queue)-1:
        queh+=1
        for i in range(4):
            nxti,nxtj=queue[queh][0]+di[i],queue[queh][1]+dj[i]
            if (nxti,nxtj) in queue or min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
                if (nxti,nxtj) in snake and mxtarget<snake.index((nxti,nxtj)):
                    target=(nxti,nxtj)
                    mxtarget=snake.index((nxti,nxtj))
                continue
            if nxti==applei and nxtj==applej:
                return -1
            queue.append((nxti,nxtj))
    dict={target:0}
    queue=[(0,0),target]
    queh=0
    while queh<len(queue)-1:
        queh+=1
        for i in range(4):
            nxti,nxtj=queue[queh][0]+di[i],queue[queh][1]+dj[i]
            if (nxti,nxtj) in queue or min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
                continue
            queue.append((nxti,nxtj))
            dict[queue[-1]]=dict[queue[queh]]+1 
    k,kmax=-1,-1
    for i in range(0,4):
        nxti,nxtj=snake[0][0]+di[i],snake[0][1]+dj[i]
        if min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
            continue
        nxt=(nxti,nxtj)
        if dict.get(nxt,0)>kmax:
            kmax=dict.get(nxt,0)
            k=i
    return k

def autoChangeDirection():
    queue=[(0,0),snake[0]]
    fa=[0,0]
    lastdire=[-1,-1]
    target=(applei,applej)
    queh=0
    while queh<len(queue)-1:
        queh+=1
#        print(f"正在搜索{queue[queh]} 目标是{target[0]},{target[1]}")
        for i in range(0,4):
            nxti,nxtj=queue[queh][0]+di[i],queue[queh][1]+dj[i]
            if (nxti,nxtj) in queue or min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
                continue
            queue.append((nxti,nxtj))
            fa.append(queh)
            lastdire.append(i)
            if queue[-1]==target:
                break
        if queue[-1]==target:
            break
    else:
        return
    stack=[]
    p=len(queue)-1
    while p>1:
        stack.append(lastdire[p])
        p=fa[p]
    while len(stack) !=0:
        yield stack[-1]
        del stack[-1]
"""
direlist=[]
def changeDirection():
    global direlist
    g=autoChangeDirection()
    direlist=[i for i in g]
    if len(direlist)>=1:
        return direlist[0]
    else:
        return stallForTime()
    del direlist[0]
    return direlist[0]
"""
direlist=[]
def changeDirection():
    global direlist
    if len(direlist) <= 1:
        g=autoChangeDirection()
        direlist=[i for i in g]
        if len(direlist)>=1:
            return direlist[0]
        else:
            return stallForTime()
    else:
        del direlist[0]
        return direlist[0]
    

def putApple():
    global applei,applej
    applei,applej=random.randint(1,mplength),random.randint(1,mpwidth)
    while (applei,applej) in snake:
        applei,applej=random.randint(1,mplength),random.randint(1,mpwidth)


    
def startGame():
    '''
    开始一局游戏
    '''
    global dire
    printmp()
    while True:
        tstart=time.time()
        dire=changeDirection()
        i,j=snake[0]
        nxti,nxtj=i+di[dire],j+dj[dire]
        if mptotype(nxti,nxtj)<3 and snake[-1]!=(nxti,nxtj):
            print(f"""
GAME OVER
The length of snake is {len(snake)} 
            """)
            return
        if nxti==applei and nxtj==applej:
            putApple()
        else:
            del snake[-1]
        snake.insert(0,(nxti,nxtj))
        printmp()
        time.sleep(showMpTime+time.time()-tstart)

#startGame()

def infinityMode():
    gameCount=0
    totalLength=0
    global snake,applei,applej,dire
    while True:
        startGame()
        totalLength+=len(snake)
        gameCount+=1
        print(f"已经进行了{gameCount}局,平均长度是{totalLength/gameCount}")
        snake=[(3,1),(2,1),(1,1)]
        dire=1
        applei,applej=4,4
        time.sleep(3)

infinityMode()
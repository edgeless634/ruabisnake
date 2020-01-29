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
mplength,mpwidth=10,30
applei,applej=4,4
#mpchar="口回田果　"
mpchar=["\033[1;44m　\033[0m","\033[1;45m　","\033[1;42m　","\033[1;43m　","\033[1;47m　"]
showMpTime=0 #地图刷新的最短时间
clearCommand="cls" if os.name=="nt" else "clear"
debug=[]

def mptotype(i,j):
    '''
    1=头 2=身子 3=果子 4=空气 0=虚空
    '''
    if (i,j) in snake:
        return 1 if snake.index((i,j))==0 else 2 #snake's head jor body
    elif i==applei and j==applej:
        return 3 #apple
    elif min(i,j)<1 or i>mplength or j>mpwidth:
        return 0 #empty
    else:
        return 4 #air

def printmp():
    mp=['',]
    os.system(clearCommand)
    '''
    print(mpchar[0]*(mpwidth+2))
    for i in range(1,mplength+1):
        print(mpchar[0],end="")
        for j in range(1,mpwidth+1):
            print(mpchar[mptotype(i,j)],end="")
        print(mpchar[0])
    print(mpchar[0]*(mpwidth+2))
    '''
    mp[0]=mpchar[0]*(mpwidth+2)
    for i in range(1,mplength+1):
        mp.insert(i,mpchar[0])
        last=""
        for j in range(1,mpwidth+1):
            mp[i]=mp[i]+("　" if last==mpchar[mptotype(i,j)] else mpchar[mptotype(i,j)])
            last=mpchar[mptotype(i,j)]
        mp[i]=mp[i]+mpchar[0]
    mp.insert(mplength+1,mpchar[0]*(mpwidth+2))
    for i in mp:
        print(i)
    if len(debug)>0:
        print(debug)


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
    k,kmax=dire,-1
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
    vis=[(0,0),snake[0]]
    fa=[0,0]
    lastdire=[dire,dire]
    target=(applei,applej)
    queh=0
    while queh<len(vis)-1:
        queh+=1
        for i in range(0,4):
            nxti,nxtj=vis[queh][0]+di[i],vis[queh][1]+dj[i]
            if (nxti,nxtj) in vis or min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
                continue
            vis.append((nxti,nxtj))
            fa.append(queh)
            lastdire.append(i)
            if vis[-1]==target:
                break
        if vis[-1]==target:
            break
    else:
        return
    stack=[]
    p=len(vis)-1
    while p>1:
        stack.append(lastdire[p])
        p=fa[p]
    while len(stack) !=0:
        yield stack[-1]
        del stack[-1]

def newAutoChangeDirection():
    fakeHead=list(snake[0])
    done=1
    while done==0:
        done=0
        if fakeHead[0]!=applei:
            if fakeHead[0]>applei and mptotype(fakeHead[0]-1,fakeHead[1])>=3:
                yield 0
                done=1
                fakeHead[0]+=1
            elif fakeHead[0]<applei and mptotype(fakeHead[0]+1,fakeHead[1])>=3:
                yield 2
                done=1
                fakeHead[0]-=1
        elif fakeHead[1]!=applej:
            if fakeHead[1]>applej and mptotype(fakeHead[0],fakeHead[1]+1)>=3:
                yield 1
                done=1
                fakeHead[1]+=1
            elif fakeHead[1]<applej and mptotype(fakeHead[0],fakeHead[1]-1)>=3:
                yield 3
                done=1
                fakeHead[1]-=1
    for i in autoChangeDirection():
        yield i

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
        g=newAutoChangeDirection()
        direlist=[i for i in g]
        if len(direlist)>=1:
            return direlist[0]
        else:
            return stallForTime()
    else:
        del direlist[0]
        return direlist[0]
    
def startGame():
    '''
    开始一局游戏
    '''
    global dire,applei,applej
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
            applei,applej=random.randint(1,mplength),random.randint(1,mpwidth)
            while (applei,applej) in snake:
                applei,applej=random.randint(1,mplength),random.randint(1,mpwidth)
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
#!/usr/bin/env python
#-*- coding:utf8 -*-
import os
import time
import random
dire=1
diretohanzi="右下左上"
#右 下 左 上
di=[0,1,0,-1] 
dj=[1,0,-1,0]
mplength,mpwidth=10,20
applei,applej=4,4
#mpchar="口回田果　"
mpchar=["\033[1;44m　\033[0m","\033[1;45m　","\033[1;42m　","\033[1;43m　","\033[1;47m　"]
showMpTime=0 #地图刷新的最短时间
clearCommand="cls" if os.name=="nt" else "clear"
debug=[]


class RobotSnake:
    def __init__(self):
        self.body = [(3,1),(2,1),(1,1)]
        self.directionPlan = []
        self.currentDirection = 1
    def leftSide(self):
        '''蛇头左侧的坐标'''
        return (self.body[0][0] + di[(self.currentDirection+1)%4],\
            self.body[0][1] + dj[(self.currentDirection+1)%4])
    def rightSide(self):
        '''蛇头右侧的坐标'''
        return (self.body[0][0] + di[(self.currentDirection+3)%4],\
            self.body[0][1] + dj[(self.currentDirection+3)%4])
    def ahead(self):
        '''蛇头前方的坐标'''
        return (self.body[0][0] + di[self.currentDirection],\
            self.body[0][1] + dj[self.currentDirection])
    def stallForTime(self):
        '''
        在够不到果子的时候苟命
        基本思路:
        1.找到头部能够得到,且离尾部最近的身体
        2.计算那段身子到周围几个空位的距离
        3.往离那段身子最远的空位走(尽量贴墙)
        '''
        queue=[(0,0),self.body[0]]
        queh=0
        target=(0,0)
        mxtarget=0
        while queh<len(queue)-1:
            queh+=1
            for i in range(4):
                nxti,nxtj=queue[queh][0]+di[i],queue[queh][1]+dj[i]
                if (nxti,nxtj) in queue or min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
                    if (nxti,nxtj) in self.body and mxtarget<self.body.index((nxti,nxtj)):
                        target=(nxti,nxtj)
                        mxtarget=self.body.index((nxti,nxtj))
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
            nxti,nxtj=self.body[0][0]+di[i],self.body[0][1]+dj[i]
            if min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth or mptotype(nxti,nxtj)<3:
                continue
            nxt=(nxti,nxtj)
            if dict.get(nxt,0)>kmax:
                kmax=dict.get(nxt,0)
                k=i
        return k

    def changeDirection(self):
        '''
        自动控制蛇的行动方向简化版
        当可以走直线时优先走
        '''
        fakeHead=list(self.body[0])
        done=1
        vis = []
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
            if done == 1:
                vis.append(tuple(fakeHead))
        
        queue=[(0,0),self.body[0]]
        father=[0,0]
        lastdire=[dire,dire]
        target=(applei,applej)
        queh=0
        while queh<len(queue)-1:
            queh+=1
            for i in range(0,4):
                nxti,nxtj=queue[queh][0]+di[i],queue[queh][1]+dj[i]
                if (nxti,nxtj) in queue\
                    or (nxti,nxtj) in vis\
                    or min(nxti,nxtj)<1 or nxti>mplength or nxtj>mpwidth\
                    or mptotype(nxti,nxtj)<3:
                    continue
                queue.append((nxti,nxtj))
                father.append(queh)
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
            p=father[p]
        while len(stack) !=0:
            yield stack[-1]
            del stack[-1]
    
    def refreshPlan(self):
        self.directionPlan = [i for i in self.changeDirection()]
    def newDirection(self):
        if len(self.directionPlan) <= 1:
            self.directionPlan = [i for i in self.changeDirection()]
            if len(self.directionPlan) == 0:
                return snake.stallForTime()
        self.currentDirection = self.directionPlan[0]
        del self.directionPlan[0]
        return self.currentDirection



snake = RobotSnake()


def mptotype(i,j):
    global snake
    '''
    1=头 2=身子 3=果子 4=空气 0=虚空
    '''
    if (i,j) in snake.body:
        return 1 if snake.body.index((i,j))==0 else 2 #snake's head jor body
    elif i==applei and j==applej:
        return 3 #apple
    elif min(i,j)<1 or i>mplength or j>mpwidth:
        return 0 #empty
    else:
        return 4 #air

def printmp():
    mp=['',]
    os.system(clearCommand)
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

def startGame():
    '''
    开始一局游戏
    '''
    global dire,applei,applej,snake
    printmp()
    while True:
        tstart=time.time()
        dire=snake.newDirection()
        i,j=snake.body[0]
        nxti,nxtj=i+di[dire],j+dj[dire]
        if mptotype(nxti,nxtj)<3 and snake.body[-1]!=(nxti,nxtj):
            print(f"""
GAME OVER
The length of snake is {len(snake.body)} 
            """)
            return
        if nxti==applei and nxtj==applej:
            ki,kj=random.randint(1,mplength),random.randint(1,mpwidth)
            while (ki,kj) in snake.body or (ki==nxti and kj==nxtj):
                ki,kj=random.randint(1,mplength),random.randint(1,mpwidth)
            applei,applej=ki,kj
        else:
            del snake.body[-1]
        snake.body.insert(0,(nxti,nxtj))
        printmp()
        time.sleep(showMpTime+time.time()-tstart)

#startGame()

def infinityMode():
    gameCount=0
    totalLength=0
    global snake,applei,applej,dire
    while True:
        startGame()
        totalLength+=len(snake.body)
        gameCount+=1
        print(f"已经进行了{gameCount}局,平均长度是{totalLength/gameCount}")
        snake=RobotSnake()
        dire=1
        applei,applej=4,4
        time.sleep(3)

infinityMode()
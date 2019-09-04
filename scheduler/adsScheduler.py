import math
import networkx as nx
import csv
from random import *
import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
from os import listdir
from os.path import isfile, join
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
from PyQt5.QtMultimedia import * 
from PyQt5.QtMultimediaWidgets import * 



import os
import time
import sys

import main5
# %matplotlib inline

MATRIX = {
    'food': [0.145437,0.038254756,0.05652054,0.699614006,0.004721533,0.014440309,0.041011856],
    'fashion': [0.088172765,0.090634441,0.033568312,0.76759539,0.001295737,0.001009287,0.017724068],
    'car': [0.066686658,0.168730671,0.071162272,0.64001289,0.002251234,0.002819637,0.048336638],
    'electronic': [0.417845905,0.055618038,0.015917939,0.486065644,0.000277616,0.008641167,0.01563369],
    'finance': [0.099159684,0.255391563,0.042608695,0.565509891,0.002488765,0.000441723,0.03439968],
    'cosmetic': [0.568414418,0.062437231,0.018259945,0.338692529,0.000471224,0.000209106,0.011515546],
    'home supplies': [0.337837838,0.021173681,0.016844839,0.580629376,0.001420989,0.00501581,0.037077467],
    'game': [0.10462379,0.161052825,0.081131874,0.639367607,0.002005289,0.007580381,0.004238232],
    'app': [0.126856416,0.222234813,0.04973527,0.585491152,0.002083845,0.009097147,0.004501357],
    'education': [0.210284944,0.032167619,0.059770914,0.673781217,0.004542589,0.008204916,0.011247799]
}
class Ads:
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount
        self.vector = MATRIX[category]
        self.weight = 0
        self.slots = []
    def calWeight(self, emotionVector):
        for i in range(7):
            self.weight += emotionVector[i] * self.vector[i]
        return self.weight
    def getSlots(self):
        return self.slots
    def setSlots(self, slots):
        self.slots = slots
    def checkSubject(self, slot, interval):
        # 광고 총량 확인 & 슬롯 최소이격 확인
        if self.amount <= 0:
            return False
        for s in self.slots:
            if (s - slot)*(s - slot) <= interval*interval:
                return False
        self.amount -= 1
        self.slots.append(slot)
        return True
    def popSlot(self):
        self.slots.pop()
        self.amount += 1
class Slot:
    def __init__(self, emotionVector):
        self.emotionVector = emotionVector
    def getEmotionVector(self):
        return self.emotionVector
class NetworkGraph:
    def __init__(self, categoryCount, slotCount):
        self.g = nx.DiGraph()
        for i in range(categoryCount+slotCount):
            self.g.add_node(i)
        self.layout = {}
        for i in range(0,categoryCount):
            self.layout[i] = [0,i]
        for i in range(categoryCount,categoryCount+slotCount):
            self.layout[i] = [1,i-categoryCount]
    def addEdge(self, edge):
        self.g.add_edge(edge['start']-1,edge['target']-1,weight=edge['weight'])
    def drawGraph(self,fileIdx):
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        nx.draw_networkx_nodes(self.g, self.layout, node_color='steelblue',node_size=600)
        nx.draw_networkx_edges(self.g, self.layout, edge_color='gray')
        nx.draw_networkx_labels(self.g, self.layout, font_color='white')
        pathName = 'result\\'+str(fileIdx)+'.png'
        plt.savefig(pathName)
        return plt

def isCyclicUtil(graph,visited,cur,parent):
    for e in graph[cur]:
        if e != parent:
            if e in visited:
                return True
            visited.append(e)
            if isCyclicUtil(graph,visited,e,cur):
                return True
    return False

def isCyclic(graph):
    visited = []
    if isCyclicUtil(graph,visited,0,-1):
        return True
    else:
        return False   

def getEmotionMatrix(amount):
    emotionMatrix = []
    for i in range(amount):
        emotionMatrix.append([random() for e in range(7)])
    # f = open('data/result2.csv', 'r', encoding='utf-8')
    # rdr = csv.reader(f)
    # for line in rdr:
    #     if amount == 0:
    #         break
    #     amount -= 1
    #     emotionMatrix.append([float(e) for e in line])
    # f.close()
    return emotionMatrix



class MainDialog(QMainWindow, main5.Ui_MainWindow):    
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Advertisement")
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)
        self.nextBtn.clicked.connect(self.set_img)

        self.ads = []
        self.slots = []
        self.categoryCount=0
        self.slotCount=0

        self.minimumSeparation = 3

        self.edgeVector = []

        self.nodeDegree = []
        self.adPlayL=[]
        self.comboList =[]
        self.imgNum = 0
        self.f = open('../playList.txt','w')
        
    def btn1_clicked(self):
        self.adNum =  self.adNode.value()
        self.slotNum = self.slotNode.value()
        self.adNodelabelList= []
        
        
        for i in range(self.adNum):
            cb = QtWidgets.QComboBox(self.gridLayoutWidget)
            dg = QtWidgets.QComboBox(self.gridLayoutWidget)
            cb.setGeometry(QtCore.QRect(80, 40, 161, 60))
            dg.setGeometry(QtCore.QRect(80, 40, 100, 60))
            cb.addItems(["food", "fashion","car","electronic","finance","cosmetic","home supplies","game","app","education"])
            dg.addItems(["1","2","3","4","5"])
            adNodelabel= QtWidgets.QLabel(self.gridLayoutWidget)
            adNodelabel.setGeometry(QtCore.QRect(80, 40, 161, 60))
            font = QtGui.QFont()
            font.setFamily("Yu Gothic Light")
            font.setPointSize(10)
            adNodelabel.setFont(font)
            adNodeName = "adNodelabel"+str(i)
            adNodelabel.setObjectName(adNodeName)
            cbName = "cb"+str(i)
            dgName = "dg"+str(i)
            cb.setObjectName(cbName)
            dg.setObjectName(dgName)
            self.adNodelabelList.append(adNodelabel)
            self.gridLayout.addWidget(adNodelabel,i,0)
            self.gridLayout.addWidget(cb,i,1)
            self.gridLayout.addWidget(dg,i,2)
            adNodelabel.setText("advertisement "+str(i))
        
        
        # 0 = left node
        # 1 ~ categoryCount = category node
        # categoryCount+1 ~ = slot node
        self.categoryCount = dlg.adNum
        self.slotCount = dlg.slotNum
        self.g = NetworkGraph(self.categoryCount,self.slotCount)

        self.emotionMatrix = getEmotionMatrix(self.slotCount)

        # append slot node
        for i in range(self.slotCount):
            self.slots.append(Slot(self.emotionMatrix[i]))

    def set_img(self):
        files = [f for f in listdir('result') if isfile(join('result', f))]
        count = len(files)
        self.imgNum = self.imgNum+1
        if self.imgNum is not count:
            pathName = 'result\\'+str(self.imgNum)+'.png'
            pixmap = QPixmap(pathName)
            pixmap_resized = pixmap.scaled(720, 405, QtCore.Qt.KeepAspectRatio)
            self.label_3.setPixmap(pixmap_resized)
            self.label_3.show()
            self.label_3.update()
    
    def btn2_clicked(self):
        for i in range(self.adNum):
            cbName = "cb"+str(i)
            combo = self.findChild(QtWidgets.QComboBox, cbName)
            self.comboList.append(combo.currentText())
            dgName = "dg"+str(i)
            degreeL = self.findChild(QtWidgets.QComboBox, dgName)
            self.nodeDegree.append(degreeL.currentText())
        
        # append ads node         
        for i in range(self.categoryCount):
            self.ads.append(Ads(self.comboList[i],int(self.nodeDegree[i])))

        # append virtual node
        for i in range(self.categoryCount):
            self.edgeVector.append({
                'start': 0, 
                'target': i+1, 
                'weight': 100
                })
        for i in range(self.categoryCount):
            for j in range(self.slotCount):
                self.edgeVector.append({
                    'start': i+1, 
                    'target': j+self.categoryCount+1,
                    'weight': self.ads[i].calWeight(self.slots[j].getEmotionVector())
                    })

        # edge sort (weight)        
        self.sortedEdgeVector = sorted(self.edgeVector, key=lambda e: e['weight'], reverse=True)

        # logger
        for e in self.sortedEdgeVector:
            print(e)

        # init graph
        self.graph = [[] for i in range(self.categoryCount+self.slotCount+1)]
        totalEdgeCount = 0

        # connect virtual node & category nodeself.
        for i in range(self.categoryCount):
            self.graph[self.sortedEdgeVector[i]['start']].append(self.sortedEdgeVector[i]['target'])
            #self.g.addEdge(self.sortedEdgeVector[i])
            #self.g.drawGraph()

        self.sortedEdgeVector = self.sortedEdgeVector[self.categoryCount:-1]
        # connect category node & slot node
        fileIdx = 0
        for e in self.sortedEdgeVector:
            if self.ads[e['start']-1].checkSubject(e['target']-self.categoryCount-1,self.minimumSeparation):
                self.graph[e['start']].append(e['target'])
                if isCyclic(self.graph):
                    self.graph[e['start']].pop(-1)
                    self.ads[e['start']-1].popSlot()
                else:
                    totalEdgeCount += 1
                    self.graph[e['target']].append(e['start'])
                    # add edge & draw graph
                    self.g.addEdge(e)
                    self.g.drawGraph(fileIdx)
                    fileIdx+=1
                    self.adPlayL.append(e['start'])
                if totalEdgeCount == self.categoryCount+self.slotCount:
                    break
        pathName = 'result\\'+str(0)+'.png'
        print(self.adPlayL)
        print(self.comboList)
        for i in self.adPlayL:
            print(self.comboList[i-1])
            self.f = open("../playList.txt",'a')
            self.f.write(str(self.comboList[i-1]) +".mp4\n")
        self.f.close()
        print(pathName)
        pixmap = QPixmap(pathName)
        pixmap_resized = pixmap.scaled(720, 405, QtCore.Qt.KeepAspectRatio)
        self.label_3.setPixmap(pixmap_resized)
        #self.set_img()

            
        
app = QApplication(sys.argv)
dlg = MainDialog()
dlg.show()
app.exec()
import numpy as np
import string
import sys
import json
import random

"""
Todo:
-change all punctuation characters to @
-change all @ to " @" with https://www.tutorialspoint.com/python/string_replace.htm

-count unique words to get vector weights for individual sentences

-average perceptron is just the sum of all the vanilla perceptrons at each step
-

"""

def indexWords(RArray):
    WordToNum = {}
    NumToWord = []
    counter = 0
    for i in range(len(RArray)):
        for j in range(len(RArray[i])):
            if RArray[i][j] not in WordToNum:
                WordToNum[RArray[i][j]] = counter
                NumToWord.append(RArray[i][j])
                counter += 1
    return WordToNum, NumToWord

def toNumRarray(Rarray, WordToNum):
    NumRarray = Rarray
    for i in range(len(Rarray)):
        for j in range(len(Rarray[i])):
            NumRarray[i][j] = WordToNum[Rarray[i][j]]
    return NumRarray

def indexTags(Tag):
    Tag = np.array(Tag)
    NumTag = np.zeros(Tag.shape)
    for i in range(len(Tag)):
        if Tag[i][0]=='Fake':
            NumTag[i][0] = -1
        else:
            NumTag[i][0] = 1
        if Tag[i][1]=='Neg':
            NumTag[i][1] = -1
        else:
            NumTag[i][1] = 1
    return NumTag

def toWCarray(NumRarray,NumToWord):
    N = len(NumRarray)
    M = len(NumToWord)
    WCarray = np.zeros(N, M)
    for i in range(len(NumRarray)):
        for j in range(len(NumRarray[i])):
            WCarray[i][NumRarray[i][j]] +=1
    return WCarray

def VanillaP(WCarray, NumTag):
    Maxiter = 30
    Wd = np.zeros(len(WCarray))
    b = 0
    r = list(range(len(WCarray)))
    WCarray = np.array(WCarray)
    for i in range(Maxiter):
        random.shuffle(r)
        for j in r:
            A = np.dot(WCarray[j], Wd)
            A = A + b
            ya = A*NumTag[j][0]
            if ya <= 0:
                Wd += NumTag[j][0]*WCarray[j]
                b += NumTag[j][0]
    Wd = Wd.tolist()
    Wd.append(b)
    Vfaketrue = Wd

    Wd = np.zeros(len(WCarray))
    b = 0
    r = list(range(len(WCarray)))
    WCarray = np.array(WCarray)
    for i in range(Maxiter):
        random.shuffle(r)
        for j in r:
            A = np.dot(WCarray[j], Wd)
            A = A + b
            ya = A * NumTag[j][1]
            if ya <= 0:
                Wd += NumTag[j][1] * WCarray[j]
                b += NumTag[j][1]
    Wd = Wd.tolist()
    Wd.append(b)
    Vnegpos = Wd

    return Vfaketrue, Vnegpos

def AverageP(WCarray, NumTag):
    Maxiter = 30
    Wd = np.zeros(len(WCarray))
    b = 0
    r = list(range(len(WCarray)))
    WCarray = np.array(WCarray)
    AvgW = np.zeros(len(WCarray))
    Avgb = 0
    counter = 0
    for i in range(Maxiter):
        random.shuffle(r)
        for j in r:
            A = np.dot(WCarray[j], Wd)
            A = A + b
            ya = A * NumTag[j][0]
            if ya <= 0:
                Wd += NumTag[j][0] * WCarray[j]
                b += NumTag[j][0]
            AvgW += Wd
            Avgb += b
            counter += 1
    AvgW = AvgW / counter
    Avgb = Avgb / counter
    AvgW = AvgW.tolist()
    AvgW.append(Avgb)
    Afaketrue = AvgW

    Wd = np.zeros(len(WCarray))
    b = 0
    r = list(range(len(WCarray)))
    WCarray = np.array(WCarray)
    AvgW = np.zeros(len(WCarray))
    Avgb = 0
    counter = 0
    for i in range(Maxiter):
        random.shuffle(r)
        for j in r:
            A = np.dot(WCarray[j], Wd)
            A = A + b
            ya = A * NumTag[j][1]
            if ya <= 0:
                Wd += NumTag[j][1] * WCarray[j]
                b += NumTag[j][1]
            AvgW += Wd
            Avgb += b
            counter += 1
    AvgW = AvgW / counter
    Avgb = Avgb / counter
    AvgW = AvgW.tolist()
    AvgW.append(Avgb)
    Anegpos = AvgW

    return Afaketrue, Anegpos


def main():
    Rarray = []
    ID = []
    Tag = []
    input_file = open(sys.argv[1], 'r')
    A = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
#    B = '                                '
    C = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    D = '0123456789'
    E = '##########'
    for line in input_file:
        word_array = line
        word_array = word_array.translate(string.maketrans(A, C))
#        word_array = word_array.translate(string.maketrans("", ""), string.punctuation)
        word_array = word_array.translate(string.maketrans("",""), "'")
        word_array = word_array.replace("@", " @ ")
        word_array = word_array.split()
        ID.append(word_array[0])
        Tag.append(word_array[1:3])
        Rarray.append(word_array[3:])

    for i in range(len(Rarray)):
        Rarray[i] = ' '.join(Rarray[i])
        Rarray[i].lower()
        Rarray[i] = Rarray[i].translate(string.maketrans("", ""), D, E)
        Rarray[i] = Rarray[i].replace('#', ' # ')
        Rarray[i] = Rarray[i].split()

    Rarray = list(filter(None, Rarray))

    WordToNum, NumToWord = indexWords(Rarray)
    NumRarray = toNumRarray(Rarray, WordToNum)
    NumTag = indexTags(Tag)
    WCarray = toWCarray(NumRarray, NumToWord)
    Vfaketrue, Vnegpos = VanillaP(WCarray, NumTag)
    Afaketrue, Anegpos = AverageP(WCarray, NumTag)

    output_file = open('vanillamodel.txt', 'w')
    output_file.write(json.dumps(Vfaketrue))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(Vnegpos))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(WordToNum))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(NumToWord))
    output_file.write('!@#$%^&*')
    output_file.close()

    output_file = open('averagedmodel.txt', 'w')
    output_file.write(json.dumps(Afaketrue))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(Anegpos))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(WordToNum))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(NumToWord))
    output_file.write('!@#$%^&*')
    output_file.close()

if __name__ == "__main__":
  main()
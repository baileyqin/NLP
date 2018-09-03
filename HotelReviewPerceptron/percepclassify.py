import numpy as np
import string
import sys
import json

def toNumRarray(Rarray, WordToNum):
    NumRarray = []
    for i in range(len(Rarray)):
        X = []
        for j in range(len(Rarray[i])):
            if Rarray[i][j] in WordToNum:
                X.append(WordToNum[Rarray[i][j]])
        NumRarray.append(X)
    return NumRarray

def classify(WCarray,Wd):
    WCarray = np.array(WCarray)
    Wd = np.array(Wd)
    Tag = []
    for i in range(len(WCarray)):
        A = np.dot(WCarray[i], Wd[:-1]) +Wd[-1]
        if A < 0:
            Tag.append(-1)
        else:
            Tag.append(1)
    return Tag

def NumToTag(FTNumTag, NPNumTag):
    Tag = []
    for i in range(len(FTNumTag)):
        X = []
        if FTNumTag[i] == -1:
            X.append('Fake')
        else:
            X.append('True')
        if NPNumTag[i] == -1:
            X.append('Neg')
        else:
            X.append('Pos')
        Tag.append(X)
    return Tag

def toWCarray(NumRarray, NumToWord):
    N = len(NumRarray)
    M = len(NumToWord)
    WCarray = np.zeros(N, M)
    for i in range(len(NumRarray)):
        for j in range(len(NumRarray[i])):
            WCarray[i][NumRarray[i][j]] += 1
    return WCarray

def main():
    training_data = open(sys.argv[1],'r')
    all_text = training_data.read()
    splits = all_text.split("!@#$%^&*")
    Vfaketrue = json.loads(splits[0])
    Vnegpos = json.loads(splits[1])
    WordToNum = json.loads(splits[2])
    NumToWord = json.loads(splits[3])
    training_data.close()

    input_file = open(sys.argv[2], 'r')
    ID=[]
    Rarray = []
    A = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
    #B = '                                '
    C = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    D = '0123456789'
    E = '##########'
    for line in input_file:
        word_array = line
        word_array = word_array.translate(string.maketrans(A, C))
        word_array = word_array.translate(string.maketrans("", ""), "'")
        word_array = word_array.replace("@", " @ ")
        word_array = word_array.split()
        ID.append(word_array[0])
        Rarray.append(word_array[1:])

    for i in range(len(Rarray)):
        Rarray[i] = ' '.join(Rarray[i])
        Rarray[i].lower()
        Rarray[i] = Rarray[i].translate(string.maketrans("", ""), D, E)
        Rarray[i] = Rarray[i].replace('#', ' # ')
        Rarray[i] = Rarray[i].split()

    Rarray = list(filter(None, Rarray))

    NumRarray = toNumRarray(Rarray, WordToNum)
    WCarray = toWCarray(NumRarray, NumToWord)
    FTNumTag = classify(WCarray, Vfaketrue)
    NPNumTag = classify(WCarray, Vnegpos)
    Tag = NumToTag(FTNumTag, NPNumTag)

    output = open('percepoutput.txt', 'w')
    PrintArray = ID
    for i in range(len(ID)):
        PrintArray[i] = ID[i] + ' ' + Tag[i][0] + ' ' + Tag[i][1]
        output.write(PrintArray[i] + '\n')
    output.close()

if __name__ == "__main__":
    main()
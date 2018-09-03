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

def classify(NumRarray, logpfake, logptrue, logpneg, logppos, logPwfake, logPwtrue, logPwneg, logPwpos):
    Tag=[]

    for i in range(len(NumRarray)):
        X = []
        Pfake = logpfake
        Ptrue = logptrue
        Pneg = logpneg
        Ppos = logppos
        for j in range(len(NumRarray[i])):
            Pfake += logPwfake[NumRarray[i][j]]
            Ptrue += logPwtrue[NumRarray[i][j]]
            Pneg += logPwneg[NumRarray[i][j]]
            Ppos += logPwpos[NumRarray[i][j]]
        if Pfake > Ptrue:
            X.append(0)
        else:
            X.append(1)
        if Pneg > Ppos:
            X.append(0)
        else:
            X.append(1)
        Tag.append(X)
    return Tag

def NumToTag(NumTag):
    Tag = []
    for i in range(len(NumTag)):
        X = []
        if NumTag[i][0] == 0:
            X.append('Fake')
        else:
            X.append('True')
        if NumTag[i][1] == 0:
            X.append('Neg')
        else:
            X.append('Pos')
        Tag.append(X)
    return Tag

def main():
    training_data = open('nbmodel.txt','r')
    all_text = training_data.read()
    splits = all_text.split("!@#$%^&*")
    logPwfake = json.loads(splits[0])
    logPwtrue = json.loads(splits[1])
    logPwneg = json.loads(splits[2])
    logPwpos = json.loads(splits[3])
    WordToNum = json.loads(splits[4])
    logpfake = json.loads(splits[5])
    logptrue = json.loads(splits[6])
    logpneg = json.loads(splits[7])
    logppos = json.loads(splits[8])
    training_data.close()

    input_file = open(sys.argv[1], 'r')
    ID=[]
    Rarray = []
    for line in input_file:
        word_array = line
        word_array = word_array.translate(string.maketrans(".", " "))
        word_array = word_array.translate(string.maketrans("", ""), string.punctuation)
        word_array = word_array.split()
        ID.append(word_array[0])
        Rarray.append(word_array[1:])

    Rarray = list(filter(None,Rarray))

    for i in range(len(Rarray)):
        for j in range(len(Rarray[i])):
            Rarray[i][j] = Rarray[i][j].lower()

    NumRarray = toNumRarray(Rarray, WordToNum)
    NumTag = classify(NumRarray, logpfake, logptrue, logpneg, logppos, logPwfake, logPwtrue, logPwneg, logPwpos)
    Tag = NumToTag(NumTag)

    nboutput = open('nboutput.txt', 'w')
    PrintArray = ID
    for i in range(len(ID)):
        PrintArray[i] = ID[i] + ' ' + Tag[i][0] + ' ' + Tag[i][1]
        nboutput.write(PrintArray[i] + '\n')
    nboutput.close()

if __name__ == "__main__":
    main()
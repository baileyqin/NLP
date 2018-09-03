import numpy as np
import string
import sys
import json

"""to delete punctuation without apostrophe
s = "this isn't ugly. For? a* the!"
A = '!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~'
     use  "string.punctuation" instead of "A" to delete apostrophes too
out = s.translate(string.maketrans("",""),A)
"""

"""
when data comes in it should be split up in an array by spaces
first line is ID
Rarray[line#][word#]
Tag[line#][0 = truth, 1 = positivity]
ID[line#]

to convert to lower case:
if s is the string you want to convert
s.lower()
converts it to lower case
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
            NumTag[i][0] = 0
        else:
            NumTag[i][0] = 1
        if Tag[i][1]=='Neg':
            NumTag[i][1] = 0
        else:
            NumTag[i][1] = 1
    return NumTag

def calcIDFw(NumRarray,NumToWord):
    NumRarray = np.array(NumRarray)
    NumToWord = np.array(NumToWord)
    IDF = np.zeros(NumToWord.shape)
    Mtotal = len(NumRarray)
    for i in range(len(NumRarray)):
        lineCount = np.zeros(NumToWord.shape)
        for j in range(len(NumRarray[i])):
            if lineCount[NumRarray[i][j]] != 1.0:
                lineCount[NumRarray[i][j]] = 1.0
        IDF = np.add(IDF, lineCount)
    IDF = np.log(Mtotal / IDF)
    return IDF

def calcPw(IDF,NumRarray,NumTag):
    Numeratorfake = np.zeros(IDF.shape)
    Numeratortrue = np.zeros(IDF.shape)
    Numeratorneg = np.zeros(IDF.shape)
    Numeratorpos = np.zeros(IDF.shape)
    for i in range(len(NumRarray)):
        if NumTag[i][0] == 0:
            for j in range(len(NumRarray[i])):
                Numeratorfake[NumRarray[i][j]] += 1
        else:
            for j in range(len(NumRarray[i])):
                Numeratortrue[NumRarray[i][j]] += 1
        if NumTag[i][1] == 0:
            for j in range(len(NumRarray[i])):
                Numeratorneg[NumRarray[i][j]] += 1
        else:
            for j in range(len(NumRarray[i])):
                Numeratorpos[NumRarray[i][j]] += 1

    Numeratorfake = np.multiply(Numeratorfake, IDF) + 1
    Numeratortrue = np.multiply(Numeratortrue, IDF) + 1
    Numeratorneg = np.multiply(Numeratorneg, IDF) + 1
    Numeratorpos = np.multiply(Numeratorpos, IDF) + 1

    Dfake = np.sum(Numeratorfake)
    Dtrue = np.sum(Numeratortrue)
    Dneg = np.sum(Numeratorneg)
    Dpos = np.sum(Numeratorpos)

    logPwfake = np.log(Numeratorfake) - np.log(Dfake)
    logPwtrue = np.log(Numeratortrue) - np.log(Dtrue)
    logPwneg = np.log(Numeratorneg) - np.log(Dneg)
    logPwpos = np.log(Numeratorpos) - np.log(Dpos)

    return logPwfake, logPwtrue, logPwneg, logPwpos

def calcprior(NumTag):
    pfake = 0.0
    ptrue = 0.0
    pneg = 0.0
    ppos = 0.0
    Mtotal = len(NumTag)

    for i in range(len(NumTag)):
        if Numtag[i][0] == 0:
            pfake += 1.0
        else:
            ptrue += 1.0
        if Numtag[i][1] == 0:
            pneg += 1.0
        else:
            ppos += 1.0

    logpfake = np.log(pfake) - np.log(Mtotal)
    logptrue = np.log(ptrue) - np.log(Mtotal)
    logpneg = np.log(pneg) - np.log(Mtotal)
    logppos = np.log(ppos) - np.log(Mtotal)
    return logpfake, logptrue, logpneg, logppos

def main():
    Rarray = []
    ID = []
    Tag = []
    input_file = open(sys.argv[1], 'r')
    for line in input_file:
        word_array = line
        word_array = word_array.translate(string.maketrans(".", " "))
        word_array = word_array.translate(string.maketrans("", ""), string.punctuation)
        word_array = word_array.split()
        ID.append(word_array[0])
        Tag.append(word_array[1:3])
        Rarray.append(word_array[3:])

    Rarray = list(filter(None, Rarray))

    for i in range(len(Rarray)):
        for j in range(len(Rarray[i])):
            Rarray[i][j] = Rarray[i][j].lower()

    WordToNum, NumToWord = indexWords(Rarray)
    NumRarray = toNumRarray(Rarray, WordToNum)
    NumTag = indexTags(Tag)
    IDF = calcIDFw(NumRarray,NumToWord)
    logPwfake, logPwtrue, logPwneg, logPwpos = calcPw(IDF,NumRarray,NumTag)
    logpfake, logptrue, logpneg, logppos = calcprior(NumTag)

    output_file = open('nbmodel.txt', 'w')
    output_file.write(json.dumps(logPwfake.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logPwtrue.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logPwneg.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logPwpos.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(WordToNum))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logpfake))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logptrue))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logpneg))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(logppos))
    output_file.close()

if __name__ == "__main__":
  main()
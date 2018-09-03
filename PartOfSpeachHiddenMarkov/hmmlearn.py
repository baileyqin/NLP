import numpy as np
import sys
import json

# I need to convert all tags into a number
# I need to create a hash table when given the tag, it gives me the number
# I need to create an array, where nth element is the nth corresponding tag

###### TO DO: CHANGE POSSIBLE THINGS WITH INTEGER TROUBLE TO FLOATING POINTS ??? not sure if needed

def findOccurences(s,ch):
    return[i for i,letter in enumerate(s) if letter == ch]

def indexTags(RArray):
    TagToNum = {}
    NumToTag = []
    counter = 0
    for i in range(len(RArray)):
        for j in range(len(RArray[i])):
            if RArray[i][j][1] not in TagToNum:
                TagToNum[RArray[i][j][1]] = counter
                NumToTag.append(RArray[i][j][1])
                counter += 1
    WordToNum = {}
    NumToWord = []
    counter = 0
    for i in range(len(RArray)):
        for j in range(len(RArray[i])):
            if RArray[i][j][0] not in WordToNum:
                WordToNum[RArray[i][j][0]] = counter
                NumToWord.append(RArray[i][j][0])
                counter += 1
    return TagToNum, NumToTag, WordToNum, NumToWord

def toNumRArray(RArray, TagToNum, WordToNum):
    NumRArray = RArray
    for i in range(len(RArray)):
        for j in range(len(RArray[i])):
            NumRArray[i][j][1] = TagToNum[RArray[i][j][1]]
            NumRArray[i][j][0] = WordToNum[RArray[i][j][0]]
    return NumRArray

# s, number of sentences
# w, number of words
# z, 0 or 1 depeneding on if you want word or tag

def CalcPriorProb(NumRArray, N):
    PriorProb = np.zeros(N)
    for line in range(len(NumRArray)):
        firstTag = NumRArray[line][0][1]
        PriorProb[firstTag] += 1
    PriorProb = PriorProb / N
    SPriorProb = np.ones(N)
    for line in range(len(NumRArray)):
        firstTag = NumRArray[line][0][1]
        SPriorProb[firstTag] += 1
    Stotal=np.sum(SPriorProb)
    SPriorProb = SPriorProb / Stotal
    return PriorProb, SPriorProb

def CalcTransitionProb(NumRArray,N):
    TransitionProb = np.zeros([N,N])
    tempProb = np.zeros([N,N])
    for i in range(len(NumRArray)):
        for j in range(len(NumRArray[i]) - 1):
            tempProb[NumRArray[i][j][1]][NumRArray[i][j+1][1]] += 1
    ProbTotals = np.sum(tempProb, axis = 1)
    for i in range(len(ProbTotals)):
        for j in range(len(ProbTotals)):
            TransitionProb[i][j] = tempProb[i][j] / ProbTotals[i]

    StempProb = tempProb + 1
    SProbTotals = np.sum(StempProb, axis = 1)
    STransitionProb = np.zeros([N,N])
    for i in range(len(SProbTotals)):
        for j in range(len(SProbTotals)):
            STransitionProb[i][j] = StempProb[i][j] / SProbTotals[i]
    return TransitionProb, STransitionProb

def CalcEmissionProb(NumRArray,N,M):
    EmissionProb = np.zeros([N,M+1])
    tempProb = np.zeros([N,M+1])
    for i in range(len(NumRArray)):
        for j in range(len(NumRArray[i])):
            tempProb[NumRArray[i][j][1]][NumRArray[i][j][0]] += 1
            tempProb[NumRArray[i][j][1]][M] +=1
    ProbTotals = np.sum(tempProb, axis = 1)
    for i in range(N):
        for j in range(M+1):
            EmissionProb[i][j] = tempProb[i][j] / ProbTotals[i]
    StempProb = np.ones([N,M+1])
    SEmissionProb = np.zeros([N,M+1])
    for i in range(len(NumRArray)):
        for j in range(len(NumRArray[i])):
            StempProb[NumRArray[i][j][1]][NumRArray[i][j][0]] += 1
            StempProb[NumRArray[i][j][1]][M] +=1
    SProbTotals = np.sum(StempProb,axis = 1)
    for i in range(N):
        for j in range(M+1):
            SEmissionProb[i][j] = StempProb[i][j] / SProbTotals[i]
    return EmissionProb, SEmissionProb

def MostProbTag(NumRArray,N,M):
    MPT = np.zeros([N,M+1])
    for i in range(len(NumRArray)):
        for j in range(len(NumRArray[i])):
            MPT[NumRArray[i][j][1]][NumRArray[i][j][0]] += 1
            MPT[NumRArray[i][j][1]][M] += 1
    
    PartialSum = np.sum(MPT, axis = 0)

    for i in range(N):
        for j in range(M+1):
            MPT[i][j] = MPT[i][j] / PartialSum[j]

    WordToTag = np.argmax(MPT, axis = 0)

    print(N)
    print(M)
    print(WordToTag.shape)

    return MPT, WordToTag


def main():
# opening file and making big array with words and labels
    result_array = []
    input_file = open(sys.argv[1], 'r')
    for line in input_file:
        line_array=[]
        word_array = line.split()
        for word in word_array:
            word_tag_array = []
            slashes = findOccurences(word,'/')
            slash_index = slashes[-1]
            word_tag_array.append(word[:slash_index])
            word_tag_array.append(word[slash_index+1:])
            line_array.append(word_tag_array)
        result_array.append(line_array)

# result_array[ line # ][word #][ 0/1]
# where 0 or 1 is word or label
    TagToNum, NumToTag, WordToNum, NumToWord = indexTags(result_array)
    N = len(NumToTag)
    M = len(NumToWord)
    NumRArray = toNumRArray(result_array, TagToNum, WordToNum)
    PriorProb,SPriorProb = CalcPriorProb(NumRArray,N)
    TransitionProb, STransitionProb = CalcTransitionProb(NumRArray,N)
    EmissionProb, SEmissionProb = CalcEmissionProb(NumRArray,N,M)
    MPT, WordToTag = MostProbTag(NumRArray,N,M)
    """
    for i in range(len(NumToTag)):
        if NumToTag[i] == ',':
            NumToTag[i] = '*&^%$#@!'

    for i in range(len(NumToWord)):
        if NumToWord[i] == ',':
            NumToWord[i] = '*&^%$#@!'
    """
    output_file = open('hmmmodel.txt','w')
    output_file.write(json.dumps(PriorProb.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(SPriorProb.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(TransitionProb.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(STransitionProb.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(EmissionProb.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(SEmissionProb.tolist()))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(TagToNum))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(NumToTag))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(WordToNum))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(NumToWord))
    output_file.write('!@#$%^&*')
    output_file.write(json.dumps(WordToTag.tolist()))
    """
    output_file.write(str(PriorProb.tolist()) + '!@#$%^&*')
    output_file.write(str(SPriorProb.tolist()) + '!@#$%^&*')
    output_file.write(str(TransitionProb.tolist()) + '!@#$%^&*')
    output_file.write(str(STransitionProb.tolist()) + '!@#$%^&*')
    output_file.write(str(EmissionProb.tolist()) + '!@#$%^&*')
    output_file.write(str(SEmissionProb.tolist()) + '!@#$%^&*')
    output_file.write(str(TagToNum) + '!@#$%^&*')
    output_file.write(str(NumToTag) + '!@#$%^&*')
    output_file.write(str(WordToNum) + '!@#$%^&*')
    output_file.write(str(NumToWord) + '!@#$%^&*')
    """
    output_file.close()
 # print(PriorProb, SPriorProb, TransitionProb, STransitionProb, EmissionProb, SEmissionProb, TagToNum, NumToTag, WordToNum, NumToWord)

if __name__ == "__main__":
  main()

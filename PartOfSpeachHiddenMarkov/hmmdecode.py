import numpy as np
import json
import sys
import copy

reload(sys)
sys.setdefaultencoding('utf8')

def veterbi(pi, A, B, O):
    """
    :param pi: initial probabilities
    :param A: Transition probabilities A[i,j] going from i to j
    :param B: Emission probabilities B[i,k] emitting from tag i to word k
    :param O: observation sequence, sequence of words from
    :return:
    """
    O = np.array(O)

    S = len(pi)
    N = len(O)
    delta = np.zeros([S,N])
    bestpaths = np.zeros([S,N])
    tempdelta = np.zeros(S)

    for j in range(S):
        delta[j][0] = pi[j] + B[j][O[0]]

    for t in range(N-1):
        for j in range(S):
            for i in range(S):
                tempdelta[i] = delta[i][t] + A[i][j] + B[j][O[t+1]]
        delta[j][t+1] = np.amax(tempdelta)
        bestpaths[j][t+1] = np.argmax(tempdelta)
        tempdelta = np.zeros(S)

    finaldelta = np.zeros(S)

    for j in range(S):
        finaldelta[j] = delta[j][N-1]

    path = np.zeros(N).astype(int)

    path[N-1] = np.argmax(finaldelta)

    for t in range(N-1):
        path[N-2-t] = bestpaths[path[N-1-t]][N-1-t]

    path = path.tolist()
    return path

def OtoNum(Ounp,WordToNum):
    O = copy.deepcopy(Ounp)
    for i in range(len(Ounp)):
        for j in range(len(Ounp[i])):
            if O[i][j] in WordToNum:
                O[i][j] = WordToNum[Ounp[i][j]]
            else:
    #unknown words:
                O[i][j] = len(WordToNum)-1
    return O



def main():

    """
    to do list:
    -check veterbi algorithm for correctness at the n-1 step vvvv
    -write loop to run veterbi over all sentences in testing data vvvv
    - write thinggy to intake test data &&&& convert words into number form vvvv
    -get all tags from veterbi algorithm &&&& convert it from number to tag form vvvv
    -write output data in format word / tag

    -account for unseen words when converting words to number vvvv done in smoothing
    and conversion from words to number step

    """

    """
    unknown tags observed variables in array Ounp[line#][word#] gives the word
    """
    training_data = open('hmmmodel.txt','r')
    all_text = training_data.read()
    BigMessUp = all_text.split("!@#$%^&*")

    PriorProb = json.loads(BigMessUp[0])
    SPriorProb = json.loads(BigMessUp[1])
    TransitionProb = json.loads(BigMessUp[2])
    STransitionProb = json.loads(BigMessUp[3])
    EmissionProb = json.loads(BigMessUp[4])
    SEmissionProb = json.loads(BigMessUp[5])
    TagToNum = json.loads(BigMessUp[6])
    NumToTag = json.loads(BigMessUp[7])
    WordToNum = json.loads(BigMessUp[8])
    NumToWord = json.loads(BigMessUp[9])
    WordToTag = json.loads(BigMessUp[10])
    training_data.close()
    
    NewArray = open(sys.argv[1], 'r')
    result_array = []
    for line in NewArray:
        word_array = line.split()
        result_array.append(word_array)
    NewArray.close()
    Ounp = result_array
    O = OtoNum(Ounp, WordToNum)
    O = np.array(O)
    """
    not sure which ones to use, shall check
    """
    pi = SPriorProb
    A =STransitionProb
    B = EmissionProb

    A = np.array(A)
    B = np.array(B)
    pi = np.array(pi)

    A = np.log(A)
    B = np.log(B)
    pi = np.log(pi)
    A = np.maximum(A, -10e13)
    B = np.maximum(B, -10e13)
    pi = np.maximum(pi, -10e13)
    """
    NumBestTags = []
    for i in range(len(O)):
    	vet = veterbi(pi,A,B,O[i])
        NumBestTags.append(vet)
    """
    NumBestTags = copy.deepcopy(O.tolist())
    for i in range(len(Ounp)):
    	for j in range(len(Ounp[i])):
    		NumBestTags[i][j] = WordToTag[O[i][j]]


    BestTags = copy.deepcopy(O.tolist())

    for i in range(len(NumBestTags)):
        for j in range(len(NumBestTags[i])):
            BestTags[i][j] = NumToTag[NumBestTags[i][j]]
    PrintArray = Ounp
    hmmoutput = open('hmmoutput.txt','w')
    for i in range(len(NumBestTags)):
        for j in range(len(NumBestTags[i])):
            PrintArray[i][j] = PrintArray[i][j]+'/'+BestTags[i][j]
        hmmoutput.write(((" ").join(PrintArray[i])) + '\n')
    hmmoutput.close()

if __name__ == "__main__":
  main()

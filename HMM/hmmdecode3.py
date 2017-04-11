import json
import codecs
import time
from collections import OrderedDict

class POSTagger:
    
    def __init__(self, testFilePath):
        self.testFilePath = testFilePath
        self.modelParameterFile = "hmmlearn.txt"
        self.outputFile = "hmmoutput.txt"
        #reading the model parameters file
        with codecs.open(self.modelParameterFile, mode='r', encoding="utf-8") as modelFile:
            model = json.load(modelFile)
        self.transitionMatrix = OrderedDict(model['transition'])
        self.emissionMatrix = OrderedDict(model['emission'])
        #reading the test data file
        with codecs.open(self.testFilePath, mode='r', encoding="utf-8") as testFile:
            self.testData = testFile.readlines()
        self.possibleTags = self.emissionMatrix.keys()
        self.startState = "start"
    
    def get_emission_prob(self, state, word):
        if word in self.emissionMatrix[state]:
            return self.emissionMatrix[state][word]
        else:
            return 1
    
    def get_transition_prob(self, prevState, currentState):
        return self.transitionMatrix[prevState][currentState]
    
    def get_tag_sequence(self, backpointers, probabilities, line, T):
        #finding the maximum probability tag
        finalTag = max(probabilities[T].keys(), key=(lambda key: probabilities[T][key]))
        word = "%s/%s" %(line[T-1], finalTag)
        tags = [word]
        currentTag = finalTag
        #retracing the backpointers to generate the probable states
        for t in range(T, 1, -1):
            word = "%s/%s" %(line[t-2], backpointers[t][currentTag]) 
            tags.append(word)
            currentTag = backpointers[t][currentTag]
        tags.reverse()
        return tags   
    
    def viterbi_decoding(self, line):
        line = line.strip().split(" ")
        T = len(line)
        backpointers = OrderedDict([])
        probabilities = OrderedDict([])
        for t in range(1, T+1): 
            backpointers[t] = {}
            probabilities[t] = {}
        
        #setting backpointers and probabilities for first word(initial probabilities)
        for state in self.transitionMatrix[self.startState]:
            backpointers[1][state] = self.startState
            probabilities[1][state] = self.get_emission_prob(state, line[0]) * self.get_transition_prob(self.startState, state)
        
        for t in range(2, T+1):
            for prevState in self.possibleTags:
                for currentState in self.possibleTags:
                    transitionProb = self.get_transition_prob(prevState, currentState)
                    emissionProb = self.get_emission_prob(currentState, line[t-1])
                    currentProb = probabilities[t-1][prevState] * transitionProb * emissionProb
                    if currentState in probabilities[t]:
                        if currentProb > probabilities[t][currentState]:
                            probabilities[t][currentState] = currentProb
                            backpointers[t][currentState] = prevState
                    else:
                        probabilities[t][currentState] = currentProb
                        backpointers[t][currentState] = prevState
                        
        return self.get_tag_sequence(backpointers, probabilities, line, T)
            
            
    def hmm_decode(self):
        with codecs.open(self.outputFile, mode='a', encoding="utf-8") as outputFile:
            for line in self.testData:
                outputLine = self.viterbi_decoding(line)
                outputLine = " ".join(outputLine) + "\n"
                outputFile.write(outputLine)
              
start_time = time.time()
hmmDecode = POSTagger("data\catalan_corpus_dev_raw.txt")
hmmDecode.hmm_decode()
print("--- %s seconds ---" % (time.time() - start_time))
        
        
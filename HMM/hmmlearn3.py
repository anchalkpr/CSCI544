import math
import json
import codecs
import sys
import time
from collections import OrderedDict

class HMMLearn:
    
    def __init__(self, inputPath):
        self.trainFilePath = inputPath
        with codecs.open(self.trainFilePath, mode='r', encoding='utf-8') as trainFile:
            self.trainingData = trainFile.readlines()
        self.modelParameterFile = "hmmlearn.txt"
        self.startState = "start"
        self.transitionMatrix = OrderedDict([(self.startState,{})])
        self.emissionMatrix = OrderedDict([])
        self.tagCount = OrderedDict([])
        self.words = set([])
    
    def normalize_and_smoothen_transition_matrix(self):
        tags = self.tagCount.keys()
        noOfTags = len(tags)
        for currentTag in self.transitionMatrix:
            denominator = float(sum(self.transitionMatrix[currentTag].values()) + noOfTags)
            for nextTag in tags:
                if nextTag in self.transitionMatrix[currentTag]:
                    self.transitionMatrix[currentTag][nextTag] += 1
                else:
                    self.transitionMatrix[currentTag][nextTag] = 1
                
                #self.transitionMatrix[currentTag][nextTag] = math.log(self.transitionMatrix[currentTag][nextTag]/denominator)
                self.transitionMatrix[currentTag][nextTag] = self.transitionMatrix[currentTag][nextTag]/denominator
    
    def normalize_emission_matrix(self):
        for tag in self.emissionMatrix:
            totalOccurencesOfTag = float(self.tagCount[tag])
            for word in self.words:
                if word in self.emissionMatrix[tag]:
                    #self.emissionMatrix[tag][word] = math.log(self.emissionMatrix[tag][word]/totalOccurencesOfTag)
                    self.emissionMatrix[tag][word] = self.emissionMatrix[tag][word]/totalOccurencesOfTag
                else:
                    self.emissionMatrix[tag][word] = 0
        
    def learn_from_training_data(self):
        for line in self.trainingData:
            wordTagPairs = line.strip().split()
            prevState = self.startState
            for wordAndTag in wordTagPairs:
                word = wordAndTag[:-3]
                tag = wordAndTag[-2:]
                self.words.add(word)
                
                #updating the tag counts for each tag
                if tag in self.tagCount:
                    self.tagCount[tag] += 1
                else:
                    self.tagCount[tag] = 1
                
                #updating the tag transition counts
                if prevState in self.transitionMatrix:
                    if tag in self.transitionMatrix[prevState]:
                        self.transitionMatrix[prevState][tag] += 1
                    else:
                        self.transitionMatrix[prevState][tag] = 1
                else:
                    self.transitionMatrix[prevState] = OrderedDict([(tag,1)])
                
                #updating the word emission counts    
                if tag in self.emissionMatrix:
                    if word in self.emissionMatrix[tag]:
                        self.emissionMatrix[tag][word] += 1
                    else:
                        self.emissionMatrix[tag][word] = 1
                else:
                    self.emissionMatrix[tag] = OrderedDict([(word,1)])
                    
                prevState = tag
                    
        self.normalize_and_smoothen_transition_matrix()
        self.normalize_emission_matrix()
        
    def outputModel(self):
        model = {"transition":self.transitionMatrix, "emission":self.emissionMatrix}
        with codecs.open(self.modelParameterFile, mode = "w", encoding = "utf-8") as outputFile:
            json.dump(model, outputFile)          
                
hmm = HMMLearn("data\catalan_corpus_train_tagged.txt")
start_time = time.time()
hmm.learn_from_training_data()
hmm.outputModel()
print("--- %s seconds ---" % (time.time() - start_time))

                
        
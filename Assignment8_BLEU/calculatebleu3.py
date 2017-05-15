from math import exp, log
import sys
import os
import codecs
from collections import defaultdict, Counter

class CalculateBleuScore:

    def __init__(self, candidateFile, referenceFiles):
        self.candidateFile = candidateFile
        self.referenceFiles = referenceFiles
        self.noOfReferenceFiles = len(self.referenceFiles)
        self.p_numerator = [0, 0, 0, 0]
        self.p_denominator = [0, 0, 0, 0]
        self.outputFileName = "bleu_out.txt"
        self.r = 0
        self.c = 0
        self.candidateSentences = []
        self.referenceSentences = defaultdict()
        self.numOfSentences = 0
        self.n = 4
        self.bleu_score = 0
        
    def get_n_grams(self, sentence):
        grams = defaultdict()
        for i in range(self.n):
            grams[i] = defaultdict(int)
        length = len(sentence)
        for i in range(length):
            for j in range(self.n):
                if i+j+1 <= length:
                    word = '_'.join(sentence[i:i+j+1])
                    grams[j][word] += 1
        return grams
        
    def calculate_count(self, c_grams, r_grams):
        print("c: %s" %c_grams)
        print("r: %s" %r_grams)
        total_count = 0
        for word, count in c_grams.items():
            if word in r_grams:
                print(word)
                total_count += min(count, r_grams[word])
        print(total_count)
        return total_count
        
    def read_data(self):
        with codecs.open(self.candidateFile, mode='r', encoding='utf-8') as cfile:
            self.candidateSentences = [sentence.strip().split() for sentence in cfile.readlines()]
        self.numOfSentences = len(self.candidateSentences)
        for i in range(len(self.referenceFiles)):
            with codecs.open(self.referenceFiles[i], mode='r', encoding='utf-8') as rfile:
                self.referenceSentences[i] = [sentence.strip().split() for sentence in rfile.readlines()]           
        
    def calculate_score(self):
        for i in range(self.numOfSentences):
            candidate = self.candidateSentences[i]
            references = [self.referenceSentences[j][i] for j in range(self.noOfReferenceFiles)]
            self.c += len(candidate)
            min_val = 10000
            min_r = 0
            for k in range(self.noOfReferenceFiles):
                if abs(len(candidate)-len(references[k])) < min_val:
                    min_val = abs(len(candidate)-len(references[k]))
                    min_r = len(references[k])
            #self.r += min([abs(len(candidate)-len(references[k])) for k in range(self.noOfReferenceFiles)])
            self.r += min_r
            #print("here")
            #print(candidate)
            grams_c = self.get_n_grams(candidate)
            grams_r = defaultdict()
            for i in range(self.n):
                grams_r[i] = defaultdict(int)
            for j in range(self.noOfReferenceFiles):
                #print("here too!!")
                grams = self.get_n_grams(references[j])
                for k in range(self.n):
                    for word, count in grams[k].items():
                        if word in grams_r[k]:
                            grams_r[k][word] = max(count, grams_r[k][word])
                        else:
                            grams_r[k][word] = count
            
            for j in range(self.n):
                self.p_numerator[j] += self.calculate_count(grams_c[j], grams_r[j])
                if len(candidate) - j > 0:
                    self.p_denominator[j] += len(candidate) - j
                    
        BP = None
        
        if self.c > self.r:
            BP = 1
        else:
            BP = exp(1-self.r/float(self.c))
        
        print("numerator: %s" %self.p_numerator)
        print("denominator: %s" %self.p_denominator)
        
        bleu_score = 0
        for i in range(self.n):
            bleu_score += log(self.p_numerator[i]/self.p_denominator[i])/float(self.n)
        bleu_score = BP * exp(bleu_score)
        self.bleu_score = bleu_score
        
    def output_score(self):
        with codecs.open(self.outputFileName, mode='w', encoding='utf-8') as outputFile:
            outputFile.write(str(self.bleu_score))
        
        
def run_calculate_bleu_score(candidateFile, referencePath):
    referenceFiles = []
    if referencePath.endswith(".txt"):
        referenceFiles = [referencePath]
    else:
        referenceFiles = [referencePath+rfile for rfile in os.listdir(referencePath)]
    
    calcBleu = CalculateBleuScore(candidateFile, referenceFiles)
    calcBleu.read_data()
    calcBleu.calculate_score()
    calcBleu.output_score()
    
    
run_calculate_bleu_score(sys.argv[1], sys.argv[2])
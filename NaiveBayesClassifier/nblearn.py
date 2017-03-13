from collections import Counter
import math
import sys

#This class contains methods that learn the model paramters from
#the training data
class NaiveBayesLearningModel:
    
    def __init__(self, file1, file2):
        self.classes = ['positive', 'negative', 'deceptive', 'truthful']
        self.train_text_file = file1
        self.train_labels_file = file2
        self.trainingClassification = {}
        self.tokens = {}
        self.priors = {}
        self.total_tokens = 0
        self.total_positive_tokens = 0
        self.total_negative_tokens = 0
        self.total_deceptive_tokens = 0
        self.total_truthful_tokens = 0
        self.total_words = 0
        self.outputFileName = "nbmodel.txt"
        
    def removePunctuation(self, line):
        line = line.replace("...", " ")
        punctuations = ['.', ',', '"', ';', '/', '!', "'s", '$', '-', '?', ':', '(', ')']
        for p in punctuations:
            if p == '$':
                line = line.replace(p, "$ ")
            elif p == '-' or p == '/' or p == '.':
                line = line.replace(p, " ")
            else:
                line = line.replace(p, "")
        line = line.replace("  ", " ")
        line = line.replace("  ", " ")
        return line
    
    def readTrainLabelsFile(self):
        with open(self.train_labels_file) as txt_file:
            for line in txt_file:
                line = line.strip().split(" ")
                self.trainingClassification[line[0]] = (line[1], line[2])

    def readTrainTextFile(self):
        with open(self.train_text_file) as txt_file:
            for line in txt_file:
                line = line.strip()
                review_id = line[:20]
                review = Counter(self.removePunctuation(line[21:].lower().strip()).split(" "))
                #review = Counter(line[21:].lower().strip().split(" "))
                if self.trainingClassification[review_id][0] == self.classes[2]:
                    for word in review:
                        if word != " " and word != '':
                            if word in self.tokens:
                                self.tokens[word][0][0] += review[word]
                            else:
                                self.tokens[word] = [[review[word], 0], [0, 0], [0, 0], [0, 0]]
                            self.total_deceptive_tokens += review[word]
                else:
                    for word in review:
                        if word != " " and word != '':
                            if word in self.tokens:
                                self.tokens[word][1][0] += review[word]
                            else:
                                self.tokens[word] = [[0, 0], [review[word], 0], [0, 0], [0, 0]]
                            self.total_truthful_tokens += review[word]
                if self.trainingClassification[review_id][1] == self.classes[0]:
                    for word in review:
                        if word != " " and word != '':
                            if word in self.tokens:
                                self.tokens[word][2][0] += review[word]
                            else:
                                self.tokens[word] = [[0, 0], [0, 0], [review[word], 0], [0, 0]]
                            self.total_positive_tokens += review[word]
                else:
                    for word in review:
                        if word != " " and word != '':
                            if word in self.tokens:
                                self.tokens[word][3][0] += review[word]
                            else:
                                self.tokens[word] = [[0, 0], [0, 0], [0, 0], [review[word], 0]]
                            self.total_negative_tokens += review[word]
        self.poupulateTotalTokens()

    
    def poupulateTotalTokens(self):
        self.total_tokens = self.total_deceptive_tokens + self.total_truthful_tokens + self.total_positive_tokens + self.total_negative_tokens
        self.total_words = len(self.tokens)
        
    def calculatePriors(self):
        for class_name in self.classes:
            if class_name == "positive":
                self.priors[class_name] = math.log(self.total_positive_tokens/float(self.total_tokens))
            elif class_name == "negative":
                self.priors[class_name] = math.log(self.total_negative_tokens/float(self.total_tokens))
            elif class_name == "deceptive":
                self.priors[class_name] = math.log(self.total_deceptive_tokens/float(self.total_tokens))
            elif class_name == "truthful":
                self.priors[class_name] = math.log(self.total_truthful_tokens/float(self.total_tokens))
                
    def calculateTokenLikelihoodProbabilities(self):
        for word in self.tokens:
            self.tokens[word][0][1] = math.log((self.tokens[word][0][0] + 1)/float(self.total_deceptive_tokens + self.total_words))
            self.tokens[word][1][1] = math.log((self.tokens[word][1][0] + 1)/float(self.total_truthful_tokens + self.total_words))
            self.tokens[word][2][1] = math.log((self.tokens[word][2][0] + 1)/float(self.total_positive_tokens + self.total_words))
            self.tokens[word][3][1] = math.log((self.tokens[word][3][0] + 1)/float(self.total_negative_tokens + self.total_words))
            
    def writeToFile(self):
        outputFile = open(self.outputFileName, "w")
        outputFile.write("%s\n" %self.total_words)
        for word, prob in self.priors.items():
            line = "%s %s\n" %(word, prob)
            outputFile.write(line)
        for word, value in self.tokens.items():
            line = "%s %s %s %s %s\n" %(word, value[0][1], value[1][1], value[2][1], value[3][1])
            outputFile.write(line)
            
def run_nb_learn():
    inputFile2 = "train-labels.txt"
    inputFile1 = "train-text.txt"
    nbl = NaiveBayesLearningModel(inputFile1, inputFile2)
    nbl.readTrainLabelsFile()
    nbl.readTrainTextFile()
    nbl.calculatePriors()
    nbl.calculateTokenLikelihoodProbabilities()
    nbl.writeToFile()

run_nb_learn()

"""if __name__=='__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    run_nb_learn(file1, file2) """ 

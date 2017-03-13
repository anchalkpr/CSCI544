from collections import Counter
import sys

#This class specieifies methods for reading the model parameters from nbmodel.txt
#and classifies the data in the test data file
class NaiveBayesClassifier:
    def __init__(self, file1):
        self.tokens = {}
        self.total_words = 0
        self.modelParametersFile = "nbmodel.txt"
        self.dataFile = file1
        self.outputFileName = "nboutput.txt"
        self.noOfClasses = 4
        self.classes = ['deceptive', 'truthful', 'positive', 'negative']
        self.priors = {}
        
        
    def removePunctuation(self, line):
        punctuations = ['.', ',', '"', ';', '/', '!', "'s", '$', '-']
        for p in punctuations:
            if p == '$':
                line = line.replace(p, "$ ")
            elif p == '-' or p== '/':
                line = line.replace(p, " ")
            else:
                line = line.replace(p, "")
        return line
    
    #reading the model parameters from nbmodel.txt
    def readModelParameters(self):
        txt_file = open(self.modelParametersFile)
        self.total_words = int(txt_file.readline().strip())
        for _ in range(self.noOfClasses):
            line = txt_file.readline().strip().split(" ")
            self.priors[line[0]] = float(line[1])
        for _ in range(self.total_words):
            line = txt_file.readline().strip().split(" ")
            self.tokens[line[0]] = [float(line[1]), float(line[2]), float(line[3]), float(line[4])]
            
    #classifies the data in the test data file        
    def classify(self):
        txt_file = open(self.dataFile, "r")
        outputFile = open(self.outputFileName, "w")
        for line in txt_file:
            line = line.strip()
            review_id = line[:20]
            review = Counter(self.removePunctuation(line[21:].lower()).split(" "))
            #review = Counter(line[21:].lower().strip().split(" "))
            prob_deceptive = self.priors[self.classes[0]]
            prob_truthful = self.priors[self.classes[1]]
            prob_positive = self.priors[self.classes[2]]
            prob_negative = self.priors[self.classes[3]]
            for word, value in review.items():
                if word in self.tokens:
                    prob_deceptive += self.tokens[word][0] * value
                    prob_truthful += self.tokens[word][1] * value
                    prob_positive += self.tokens[word][2] * value
                    prob_negative += self.tokens[word][3] * value
            classification1 = None
            classification2 = None
            if prob_deceptive > prob_truthful:
                classification1 = self.classes[0]
            else:
                classification1 = self.classes[1]
            if prob_positive > prob_negative:
                classification2 = self.classes[2]
            else:
                classification2 = self.classes[3]
            outputFile.write("%s %s %s\n" %(review_id, classification1, classification2))
            
def nb_classifier():
    file_name = "test-data.txt"
    nbc = NaiveBayesClassifier(file_name)
    nbc.readModelParameters()
    nbc.classify()

nb_classifier()

"""if __name__=='__main__':
    file_name = sys.argv[1]   
    nb_classifier(file_name)"""      
                    

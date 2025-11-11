import os


class Game():

    madLibsFiles = []
    madLibsDir = "madLibs"
    selectedMadLib = "" #The entire Mad Lib
    currFillInWord = 0
    fillInWords = []
    filledInWords = []

    def getMadLibs(self, dir :str) -> list:
        madList = []
        for file in os.scandir(dir):
            if file.name.endswith(".txt"):
                madList.append(file)
        return madList
    
    def selectMadLib(self, select :int):
        with open(os.path.join(self.madLibsFiles[select]), "r") as f:
            self.selectedMadLib = f.read()
            print(self.selectedMadLib)
    
    def getFillInWords(self):
        currWord = ""
        inBrackets = False
        for c in self.selectedMadLib:
            if c == "[":
                inBrackets = True
            elif c == "]":
                inBrackets = False
                self.fillInWords.append(currWord)
                currWord = ""
            elif inBrackets:
                currWord += c

    def getFillInWord(self) -> str:
        self.currFillInWord += 1
        return self.fillInWords[self.currFillInWord - 1]

    def showMadLib(self) -> str:
        for x in range(len(self.filledInWords)):
            if self.filledInWords[x] == "":
                self.filledInWords[x] = "Word Not Entered"
            self.selectedMadLib = self.selectedMadLib.replace("[" + self.fillInWords[x] + "]", self.filledInWords[x], 1)
        return("Mad Lib: " + self.selectedMadLib)
    
    def __init__(self):
        self.madLibsFiles = self.getMadLibs(self.madLibsDir)
    
    def reset(self):
        self.selectedMadLib = ""
        self.currFillInWord = 0
        self.fillInWords = []
        self.filledInWords = []


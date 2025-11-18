import os
import discord

class GameMaster():
    madLibsFiles = []
    madLibsDir = "madLibs"
    
    def getMadLibs(self, dir :str) -> list:
        madList = []
        for file in os.scandir(dir):
            if file.name.endswith(".txt"):
                madList.append(file)
        return madList
    
    def __init__(self):
        self.madLibsFiles = self.getMadLibs(self.madLibsDir)

class Game():

    def __init__(self, discordUser :discord.user):
        self.player = discordUser
        self.isSinglePlayer = True
        self.selectedMadLib = "" #The entire Mad Lib
        self.currFillInWord = 0
        self.fillInWords = []
        self.filledInWords = []
    

    def getMadLibs(self, dir :str) -> list:
        madList = []
        for file in os.scandir(dir):
            if file.name.endswith(".txt"):
                madList.append(file)
        return madList
    
    def selectMadLib(self, joinStr :str):
        with open(os.path.join(joinStr), "r") as f:
            self.selectedMadLib = f.read()
    
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
            self.selectedMadLib = self.selectedMadLib.replace("[" + self.fillInWords[x] + "]", self.filledInWords[x], 1)
        return("Mad Lib: " + self.selectedMadLib)

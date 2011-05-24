import re

allWhitespace = re.compile('\s+')

class StandardCommunicator(object):
    def __init__(self,
                 wrapLength=80):
        self.wrapLength = wrapLength
        
    def output(self,
               textToOutput):
        textToOutput = process(textToOutput, self.wrapLength)
        print textToOutput

def process(textToProcess,
            wrapLength):
    textToProcess = re.sub(allWhitespace, ' ', textToProcess)
    textToProcess = applyLineBreaks(textToProcess, wrapLength)
    return textToProcess

def applyLineBreaks(textToProcess, charactersPerLine):
    currentIndex = 0
    lines = []
    toIndex = findIndexOfLastSpace(textToProcess, charactersPerLine) + 1
    while currentIndex <= len(textToProcess):
        line = textToProcess[currentIndex:toIndex]
        lines.append(line)
        currentIndex = toIndex
        toIndex = findIndexOfLastSpace(textToProcess, toIndex + charactersPerLine) + 1
    return '\n'.join(lines)

def findIndexOfLastSpace(textToProcess, currentIndex):
    if currentIndex > len(textToProcess):
        return len(textToProcess)
    currentCharacter = textToProcess[currentIndex]
    while currentCharacter != ' ':
        currentIndex -= 1
        currentCharacter = textToProcess[currentIndex]
    return currentIndex
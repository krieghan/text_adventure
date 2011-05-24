import re

allWhitespace = re.compile('\s+')

def process(textToProcess):
    textToProcess = re.sub(allWhitespace, ' ', textToProcess)
    textToProcess = applyLineBreaks(textToProcess, 80)
    return textToProcess

def applyLineBreaks(textToProcess, charactersPerLine):
    currentIndex = 0
    lines = []
    toIndex = -1
    while (currentIndex + charactersPerLine) < len(textToProcess):
        currentIndex = toIndex + 1
        toIndex = findIndexOfLastSpace(textToProcess, currentIndex)
        line = textToProcess[currentIndex:toIndex]
        lines.append(line)
    return textToProcess
    
def findIndexOfLastSpace(textToProcess, currentIndex):
    currentCharacter = textToProcess[currentIndex]
    while currentCharacter != ' ':
        currentIndex -= 1
        currentCharacter = textToProcess[currentIndex]
    return currentIndex
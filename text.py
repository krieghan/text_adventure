import re

allWhitespace = re.compile('\s+')

def process(textToProcess):
    textToProcess = re.sub(allWhitespace, ' ', textToProcess)
    return textToProcess
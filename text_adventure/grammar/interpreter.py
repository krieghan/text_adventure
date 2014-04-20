from text_adventure import (exception,
                            sentence)

class Interpreter(object):
    def __init__(self,
                 dictionary,
                 thesaurus,
                 singleToPlural=None,
                 pluralToSingle=None):
        if singleToPlural is None:
            singleToPlural = {}
        if pluralToSingle is None:
            pluralToSingle = {}
        self.dictionary = dictionary
        self.verbs = dictionary.get('verbs', [])
        self.nouns = dictionary.get('nouns', [])
        self.commands = dictionary.get('commands', [])
        self.prepositions = dictionary.get('prepositions', [])
        self.articles = dictionary.get('articles', [])
        self.adjectives = dictionary.get('adjectives', [])
        self.directions = dictionary.get('directions', [])
        self.thesaurus = thesaurus
        self.singleToPlural = singleToPlural
        self.pluralToSingle = pluralToSingle    
        self.multiWordTokens = self.getMultiWordTokens()

    def addWords(self,
                 words,
                 partOfSpeech):
        if partOfSpeech == 'noun':
            self.nouns.extend(words)
            self.nouns = list(set(self.nouns))
        if partOfSpeech == 'adjective':
            self.adjectives.extend(words)
            self.adjectives = list(set(self.adjectives))
            
    def evaluate(self, text):
        words = self.getListOfWords(text)
        
        reducedWords = [x for x in words if not self.exclude(x)]
        simplifiedWords = [self.simplify(x) for x in reducedWords]
        structure = self.getStructure(simplifiedWords)
        
        actions = []
        
        if self.determineMatch(['command'],
                               structure):
            actions.append(sentence.Sentence(command=simplifiedWords[0]))
        if self.determineMatch(['direction'],
                               structure):
            actions.append(sentence.Sentence(verb='go',
                                             object=simplifiedWords[0]))
        if self.determineMatch(['verb', 'direction'],
                               structure):
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                             object=simplifiedWords[1]))
        if self.determineMatch(['verb', 'preposition'],
                               structure):
            phrases = [sentence.PrepositionalPhrase(preposition=simplifiedWords[1],
                                                    object=None)]
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                             prepositionalPhrases=phrases))
        if self.determineMatch(['verb', 'preposition', 'noun'],
                               structure):
            phrases = [sentence.PrepositionalPhrase(preposition=simplifiedWords[1],
                                                    object=simplifiedWords[2])]
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                             prepositionalPhrases=phrases))
        if self.determineMatch(['verb', 'noun'],
                               structure):
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                             object=simplifiedWords[1]))
        if self.determineMatch(['noun'],
                               structure):
            actions.append(sentence.Sentence(verb=None,
                                  object=simplifiedWords[0]))
        if self.determineMatch(['verb', 'noun', 'preposition'],
                               structure):
            phrases = [sentence.PrepositionalPhrase(preposition=simplifiedWords[2],
                                                    object=None)]
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                             prepositionalPhrases=phrases))
        if self.determineMatch(['verb', 'noun', 'preposition', 'noun'],
                               structure):
            phrases = [sentence.PrepositionalPhrase(preposition=simplifiedWords[2],
                                                    object=simplifiedWords[3])]
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                             object=simplifiedWords[1],
                                             prepositionalPhrases=phrases))
        if self.determineMatch(['verb', 'preposition', 'noun', 'preposition', 'noun'],
                               structure):
            phrases = [sentence.PrepositionalPhrase(preposition=simplifiedWords[1],
                                                    object=simplifiedWords[2]),
                       sentence.PrepositionalPhrase(preposition=simplifiedWords[3],
                                                    object=simplifiedWords[4])]
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                  object=simplifiedWords[2],
                                  prepositionalPhrases=phrases))
        if self.determineMatch(['verb', 
                                'noun', 
                                'preposition', 
                                'noun', 
                                'preposition',
                                'noun'],
                               structure):
            phrases = [PrepositionalPhrase(preposition=simplifiedWords[2],
                                           object=simplifiedWords[3]),
                       PrepositionalPhrase(preposition=simplifiedWords[4],
                                           object=simplifiedWords[5])]
            actions.append(
               sentence.Sentence(verb=simplifiedWords[0],
                                 object=simplifiedWords[1],
                                 prepositionalPhrases=phrases))
        if self.determineMatch(['verb',
                                'noun',
                                'noun'],
                               structure):
            raise Exception('What the fuck?')
            actions.append(sentence.Sentence(verb=simplifiedWords[0],
                                  object=simplifiedWords[2],
                                  indirectObject=simplifiedWords[1]))
            
        if len(actions) > 1:
            raise exception.CouldNotInterpret('I identified more than one way to interpret that command.')
        if len(actions) == 0:
            raise exception.CouldNotInterpret('I do not know what to do with the structure %s' % structure)
        if len(actions) == 1:
            parsedAction = actions[0]
        return parsedAction
    
    def getPartsOfSpeech(self, word):
        parts = []
        if word in self.commands:
            parts.append('command')
        if word in self.verbs:
            parts.append('verb')
        if word in self.nouns:
            parts.append('noun')
        if word in self.directions:
            parts.append('direction')
        if word in self.prepositions:
            parts.append('preposition')
        
        if not parts:
            raise exception.CouldNotInterpret('I did not understand "%s"' % word)
        else:
            return parts
        
    def getStructure(self, words):
        possibilities = [self.getPartsOfSpeech(x) for x in words]
        return possibilities
        
    def determineMatch(self,
                       concreteStructure,
                       possibilities):
        if len(concreteStructure) != len(possibilities):
            return False
        for index in range(len(concreteStructure)):
            partOfSpeech = concreteStructure[index]
            possiblePartsOfSpeech = possibilities[index]
            if partOfSpeech not in possiblePartsOfSpeech:
                return False
        return True
            
        
    def simplify(self, word):
        for synonymSet in self.thesaurus:
            if word in synonymSet:
                return synonymSet[0]
        return word
    
    def exclude(self, word):
        if word in self.articles:
            return True
        
        return False
    
    def getSingle(self,
                  plural):
        single = self.pluralToSingle.get(plural)
        if single is None:
            single = plural[0:-1]
        return single
    
    def getPlural(self,
                  single):
        plural = self.singleToPlural.get(single)
        if plural is None:
            plural = single[0:-1]
        return plural
    
    def getAllWords(self):
        return self.nouns + self.adjectives + self.verbs + self.prepositions + self.articles + self.directions
    
    def getMultiWordTokens(self):
        allTokens = self.getAllWords()
        multiWordTokens = []
        for token in allTokens:
            index = token.find(' ')
            if index > 0:
                multiWordTokens.append(token)
                
        return multiWordTokens
    
    def getListOfWords(self,
                       text):
        text = text.lower()
        for token in self.multiWordTokens:
            if token in text:
                tokenWithUnderscores = token.replace(' ', '_')
                text = text.replace(token, tokenWithUnderscores)
        
        words = text.split(' ')
        words = [x.replace('_', ' ') for x in words]
        return words

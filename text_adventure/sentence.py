class Sentence(object):
    def __init__(self,
                 verb=None,
                 object=None,
                 command=None,
                 prepositionalPhrases=None):
        if prepositionalPhrases is None:
            prepositionalPhrases = []
        self.prepositionalPhrases = {}
        self.verb = verb
        self.object = object
        self.command = command
        for prepositionalPhrase in prepositionalPhrases:
            self.prepositionalPhrases[prepositionalPhrase.preposition] = prepositionalPhrase
            
        if prepositionalPhrases:
            self.prepositionalPhrases['main'] = prepositionalPhrases[0]

        
    def verbOnly(self):
        if (self.verb is not None and 
            self.object is None and
            self.prepositionalPhrases == {}):
            return True
        else:
            return False
    
class PrepositionalPhrase(object):
    def __init__(self,
                 preposition=None,
                 object=None):
        self.preposition = preposition
        self.object = object

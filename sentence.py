class Sentence(object):
    def __init__(self,
                 verb,
                 object=None,
                 preposition=None,
                 indirectObject=None,
                 indirectObjectPhrase=None):
        if indirectObjectPhrase is None:
            indirectObjectPhrase = dict()
        self.verb = verb
        self.object = object
        self.preposition = preposition
        self.indirectObject = indirectObject
        self.indirectObjectPhrase = indirectObjectPhrase
    
    def verbOnly(self):
        if (self.verb is not None and 
            self.preposition is None and 
            self.object is None and 
            self.indirectObject is None):
            return True
        else:
            return False
    

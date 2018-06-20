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
        
    def verbOnly(self):
        if (self.verb is not None and 
            self.object is None and
            self.prepositionalPhrases == {}):
            return True
        else:
            return False

    def getObjects(self):
        objects = {}
        objects['main'] = getattr(self, 'object', None)
        for phrase in self.prepositionalPhrases.values():
            objects[phrase.preposition] = phrase.object
        return objects


class PrepositionalPhrase(object):
    def __init__(self,
                 preposition=None,
                 object=None):
        self.preposition = preposition
        self.object = object


class Command(object):
    def __init__(
            self,
            command,
            arguments):
        self.command = command
        self.arguments = arguments

    def isCheckingInventory(self):
        return self.command == 'inventory'

    def isQuitting(self):
        return self.sentence.command in ('quit', 'exit')

    def isSaving(self):
        return self.sentence.command == 'save'

    def isRestoring(self):
        return self.sentence.command in ('restore', 'load')


class InventoryManager(object):
    def __init__(self,
                 on=False,
                 under=False,
                 inside=False,
                 exposed=True):
        self.slots = dict() 
        self.exposed = exposed
        if on:
            self.slots['on'] = Inventory()
        if under:
            self.slots['under'] = Inventory()
        if inside:
            self.slots['inside'] = Inventory()
        
    def match(self, entityKey):
        matches = []
        for (key, inventory) in self.slots.items():
            matches.extend(inventory.match(entityKey))
        return matches
    
    def add(self,
            resource,
            slotKey):
        self.slots[slotKey][resource.key] = resource
        
    def remove(self,
               resource,
               slotKey=None):
        if slotKey is None:
            for slot in self.slots.values():
                if slot.get(resource.key):
                    del slot[resource.key]
            
    def addSlotKey(self,
                   slotKey):
        self.slots[slotKey] = Inventory()
    
    @classmethod
    def getSlotKey(cls,
                   key):
        if key in ('on', 'onto'):
            return 'on'
        if key in ('under',):
            return 'under'
        if key in ('inside', 'in', 'into'):
            return 'inside'
        
        return 'on'
    
    def getAll(self):
        resources = []
        for slot in self.slots.values():
            for resource in slot.values():
                 resources.append(resource)
                 
        return resources

class Inventory(dict):
    
    def __init__(self, 
                 **kwargs):
        dict.__init__(self,
                      **kwargs)
    
    def match(self, entityKey):
        matches = []
        for (key, entity) in self.items():
            if entityKey in entity.names:
                matches.append(entity)
            if entity.inventory.exposed:
                matches.extend(entity.inventory.match(entityKey))
        return matches
    
    

def displayPlayerInventory(inventory):
    print "In your inventory, you have:"
    slot = inventory.slots['inside']
    inventoryItems = slot.items()
    if not inventoryItems:
        print "nothing"
    else:
        for item in slot.values():
            print item.name

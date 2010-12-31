class ElementList(list):
    
    def __init__(self, list):
        self.extend(list)
    
    @property
    def first(self):
        return self[0]
    
    @property
    def last(self):
        return self[-1]
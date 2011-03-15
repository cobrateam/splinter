class ElementDoesNotExist(Exception):
    pass

class ElementList(list):
    
    def __init__(self, list):
        self.extend(list)
    
    @property
    def first(self):
        try:
            return self[0]
        except IndexError:
            raise ElementDoesNotExist('element doest not exist')
    
    @property
    def last(self):
        return self[-1]

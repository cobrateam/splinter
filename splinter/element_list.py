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
            raise ElementDoesNotExist('element does not exist')
    
    @property
    def last(self):
        try:
            return self[-1]
        except IndexError:
            raise ElementDoesNotExist('element does not exist')

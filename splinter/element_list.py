class ElementDoesNotExist(Exception):
    pass

class ElementList(list):
    
    def __init__(self, list):
        self.extend(list)

    def __getitem__(self, index):
        try:
            return super(ElementList, self).__getitem__(index)
        except IndexError:
            raise ElementDoesNotExist('element does not exist')
    
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

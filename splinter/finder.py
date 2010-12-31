class QueryElements(object):
    
    def __init__(self, list):
        self.list = list
    
    def all(self):
        return self.list
    
    def first(self):
        return self.list[0]
    
    def last(self):
        return self.list[-1]

    def __getitem__(self, key):
        return self.list[key]
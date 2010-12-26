class QueryElements(object):
    
    def __init__(self, list):
        self.list = list
    
    def all(self):
        return self.list
    
    def first(self):
        return self.list[0]
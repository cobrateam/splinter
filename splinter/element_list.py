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
        return self[0]

    @property
    def last(self):
        return self[-1]

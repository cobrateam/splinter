from splinter.exceptions import ElementDoesNotExist

class AttributesGrouper(type):

    def __init__(self, name, bases, class_dict):
        super(AttributesGrouper, self).__init__(name, bases, class_dict)

        attributes = {}
        for key, value in class_dict.items():
            if not key.startswith('__') or not key.endswith('__'):
                attributes[key] = value

        setattr(self, "_attributes", attributes)

class ElementList(list):
    __metaclass__ = AttributesGrouper

    def __init__(self, list, context=None, driver=None):
        self.extend(list)
        self.context = context
        self.driver = driver

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

    def find_by_css(self, element):
        return self.driver.find_by_css(element)

    def is_empty(self):
        return not len(self)

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]

        return getattr(self.first, name)

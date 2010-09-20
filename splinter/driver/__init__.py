class DriverAPI(object):
    @property
    def title(self):
        raise NotImplementedError

    @property
    def html(self):
        raise NotImplementedError

    def visit(self, url):
        raise NotImplementedError
 
    def find(self, css_selector=None,
                   xpath=None,
                   name=None,
                   id=None,
                   tag=None):
        raise NotImplementedError

    def fill_in(self, name, value):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError


class ElementAPI(object):

    def _get_value(self):
        raise NotImplementedError

    def _set_value(self, value):
        raise NotImplementedError

    value = property(_get_value, _set_value)

    def click(self):
        raise NotImplementedError

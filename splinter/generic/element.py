import lxml.html
from lxml.cssselect import CSSSelector
from splinter.driver import ElementAPI


class GenericElement(ElementAPI):

    def __init__(self, element, parent):
        self._element = element
        self.parent = parent

    def __getitem__(self, attr):
        return self._element.attrib[attr]

    def find_by_css(self, selector):
        elements = self._element.cssselect(selector)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_xpath(self, selector):
        elements = self._element.xpath(selector)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_name(self, name):
        elements = self._element.cssselect('[name="%s"]' % name)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_tag(self, name):
        elements = self._element.cssselect(name)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_value(self, value):
        elements = self._element.cssselect('[value="%s"]' % value)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_id(self, id):
        elements = self._element.cssselect('#%s' % id)
        return ElementList([self.__class__(element, self) for element in elements])

    @property
    def value(self):
        # @todo: tests are calling this method even if element is h1, what should we do?
        try:
            return self._element.attrib['value']
        except KeyError:
            return self._element.text

    @property
    def text(self):
        return self._element.text


class GenericLinkElement(GenericElement):

    def __init__(self, element, parent):
        super(GenericLinkElement, self).__init__(element, parent)
        self._browser = parent._browser

    def __getitem__(self, attr):
        return super(GenericLinkElement, self).__getitem__(attr)


class GenericControlElement(ElementAPI):

    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return self._control.attrib[attr]

    @property
    def value(self):
        return self.value

    @property
    def checked(self):
        return bool(self._control.value)


class GenericOptionElement(ElementAPI):

    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return self._control.attrib[attr]

    @property
    def text(self):
        return self._control.mech_item.get_labels()[0]._text

    @property
    def value(self):
        return self._control.value

    @property
    def selected(self):
        return self._control.mech_item._selected


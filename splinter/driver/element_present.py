class ElementPresentMixIn(object):
    ''' Support is_element_present_by_* methods for non-javascript drivers. '''

    def is_element_present_by_css(self, css_selector, wait_time=None):
        return bool(self.find_by_css(css_selector))

    def is_element_not_present_by_css(self, css_selector, wait_time=None):
        return not self.is_element_present_by_css(css_selector, wait_time)

    def is_element_present_by_xpath(self, xpath, wait_time=None):
        return bool(self.find_by_xpath(xpath))

    def is_element_not_present_by_xpath(self, xpath, wait_time=None):
        return not self.is_element_present_by_xpath(xpath, wait_time)

    def is_element_present_by_tag(self, tag, wait_time=None):
        return bool(self.find_by_tag(tag))

    def is_element_not_present_by_tag(self, tag, wait_time=None):
        return not self.is_element_present_by_tag(tag, wait_time)

    def is_element_present_by_name(self, name, wait_time=None):
        return bool(self.find_by_name(name))

    def is_element_not_present_by_name(self, name, wait_time=None):
        return not self.is_element_present_by_name(name, wait_time)

    def is_element_present_by_value(self, value, wait_time=None):
        return bool(self.find_by_value(value))

    def is_element_not_present_by_value(self, value, wait_time=None):
        return not self.is_element_present_by_value(value, wait_time)

    def is_element_present_by_text(self, text, wait_time=None):
        return bool(self.find_by_text(text))

    def is_element_not_present_by_text(self, text, wait_time=None):
        return not self.is_element_present_by_text(text, wait_time)

    def is_element_present_by_id(self, id, wait_time=None):
        return bool(self.find_by_id(id))

    def is_element_not_present_by_id(self, id, wait_time=None):
        return not self.is_element_present_by_id(id, wait_time)

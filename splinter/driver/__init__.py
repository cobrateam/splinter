from splinter.element_list import ElementList


class DriverAPI(object):
    @property
    def title(self):
        raise NotImplementedError

    @property
    def html(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    def visit(self, url):
        raise NotImplementedError

    def reload(self):
        raise NotImplementedError

    def get_alert(self):
        raise NotImplementedError

    def get_iframe(self, id):
        raise NotImplementedError

    def execute_script(self, script):
        raise NotImplementedError

    def evaluate_script(self, script):
        raise NotImplementedError

    def find_by_css(self, css_selector):
        raise NotImplementedError

    find_by_css_selector = find_by_css

    def find_by_xpath(self, xpath):
        raise NotImplementedError

    def find_by_name(self, name):
        raise NotImplementedError

    def find_by_id(self, id):
        raise NotImplementedError

    def find_by_tag(self, tag):
        raise NotImplementedError

    def find_link_by_href(self, href):
        raise NotImplementedError

    def find_link_by_text(self, text):
        raise NotImplementedError

    def find_option_by_value(self, value):
        raise NotImplementedError

    def find_option_by_text(self, text):
        raise NotImplementedError

    def wait_for_element(self, selector, timeout, interval):
        raise NotImplementedError

    def fill(self, name, value):
        raise NotImplementedError

    fill_in = fill
    attach_file = fill

    def choose(self, name):
        raise NotImplementedError

    def check(self, name):
        raise NotImplementedError

    def uncheck(self, name):
        raise NotImplementedError

    def select(self, name, value):
        raise NotImplementedError

    def click_link_by_href(self, href):
        return self.find_link_by_href(href).first.click()

    def click_link_by_text(self, text):
        return self.find_link_by_text(text).first.click()

    def within(self, context):
        return ElementList([], context, self)

    def quit(self):
        raise NotImplementedError

    def is_element_present(self, finder, selector, wait_time=None):
        raise NotImplementedError


class ElementAPI(object):

    def _get_value(self):
        raise NotImplementedError

    def _set_value(self, value):
        raise NotImplementedError

    value = property(_get_value, _set_value)

    def click(self):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def uncheck(self):
        raise NotImplementedError

    def mouseover(self):
        raise NotImplementedError

    @property
    def checked(self):
        raise NotImplementedError

    @property
    def visible(self):
        raise NotImplementedError

    def __getitem__(self, attribute):
        raise NotImplementedError

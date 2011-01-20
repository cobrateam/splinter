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

    def execute_script(self, script):
        raise NotImplementedError
        
    def evaluate_script(self, script):
        raise NotImplementedError

    def find_by_css_selector(self, css_selector):
        raise NotImplementedError
        
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

    def fill_in(self, name, value):
        raise NotImplementedError

    fill = fill_in
    attach_file = fill

    def choose(self, name):
        raise NotImplementedError
    
    def check(self, name):
        raise NotImplementedError

    def uncheck(self, name):
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
        
    def check(self):
        raise NotImplementedError
        
    def uncheck(self):
        raise NotImplementedError

    @property
    def checked(self):
        raise NotImplementedError
        
    @property
    def visible(self):
        raise NotImplementedError

    def __getitem__(self, attribute):
        raise NotImplementedError

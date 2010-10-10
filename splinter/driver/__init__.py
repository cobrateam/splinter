import os
import webbrowser

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

    def open_in_browser(self, path):
        webbrowser.open(path)
        
    def save_and_open_page(self):
                
        if not os.path.exists('/tmp/splinter'):
            os.mkdir('/tmp/splinter')
            
        tempfile = open('/tmp/splinter/splinter.html', 'w')
        tempfile.write(self.html)
        tempfile.close()
        
        tempfile_path = os.path.abspath(tempfile.name)
        
        self.open_in_browser(tempfile_path)
         
    def find(self, css_selector=None,
                   xpath=None,
                   name=None,
                   id=None,
                   tag=None):
        raise NotImplementedError

    def find_link(self, text=None, href=None):
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

    def __getitem__(self, attribute):
        raise NotImplementedError

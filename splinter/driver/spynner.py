import spynner
from splinter.driver import DriverAPI

class Spynner(DriverAPI):

    def __init__(self):
        self._browser = spynner.Browser()

    def visit(self, url):
        self._browser.load(url)

class Page(object):
    
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
    
    @property
    def title(self):
        return self.driver.title

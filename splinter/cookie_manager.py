class CookieManagerAPI(object):

    def add(self, cookies):
        raise NotImplementedError

    def delete(self, cookie=None):
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError

    def __eq__(self, other_object):
        raise NotImplementedError

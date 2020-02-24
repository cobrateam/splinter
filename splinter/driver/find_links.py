class FindLinks(object):
    """Contains methods for finding links in a parent.

    Accessed through the browser object or an element via the links attribute.

    Example:

        browser.links.find_by_href('foobar')

    """
    def __init__(self, parent):
        self.parent = parent

    def find_by_href(self, href):
        return self.parent.find_by_xpath(
            '//a[@href="{}"]'.format(href),
            original_find="link by href",
            original_query=href,
        )

    def find_by_partial_href(self, partial_href):
        return self.parent.find_by_xpath(
            '//a[contains(@href, "{}")]'.format(partial_href),
            original_find="link by partial href",
            original_query=partial_href,
        )

    def find_by_partial_text(self, partial_text):
        return self.parent.find_by_xpath(
            '//a[contains(normalize-space(.), "{}")]'.format(partial_text),
            original_find="link by partial text",
            original_query=partial_text,
        )

    def find_by_text(self, text):
        return self.parent.find_by_xpath(
            '//a[text()="{}"]'.format(text),
            original_find="link by text",
            original_query=text,
        )

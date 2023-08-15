from splinter.element_list import ElementList


class FindLinks:
    """Contains methods for finding links in a parent.

    Accessed through the browser object or an element via the links attribute.

    Example:

        browser.links.find_by_href('foobar')

    """

    def __init__(self, parent) -> None:
        self.parent = parent

    def find_by_href(self, href: str) -> ElementList:
        return self.parent.find_by_xpath(
            f'//a[@href="{href}"]',
            original_find="link by href",
            original_query=href,
        )

    def find_by_partial_href(self, partial_href: str) -> ElementList:
        return self.parent.find_by_xpath(
            f'//a[contains(@href, "{partial_href}")]',
            original_find="link by partial href",
            original_query=partial_href,
        )

    def find_by_partial_text(self, partial_text: str) -> ElementList:
        return self.parent.find_by_xpath(
            f'//a[contains(normalize-space(.), "{partial_text}")]',
            original_find="link by partial text",
            original_query=partial_text,
        )

    def find_by_text(self, text: str) -> ElementList:
        return self.parent.find_by_xpath(
            f'//a[text()="{text}"]',
            original_find="link by text",
            original_query=text,
        )

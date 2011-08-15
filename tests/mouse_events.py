class MouseEventsTest(object):

    def test_double_click(self):
        "double click should shows a hidden element"
        button = self.browser.find_by_css(".db-button").first
        button.double_click()
        assert self.browser.find_by_css(".should-be-visible-after-double-click").visible
    def test_mouse_hover(self):
        "mouse hover should shows a hidden element"
        button = self.browser.find_by_css(".hover-button").first
        button.hover()
        assert self.browser.find_by_css(".should-be-visible-after-mouse-hover").visible

    def test_right_click(self):
        "right click should shows a hidden element"
        button = self.browser.find_by_css(".right-button").first
        button.right_click()
        assert self.browser.find_by_css(".should-be-visible-after-right-click").visible


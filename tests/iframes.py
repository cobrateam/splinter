from nose.tools import assert_equals

class IFrameElementsTest(object):

    def test_can_work_on_iframes(self):
        """can work on iframes and switch back to the page"""
        with self.browser.get_iframe('iframemodal') as frame:
            value = frame.find_by_tag('h1').first.value
            assert_equals(value, 'IFrame Example Header')
        value = self.browser.find_by_tag('h1').first.value
        assert_equals(value, 'Example Header')
from nose.tools import assert_equals

class IFrameElementsTest(object):

    def test_can_change_frames(self):
        self.browser.switch_to_frame('iframemodal')
        value = self.browser.find_by_tag('h1').first.value
        assert_equals(value, 'IFrame Example Header')

    def test_can_change_frames_back(self):
        self.browser.switch_to_frame('iframemodal')
        self.browser.switch_to_frame(None)
        value = self.browser.find_by_tag('h1').first.value
        assert_equals(value, 'Example Header')

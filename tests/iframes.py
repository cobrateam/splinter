from nose.tools import assert_equals

class IFrameElementsTest(object):

    def test_can_change_frames_using(self):
        self.browser.switch_to_frame('iframemodal')
        value = self.browser.find_by_tag('h1').first.value
        assert_equals(value, 'IFrame Example Header')

    def test_can_change_frames_back(self):
        self.browser.switch_to_frame('iframemodal')
        self.browser.switch_to_frame(None)
        value = self.browser.find_by_tag('h1').first.value
        assert_equals(value, 'Example Header')

    def test_can_change_frames_using_new_with_approach(self):
        """can change frames using new with's approach"""
        with self.browser.get_iframe('iframemodal') as frame:
            value = frame.find_by_tag('h1').first.value
            assert_equals(value, 'IFrame Example Header')
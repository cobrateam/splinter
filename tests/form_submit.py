import json

class FormSubmitTest(object):
    def test_can_submit_a_form_with_multiple_input_submit(self):
        "should be able to submit a form with multiple input[type=submit]"

        for value in ("X", "Y"):
            input_value = "Input %s" % value
            with self.subTest("Value '%s'" % input_value):
                self.browser.visit("/echo")
                self.browser.find_by_value(input_value).first.click()
                j = json.loads(self.browser.html)
                self.assertEqual(j["the-input-submit"], input_value)

    def test_can_submit_a_form_with_multiple_buttons(self):
        "should be able to submit a form with multiple buttons"

        for value in ("X", "Y"):
            button_value = "Button %s" % value
            with self.subTest("Button '%s'" % button_value):
                self.browser.visit("/echo")
                self.browser.find_by_value(button_value).first.click()
                j = json.loads(self.browser.html)
                self.assertEqual(j["the-button"], button_value)

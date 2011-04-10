from nose.tools import assert_equals

class AlertTests(object):
    
    def should_access_alerts_and_accept_them(self):
        self.browser.visit('http://localhost:5000/alert')
        self.browser.find_by_tag('h1').first.click()
        alert = self.browser.get_alert()
        assert_equals(alert.text, 'This is an alert example.')
        alert.accept()
        
    def should_access_prompts_and_be_able_to_fill_then(self):
        self.browser.visit('http://localhost:5000/alert')
        self.browser.find_by_tag('h2').first.click()
        
        alert = self.browser.get_alert()
        assert_equals(alert.text, 'What is your name?')
        alert.fill_with('Splinter')
        alert.accept()
        
        response = self.browser.get_alert()
        assert_equals(response.text, 'Splinter')
        response.accept()
        
    def should_access_alerts_using_with(self):
        "should access alerts using 'with' statement"
        self.browser.visit('http://localhost:5000/alert')
        self.browser.find_by_tag('h1').first.click()
        with self.browser.get_alert() as alert:
            assert_equals(alert.text, 'This is an alert example.')
            alert.accept()
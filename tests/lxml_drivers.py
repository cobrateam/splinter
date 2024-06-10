import os

import pytest

from .fake_webapp import EXAMPLE_APP


class LxmlDriverTests:
    def test_cant_switch_to_frame(self):
        """lxml-based drivers should not be able to switch to frames"""
        with pytest.raises(NotImplementedError) as err:
            self.browser.get_iframe("frame_123")
            self.fail()

        assert f"{self.browser.driver_name.lower()} doesn't support frames." == err.value.args[0]

    def test_attach_file(self):
        """should provide a way to change file field value"""
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "mockfile.txt",
        )
        self.browser.attach_file("file", file_path)
        self.browser.find_by_name("upload").click()

        html = self.browser.html
        assert "text/plain" in html
        with open(file_path) as f:
            assert f.read() in html

    def test_forward_to_none_page(self):
        """lxml-based drivers should not fail when trying to forward to none"""
        browser = self.get_new_browser()
        browser.visit(EXAMPLE_APP)
        browser.forward()
        assert EXAMPLE_APP == browser.url
        browser.quit()

    def test_can_clear_password_field_content(self):
        """lxml-based drivers should not be able to clear"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("password").first.clear()

    def test_can_clear_tel_field_content(self):
        """lxml-based drivers should not be able to clear"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("telephone").first.clear()

    def test_can_clear_text_field_content(self):
        """lxml-based drivers should not be able to clear"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("query").first.clear()

    def test_can_clear_textarea_content(self):
        """lxml-based drivers should not be able to clear"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("description").first.clear()

    def test_can_clear_search_content(self):
        """lxml-based drivers should not be able to clear"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("search_keyword").first.clear()

    def test_can_clear_url_content(self):
        """lxml-based drivers should not be able to clear"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("url_input").first.clear()

    def test_simple_type(self):
        """
        lxml-based drivers won't support type method
        because it doesn't interact with JavaScript
        """
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("query").type("with type method")

    def test_simple_type_on_element(self):
        """
        lxml-based drivers won't support type method
        because it doesn't interact with JavaScript
        """
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("query").type("with type method")

    def test_slowly_typing(self):
        """
        lxml-based drivers won't support type method
        because it doesn't interact with JavaScript
        """
        with pytest.raises(NotImplementedError):
            self.browser.find_by_name("query").type("with type method", slowly=True)

    def test_slowly_typing_on_element(self):
        """
        lxml-based drivers won't support type method
        on element because it doesn't interac with JavaScript
        """
        with pytest.raises(NotImplementedError):
            query = self.browser.find_by_name("query")
            query.type("with type method", slowly=True)

    def test_cant_mouseover(self):
        """lxml-based drivers should not be able to put the mouse over the element"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_css("#visible").mouse_over()

    def test_cant_mouseout(self):
        """lxml-based drivers should not be able to mouse out of an element"""
        with pytest.raises(NotImplementedError):
            self.browser.find_by_css("#visible").mouse_out()

    def test_finding_all_links_by_non_ascii_text(self):
        """lxml-based drivers should find links by non ascii text"""
        non_ascii_encodings = {
            "pangram_pl": "Jeżu klątw, spłódź Finom część gry hańb!",
            "pangram_ja": "天 地 星 空",
            "pangram_ru": "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!",  # NOQA RUF001
            "pangram_eo": "Laŭ Ludoviko Zamenhof bongustas freŝa ĉeĥa manĝaĵo kun spicoj.",
        }
        for key, text in non_ascii_encodings.items():
            link = self.browser.links.find_by_text(text)
            assert key == link["id"]

    def test_links_with_nested_tags_xpath(self):
        links = self.browser.find_by_xpath('//a/span[text()="first bar"]/..')
        assert len(links) == 1, 'Found more than one link with a span with text "BAR ONE". %s' % [
            item.outer_html for item in links
        ]

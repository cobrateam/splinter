from typing import Union

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class Keyboard:
    """Representation of a keyboard.

    Requires a WebDriver instance to use.

    Arguments:
        driver: The WebDriver instance to use.
        element: Optionally, a WebElement to act on.
    """

    def __init__(self, driver, element: Union[WebElement, None] = None) -> None:
        self.driver = driver

        self.element = element

    def _resolve_key_down_action(self, action_chain: ActionChains, key: str) -> ActionChains:
        """Given the string <key>, select the correct action for key down.

        For modifier keys, use ActionChains.key_down().
        For other keys, use ActionChains.send_keys() or ActionChains.send_keys_to_element()
        """
        key_value = getattr(Keys, key, None)

        if key_value:
            chain = action_chain.key_down(key_value, self.element)
        elif self.element:
            chain = action_chain.send_keys_to_element(self.element, key)
        else:
            chain = action_chain.send_keys(key)

        return chain

    def _resolve_key_up_action(self, action_chain: ActionChains, key: str) -> ActionChains:
        """Given the string <key>, select the correct action for key up.

        For modifier keys, use ActionChains.key_up().
        For other keys, use ActionChains.send_keys() or ActionChains.send_keys_to_element()
        """
        key_value = getattr(Keys, key, None)

        chain = action_chain
        if key_value:
            chain = action_chain.key_up(key_value, self.element)

        return chain

    def down(self, key: str) -> "Keyboard":
        """Hold down on a key.

        Arguments:
            key: The name of a key to hold.

        Example:

            >>> b = Browser()
            >>> Keyboard(b.driver).down('SHIFT')
        """
        chain = ActionChains(self.driver)
        chain = self._resolve_key_down_action(chain, key)
        chain.perform()
        return self

    def up(self, key: str) -> "Keyboard":
        """Release a held key.

        If <key> is not held down, this method has no effect.

        Arguments:
            key: The name of a key to release.

        Example:

            >>> b = Browser()
            >>> Keyboard(b.driver).down('SHIFT')
            >>> Keyboard(b.driver).up('SHIFT')
        """
        chain = ActionChains(self.driver)
        chain = self._resolve_key_up_action(chain, key)
        chain.perform()
        return self

    def press(self, key_pattern: str, delay: int = 0) -> "Keyboard":
        """Hold and release a key pattern.

        Key patterns are strings of key names separated by '+'.
        The following are examples of key patterns:
        - 'CONTROL'
        - 'CONTROL+a'
        - 'CONTROL+a+BACKSPACE+b'

        Arguments:
            key_pattern: Pattern of keys to hold and release.
            delay: Time, in seconds, to wait between the hold and release.

        Example:

            >>> b = Browser()
            >>> Keyboard(b.driver).press('CONTROL+a')
        """
        keys_names = key_pattern.split("+")

        chain = ActionChains(self.driver)

        for item in keys_names:
            chain = self._resolve_key_down_action(chain, item)

        if delay:
            chain = chain.pause(delay)

        for item in keys_names:
            chain = self._resolve_key_up_action(chain, item)

        chain.perform()

        return self

from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass
class Config:
    """Standard interface for basic and nearly universal driver flags.

    The primary purpose of Config is to reduce the burden on the user to import
    Selenium Options objects for common operations. The second purpose is to
    avoid argument bloat and drift for the various drivers.

    Both Splinter Config and Selenium Options can be used together.
    Config will override Options, if applicable.

    Config is not a complete replacement for Selenium Options.
    For unique and esoteric functionality that is exclusive to one web browser,
    Selenium Options should still be used. The purpose of Config is to expose
    a universal interface for common functionality, not try to capture all
    of it.

    Example:

        >>> from splinter import Browser, Config
        >>>
        >>>
        >>> my_config = Config(fullscreen=True)
        >>> my_browser = Browser(config=my_config)


    Attributes:
        extensions: Add extensions to the browser.
            The full path to each extension must be included.
            When the browser is closed extensions will be deleted from
            the profile, even if the profile is not a temporary one.

        fullscreen: Launch the browser in fullscreen mode.

        headless: Launch the browser in headless mode.
            Requires Chrome 59+ or Firefox 55+.

        incognito: Launch the browser in incognito mode.

        user_agent: Set a custom user_agent.
    """

    extensions: Optional[List[str]] = None
    fullscreen: Optional[bool] = False
    headless: Optional[bool] = False
    incognito: Optional[bool] = False
    user_agent: Optional[str] = None

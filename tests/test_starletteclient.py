from splinter import Browser
from fastapi import FastAPI

def test_starlette_client():
    app = FastAPI()
    browser = Browser("starlette", app=app)  # Create the browser instance

    browser.visit("http://example.com")  # Try to visit a page
    assert browser.title == "Example Domain"  # Check if title is correct

    browser.quit()

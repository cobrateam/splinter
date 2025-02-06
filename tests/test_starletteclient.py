from fastapi import FastAPI
from starlette.responses import HTMLResponse
from splinter import Browser
import pytest
import logging

# ----- Step 1: Define a minimal FastAPI application -----
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # Return an HTML page with a title set to "Example Domain"
    return """
    <!doctype html>
    <html>
      <head>
        <title>Example Domain</title>
      </head>
      <body>
        <h1>Welcome to Example Domain</h1>
        <p>This is a sample page for testing.</p>
      </body>
    </html>
    """

# ----- Step 2: Write the test function using the StarletteClient -----
def test_starlette_client():
    browser = Browser("starlette", app=app)
    
    try:
        # Visit the local route "/" served by our FastAPI app.
        browser.visit("/")  
        
        # Check the title to match the expected "Example Domain"
        assert browser.title == "Example Domain"
        
        # Assert that some content is present on the page (the header in this case)
        assert browser.is_text_present("Welcome to Example Domain")
        
        # Check for the presence of a paragraph (new test case)
        assert browser.is_text_present("This is a sample page for testing.")
        
        # Optionally, check that the number of <h1> tags is exactly one
        assert len(browser.find_by_tag("h1")) == 1

    except ValueError as e:
        logging.error(f"Test failed: {e}")  # Log the error if we catch it

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    finally:
        # Clean up (quit() is a no-op for the StarletteClient)
        browser.quit()

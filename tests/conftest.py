from playwright.sync_api import sync_playwright
import pytest


BASE_URL = "http://127.0.0.1:8001/#login"
VIDEO_PATH = "videos"

# @pytest.fixture(scope="session")
# def browser_instance():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, slow_mo=2000)
#         yield browser
#         browser.close()

# @pytest.fixture(scope="session")
# def page(browser_instance):
#     context = browser_instance.new_context(
#         record_video_dir=VIDEO_PATH,
#         record_video_size={"width":1280, "height":720}
#     )
#     page = context.new_page()
#     page.set_default_timeout(30000)
#     yield page
#     context.close()

# @pytest.fixture(scope="session")
# def base_url():
#     return BASE_URL

@pytest.fixture(scope="session")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8001/#login")
        yield page
        browser.close()

@pytest.fixture
def read_test_data():
    import json
    with open("test_data.json", "r") as file:
        data = json.load(file)
    return data
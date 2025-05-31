import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.youtube.com/results?search_query=time")
    page.locator("a").filter(has_text=":00:03 10:00:03 Now playing").click()
    page.get_by_role("button", name="Skip", exact=True).click()
    page.locator("video").click(button="right")
    page.get_by_text("Stats for nerds").click()
    page.locator("video").click()
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")
    page.get_by_label("YouTube Video Player").press("ArrowRight")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

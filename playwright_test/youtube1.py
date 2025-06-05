import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.youtube.com/")
    page.get_by_role("combobox", name="Search").click()
    page.get_by_role("combobox", name="Search").fill("timeless")
    page.get_by_role("combobox", name="Search").press("Enter")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.locator("body").press("ArrowRight")
    page.get_by_text("4:17 4:17 Now playing Watch").click()
    page.locator("#movie_player video").click()
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.get_by_text("19:59 19:59 Now playing Watch").click()
    page.locator("#movie_player video").click()
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")
    page.locator("#movie_player").press("ArrowRight")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

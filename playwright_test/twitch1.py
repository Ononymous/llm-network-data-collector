import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome", headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twitch-tools.rootonline.de/random_channel_previews.php")
    page.locator("iframe").content_frame.get_by_role("button", name="Settings").click()
    page.locator("iframe").content_frame.get_by_role("menuitem", name="Advanced").click()
    page.locator("iframe").content_frame.get_by_role("checkbox", name="Video Stats").check()
    page.locator("iframe").content_frame.get_by_label("Play Session ID").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Serving ID").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Play Session ID").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Backend Version").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Render Surface").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Latency Mode").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Protocol").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Codecs").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Latency To Broadcaster").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Buffer Size").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Skipped Frames").click()
    page.locator("iframe").content_frame.get_by_role("status", name="FPS").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Bandwidth Estimate").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Download Bitrate").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Viewport Resolution").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Render Resolution").click()
    page.locator("iframe").content_frame.get_by_role("status", name="Download Resolution").click()
    page.locator("iframe").content_frame.locator(".simplebar-content").click()
    page.locator("iframe").content_frame.locator(".simplebar-content").click()
    page.locator("iframe").content_frame.get_by_role("button", name="Close video stats").click()
    page.goto("https://twitch-tools.rootonline.de/random_channel_previews.php")
    page.locator("iframe").content_frame.get_by_role("button", name="Intended for certain audiences").click()
    page.goto("https://twitch-tools.rootonline.de/random_channel_previews.php")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

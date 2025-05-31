import re
import time
import random
import json
from playwright.sync_api import Playwright, sync_playwright, expect, Error

# Your existing list of nouns…
nouns = [
    # English
    "time", "year", "people", "way", "day", "man", "thing", "woman", "life", "child",
    "world", "school", "state", "family", "student", "group", "country", "problem", "hand", "part",

    # Spanish
    "tiempo", "año", "día", "persona", "hombre", "mujer", "mano", "parte", "país", "lugar",
    "trabajo", "vida", "momento", "forma", "caso", "grupo", "problema", "punto", "gobierno", "empresa",

    # French
    "temps", "homme", "façon", "gens", "vie", "jour", "travail", "appel", "nuit", "maison",
    "pensée", "argent", "nom", "père", "mec", "place", "femme", "enfant", "monde", "école",

    # Chinese (Simplified)
    "人", "事", "时间", "朋友", "孩子", "中国", "家", "学生", "问题", "男人",
    "女人", "学校", "工作", "钱", "世界", "书", "生活", "水", "国家", "老师",

    # Japanese
    "人", "子供", "大人", "男", "女", "生活", "友達", "家族", "学生", "先生",
    "社員", "学校", "会社", "駅", "空港", "家", "アパート", "車", "電車", "時間",

    # Hindi
    "नाम", "घर", "समय", "मनुष्य", "पुस्तक", "दिन", "रात", "सप्ताह", "महीना", "साल",
    "शहर", "गांव", "देश", "जल", "अन्न", "आदमी", "औरat", "बच्चा", "पिता", "माता",

    # Korean
    "사람", "것", "시간", "날", "집", "눈", "생각", "아이", "년", "사랑",
    "친구", "말", "학교", "일", "몸", "마음", "세상", "문제", "엄마", "아빠",

    # Russian
    "человек", "друг", "ребёнок", "женщина", "мужчина", "время", "год", "день", "дело", "рука",
    "глаз", "жизнь", "голова", "дом", "слово", "место", "лицо", "сторона", "нога", "работа",

    # Arabic
    "الله", "كتاب", "رجل", "امرأة", "طفل", "عين", "يد", "رأس", "قدم", "سماء",
    "أرض", "بحر", "نار", "شمس", "قمر", "نجم", "بيت", "مدينة", "شارع", "سيارة",

    # German
    "Zeit", "Jahr", "Mensch", "Tag", "Mann", "Frau", "Kind", "Hand", "Auge", "Weg",
    "Freund", "Haus", "Auto", "Arbeit", "Stadt", "Leben", "Problem", "Moment", "Land", "Platz",

    # Portuguese
    "coisa", "tempo", "vida", "dia", "mão", "ano", "olho", "vez", "homem", "parte",
    "mulher", "lugar", "trabalho", "semana", "problema", "ponto", "hora", "pessoa", "forma", "caso",

    # Italian
    "anno", "giorno", "uomo", "volta", "vita", "mano", "occhio", "donna", "casa", "mondo",
    "tempo", "modo", "parte", "amico", "persona", "problema", "notte", "punto", "cuore", "padre"
]

class YouTubeVideoPlayerTest:
    """
    A Playwright test class for simulating YouTube video playback with
    stats collection and random user interactions.
    """

    BASE_URL = "https://www.youtube.com/"
    SEARCH_URL_TEMPLATE = "https://www.youtube.com/results?search_query={}"
    DEFAULT_TIMEOUT = 15000  # Default timeout for Playwright operations
    SHORT_TIMEOUT = 5000     # Shorter timeout for specific elements
    AD_CHECK_TIMEOUT = 2000  # Timeout for checking ad elements

    def __init__(self, headless: bool = False, browser_type: str = "firefox"):
        """
        Initializes the test with browser settings.
        :param headless: Whether to run the browser in headless mode.
        :param browser_type: Type of browser to use (chromium, firefox, webkit).
        """
        self.headless = headless
        self.browser_type = browser_type
        self.telemetry = [] # To store collected data for all videos

    def _setup(self, playwright: Playwright):
        """
        Sets up the browser and page for the test.
        :param playwright: The Playwright instance.
        """
        # Launch the specified browser type as per user guidelines
        if self.browser_type == "chromium":
            self.browser = playwright.chromium.launch(headless=self.headless)
        elif self.browser_type == "webkit":
            self.browser = playwright.webkit.launch(headless=self.headless)
        else: # Default to firefox, as per recorded code example
            self.browser = playwright.firefox.launch(headless=self.headless)

        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def _teardown(self):
        """
        Closes the browser context and browser.
        """
        if hasattr(self, 'context'):
            self.context.close()
        if hasattr(self, 'browser'):
            self.browser.close()

    def _perform_random_video_action(self, page):
        """
        Performs a random action on the video player (play/pause, seek forward/backward).
        Adjusted probabilities: 'seek_forward' is now more likely than 'play_pause' or 'seek_backward'.
        :param page: The Playwright page object.
        """
        # Adjusted probabilities to have less seek back and pause.
        # 'seek_forward' is 3 times more likely than 'play_pause' or 'seek_backward'.
        actions = ["seek_forward"] * 3 + ["play_pause"] * 1 + ["seek_backward"] * 1
        action = random.choice(actions)

        # Click the video element to ensure it's in focus for keyboard shortcuts
        # Use a more specific locator like #player or #movie_player for robustness
        video_player_locator = page.locator("#movie_player")
        try:
            video_player_locator.click(timeout=self.SHORT_TIMEOUT)
        except Error:
            # Player might not be ready or clickable yet, skip action if not responsive
            print("      ⚠️ Could not click video player for action, skipping random action.")
            return

        if action == "play_pause":
            # Press 'k' to toggle play/pause
            page.keyboard.press("k")
            time.sleep(random.uniform(0.5, 1.5)) # Small delay after action
            print("      • Action: Play/Pause toggled")
        elif action == "seek_forward":
            # Press 'l' multiple times to fast forward by 10 seconds per press
            presses = random.randint(1, 3) # Fast forward by 10-30 seconds
            for _ in range(presses):
                page.keyboard.press("l")
            time.sleep(random.uniform(0.5, 1.5))
            print(f"      • Action: Seek forward by {presses * 10} seconds")
        elif action == "seek_backward":
            # Press 'j' multiple times to rewind by 10 seconds per press
            presses = random.randint(1, 3) # Rewind by 10-30 seconds
            for _ in range(presses):
                page.keyboard.press("j")
            time.sleep(random.uniform(0.5, 1.5))
            print(f"      • Action: Seek backward by {presses * 10} seconds")

    def _get_video_stats(self, page) -> str:
        """
        Attempts to get the innerText of the Stats for Nerds panel.
        :param page: The Playwright page object.
        :return: The stats text or an empty string if not found or visible.
        """
        try:
            stats_panel = page.locator(".html5-video-info-panel")
            # Ensure the panel is visible before attempting to get its text
            stats_panel.wait_for(state="visible", timeout=self.SHORT_TIMEOUT)
            return stats_panel.inner_text()
        except Error:
            return "" # Return empty string if panel is not visible or an error occurs

    def _skip_ads_if_present(self):
        """
        Attempts to skip YouTube ads if present.
        Looks for 'Skip Ad' button and clicks it.
        """
        print("  Checking for ads...")
        try:
            # Wait for a short duration to allow ads to load
            self.page.wait_for_timeout(1000) # Small initial wait for ad elements to appear

            # Try to click the 'Skip Ad' button by its common class name
            skip_button_locator = self.page.locator("button.ytp-ad-skip-button")
            # Or by text content, which might be more robust for localization or variations
            skip_text_locator = self.page.get_by_text("Skip Ad")

            # Prioritize clicking the button by its class, then by text
            if skip_button_locator.is_visible():
                skip_button_locator.click(timeout=self.AD_CHECK_TIMEOUT)
                print("    ✅ Skipped ad via button class.")
                self.page.wait_for_timeout(500) # Wait a bit for the ad to transition
                return True
            elif skip_text_locator.is_visible():
                skip_text_locator.click(timeout=self.AD_CHECK_TIMEOUT)
                print("    ✅ Skipped ad via text content.")
                self.page.wait_for_timeout(500) # Wait a bit for the ad to transition
                return True
            else:
                print("    ➡️ No skippable ad found or ad already finished.")
                return False
        except Error as e:
            # This catch is broad, but specifically for Playwright errors like timeout
            print(f"    ⚠️ Error checking for ads: {e}")
            return False
        except Exception as e:
            # Catch any other unexpected errors during ad skipping
            print(f"    ⚠️ An unexpected error occurred during ad check: {e}")
            return False

    def run_tests(self, num_videos: int, browser_type: str = "firefox", headless: bool = False):
        """
        Executes the YouTube video playback test for a specified number of videos.
        :param num_videos: Number of random videos to process.
        :param browser_type: Type of browser to use (chromium, firefox, webkit).
        :param headless: Whether to run the browser in headless mode.
        """
        self.browser_type = browser_type
        self.headless = headless

        # Use sync_playwright context manager to manage Playwright resources
        with sync_playwright() as p:
            self._setup(p) # Setup browser and page before starting tests

            for i in range(num_videos):
                print(f"\n▶️ Processing Video {i+1}/{num_videos}")
                video_telemetry = {} # Data for the current video iteration

                try:
                    # 1) Pick and search a random noun
                    query = random.choice(nouns)
                    print(f"  🔍 Searching for: '{query}'")
                    self.page.goto(self.SEARCH_URL_TEMPLATE.format(query), timeout=self.DEFAULT_TIMEOUT)
                    # Wait for network to be idle, indicating page content has likely loaded
                    self.page.wait_for_load_state("networkidle", timeout=self.DEFAULT_TIMEOUT)

                    # 2) Click the first video result
                    first_video_locator = self.page.locator("a#video-title").first
                    href = None
                    try:
                        # Wait for the video title link to be attached to the DOM
                        first_video_locator.wait_for(state="attached", timeout=self.SHORT_TIMEOUT)
                        href = first_video_locator.get_attribute("href")
                    except Error:
                        print(f"  ⚠️ No video results found for '{query}', skipping this video.")
                        continue # Skip to next video if no result element is found

                    if not href or not href.startswith("/watch?v="):
                        print(f"  ⚠️ Invalid video link found for '{query}' (href: {href}), skipping.")
                        continue

                    video_url = self.BASE_URL + href
                    print(f"  🎬 Navigating to: {video_url}")
                    self.page.goto(video_url, timeout=self.DEFAULT_TIMEOUT)

                    # 3) Skip ads if any
                    self._skip_ads_if_present()

                    # 4) Wait for the video element to be present and the player to be visible
                    self.page.wait_for_selector("video", state="attached", timeout=self.DEFAULT_TIMEOUT)
                    self.page.locator("#movie_player").wait_for(state="visible", timeout=self.DEFAULT_TIMEOUT)

                    # 5) Get the full duration of the video
                    duration = self.page.evaluate("() => document.querySelector('video').duration")
                    if not isinstance(duration, (int, float)) or duration <= 0:
                        print(f"  ⚠️ Could not get valid video duration for '{query}', skipping.")
                        continue # Skip if duration is invalid or zero

                    # Pick a random watch time (at least 5 seconds, max 90% of duration or 120s, whichever is smaller)
                    max_watch_time = min(duration * 0.9, 120)
                    watch_time = random.uniform(5, max_watch_time) # Watch at least 5 seconds
                    print(f"  ⏱ Watching for {watch_time:.1f}s out of {duration:.1f}s")

                    video_telemetry["video_url"] = video_url
                    video_telemetry["query"] = query
                    video_telemetry["duration"] = duration
                    video_telemetry["watched"] = watch_time
                    video_telemetry["stats_collections"] = [] # List to store multiple stats snapshots

                    # 6) Open Stats for nerds panel
                    video_player_area = self.page.locator("#player")
                    try:
                        # Ensure the player area is visible then right-click its center
                        video_player_area.wait_for(state="visible", timeout=self.SHORT_TIMEOUT)
                        box = video_player_area.bounding_box()
                        if box:
                            self.page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, button="right")
                            time.sleep(1) # Give time for the context menu to appear

                        # Click on "Stats for nerds" option in the context menu
                        nerds_option = self.page.get_by_text("Stats for nerds")
                        nerds_option.wait_for(state="visible", timeout=self.SHORT_TIMEOUT)
                        nerds_option.click()
                        # Wait for the stats panel itself to become visible
                        self.page.locator(".html5-video-info-panel").wait_for(state="visible", timeout=self.SHORT_TIMEOUT)
                        print("  📊 'Stats for nerds' panel opened.")
                    except Error as e:
                        print(f"  ⚠️ Could not open 'Stats for nerds' for '{query}': {e}")
                        # Continue with the test even if stats panel fails to open,
                        # but stats_collections will contain "Not Available" entries.
                        pass

                    # 7) Loop to collect stats and perform random actions
                    # Collect stats approximately once per second and perform random actions intermittently.
                    
                    start_watching_time = time.time()
                    STAT_COLLECTION_INTERVAL = 1.0 # Target interval for collecting stats in seconds

                    while (time.time() - start_watching_time) < watch_time:
                        current_interval_start = time.time()
                        
                        # Decide if a random user action should be performed in this interval (e.g., 30% chance)
                        if random.random() < 0.3:
                            self._perform_random_video_action(self.page)
                        
                        # Calculate time spent on actions (including their internal sleep) within this interval
                        time_spent_on_actions = time.time() - current_interval_start
                        
                        # Determine how much more to sleep to reach the target STAT_COLLECTION_INTERVAL
                        # Ensure we don't sleep past the total target watch_time
                        remaining_sleep_needed = STAT_COLLECTION_INTERVAL - time_spent_on_actions
                        
                        # Only sleep if remaining time is positive and doesn't exceed total remaining watch time
                        if remaining_sleep_needed > 0:
                            max_total_sleep_allowed = watch_time - (time.time() - start_watching_time)
                            actual_sleep_duration = min(remaining_sleep_needed, max_total_sleep_allowed)
                            if actual_sleep_duration > 0:
                                time.sleep(actual_sleep_duration)
                        
                        # Collect stats at the current point in time
                        current_stats = self._get_video_stats(self.page)
                        timestamp_since_start = time.time() - start_watching_time
                        
                        if current_stats:
                            video_telemetry["stats_collections"].append({
                                "timestamp_watched": timestamp_since_start,
                                "stats": current_stats.strip()
                            })
                            print(f"    • Stats collected at {timestamp_since_start:.1f}s.")
                            # Print only the first line of stats for brevity
                            print("      " + current_stats.strip().split('\n')[0] + "...")
                        else:
                            print(f"    • Stats not available at {timestamp_since_start:.1f}s.")
                            video_telemetry["stats_collections"].append({
                                "timestamp_watched": timestamp_since_start,
                                "stats": "Not Available"
                            })
                        
                        # If the total elapsed time has reached or exceeded `watch_time` after this iteration, break
                        if (time.time() - start_watching_time) >= watch_time:
                            break

                    # Ensure video is playing at the end of the loop if it was paused
                    try:
                        is_paused = self.page.evaluate("() => document.querySelector('video').paused")
                        if is_paused:
                            self.page.keyboard.press("k") # Press 'k' to resume playback
                            print("  ▶️ Resumed playback after stats collection.")
                    except Error:
                        print("  ⚠️ Could not verify video playing state.")

                    # Ensure total watched time approximately matches the target watch_time
                    # This final sleep ensures we hit the target watch_time if the loop ended slightly early
                    time_elapsed_actual = time.time() - start_watching_time
                    if time_elapsed_actual < watch_time:
                         remaining_total_sleep = watch_time - time_elapsed_actual
                         if remaining_total_sleep > 0:
                            print(f"  ⏳ Waiting for remaining {remaining_total_sleep:.1f}s to reach target watch time.")
                            time.sleep(remaining_total_sleep)

                    self.telemetry.append(video_telemetry)
                    time.sleep(random.uniform(1, 3)) # Optional small pause between videos

                except Error as e:
                    print(f"  ❌ Playwright error occurred processing video '{query}': {e}")
                    # Capture partial telemetry even on Playwright errors
                    # Ensure video_telemetry has basic info if error occurs very early
                    if "video_url" not in video_telemetry:
                        video_telemetry["video_url"] = "N/A"
                        video_telemetry["query"] = query if 'query' in locals() else "N/A"
                    self.telemetry.append({**video_telemetry, "error": f"Playwright Error: {str(e)}"})
                    time.sleep(random.uniform(1, 2)) # Small pause before next iteration
                except Exception as e:
                    print(f"  ❌ An unexpected error occurred processing video '{query}': {e}")
                    # Capture partial telemetry on any other unexpected errors
                    # Ensure video_telemetry has basic info if error occurs very early
                    if "video_url" not in video_telemetry:
                        video_telemetry["video_url"] = "N/A"
                        video_telemetry["query"] = query if 'query' in locals() else "N/A"
                    self.telemetry.append({**video_telemetry, "error": f"Unexpected Error: {str(e)}"})
                    time.sleep(random.uniform(1, 2))

            self._teardown() # Teardown browser and page after all videos are processed

        # 8) Output results
        print("\n\n=== Test Summary ===")
        print(f"💾 Collected telemetry for {len(self.telemetry)} videos.")
        # Print results to console
        print(json.dumps(self.telemetry, indent=2, ensure_ascii=False))

        # Write results to a JSON file
        output_filename = "youtube_telemetry.json"
        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(self.telemetry, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {output_filename}")
        except IOError as e:
            print(f"Error saving results to file '{output_filename}': {e}")


# Main execution block
if __name__ == "__main__":
    # Get number of videos to process from user input
    try:
        num_videos_to_process = int(input("How many random videos should I process? "))
        if num_videos_to_process <= 0:
            print("Please enter a positive number of videos (e.g., 5).")
            exit()
    except ValueError:
        print("Invalid input. Please enter a valid integer number.")
        exit()

    # Instantiate the test class and run the tests.
    # Set headless=True for running without opening a browser GUI.
    # Set browser_type to "chromium", "firefox", or "webkit".
    # Default is "firefox" to match the original recorded code.
    test_runner = YouTubeVideoPlayerTest(headless=False, browser_type="firefox")
    test_runner.run_tests(num_videos_to_process)
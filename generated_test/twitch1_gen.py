import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import random
import json

def run_twitch_test(num_videos: int):
    """
    Automates browsing random Twitch channels via twitch-tools.rootonline.de
    and collects video statistics for a specified number of videos.
    """
    telemetry = [] # List to store collected data for each video

    # Launch browser with sync_playwright context manager
    with sync_playwright() as p:
        # Launch Chromium browser (Google Chrome), non-headless as requested
        browser = p.chromium.launch(
            executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            headless=False
        )
        context = browser.new_context() # Create a new browser context
        page = context.new_page()       # Create a new page within the context

        print(f"Starting Twitch video stats collection for {num_videos} videos...")

        # Loop for the desired number of videos
        for i in range(num_videos):
            print(f"\n--- Processing Video {i+1}/{num_videos} ---")
            current_video_data = {"iteration": i + 1} # Dictionary to store data for current video

            try:
                # 1. Navigate to the random channel preview page. This reloads the page
                # and fetches a new random channel each iteration.
                page.goto("https://twitch-tools.rootonline.de/random_channel_previews.php", wait_until="load")
                page.wait_for_load_state("networkidle") # Wait for network to be idle
                print("  Navigated to random channel preview page.")

                # 2. Ensure the main iframe containing the Twitch player is loaded and visible
                iframe_locator = page.locator("iframe")
                iframe_locator.wait_for(state="visible", timeout=15000) # Increased timeout for stability
                iframe_frame = iframe_locator.content_frame # Get the content frame of the iframe

                if not iframe_frame:
                    print("  Error: Could not get content frame of the iframe. Skipping this video.")
                    current_video_data["error"] = "Iframe content frame not found."
                    telemetry.append(current_video_data)
                    continue

                # 3. Handle "Intended for certain audiences" popup if it appears.
                # This button is inside the iframe, as per the recorded code.
                start_watching_button = iframe_frame.get_by_role("button", name="Intended for certain audiences")
                if start_watching_button.is_visible(timeout=5000): # Check visibility with a timeout
                    print("  ⚠️ 'Intended for certain audiences' popup detected. Clicking 'Start Watching'.")
                    start_watching_button.click()
                    time.sleep(1) # Small delay for UI to react
                    # Re-get the iframe frame as content might have changed/reloaded
                    iframe_frame = iframe_locator.content_frame
                    if not iframe_frame:
                        print("  Error: Iframe frame lost after popup dismissal. Skipping this video.")
                        current_video_data["error"] = "Iframe lost after popup dismissal."
                        telemetry.append(current_video_data)
                        continue
                    # Wait for settings button to be ready after dismissal
                    iframe_frame.get_by_role("button", name="Settings").wait_for(state="visible", timeout=10000)
                else:
                    print("  No 'Intended for certain audiences' popup detected.")

                # 4. Open Settings panel within the iframe
                settings_button = iframe_frame.get_by_role("button", name="Settings")
                settings_button.wait_for(state="visible", timeout=10000) # Wait for settings button to be clickable
                settings_button.click()
                print("  Clicked 'Settings'.")

                # 5. Open Advanced settings menu item
                advanced_menu_item = iframe_frame.get_by_role("menuitem", name="Advanced")
                advanced_menu_item.wait_for(state="visible", timeout=5000) # Wait for Advanced menu item
                advanced_menu_item.click()
                print("  Clicked 'Advanced'.")

                # 6. Ensure 'Video Stats' checkbox is checked
                video_stats_checkbox = iframe_frame.get_by_role("checkbox", name="Video Stats")
                if not video_stats_checkbox.is_checked():
                    video_stats_checkbox.check()
                    print("  Checked 'Video Stats' checkbox.")
                else:
                    print("  'Video Stats' checkbox already checked.")
                
                # 7. Collect video statistics from the displayed panel using the table rows
                collected_stats = {}

                # Locate all rows in the stats table
                rows = iframe_frame.locator(
                    "tbody.tw-table-body tr[data-a-target='player-overlay-video-stats-row']"
                )
                num_rows = rows.count()

                if num_rows > 0:
                    print(f"  Collecting {num_rows} video stats:")
                    for j in range(num_rows):
                        row = rows.nth(j)
                        # First <td> contains the label, second <td> contains the value
                        label = row.locator("td").nth(0).locator("p").inner_text().strip()
                        value = row.locator("td").nth(1).locator("p").inner_text().strip()
                        collected_stats[label] = value
                        print(f"    - {label}: {value}")
                else:
                    print("  ⚠️ No video stats rows found in table.")

                current_video_data["stats"] = collected_stats
                current_video_data["source_page_url"] = page.url

                # 9. Record the collected telemetry for the current video
                telemetry.append(current_video_data)
                print(f"  Telemetry collected for video {i+1}.")

                # 10. Add a random pause before the next iteration for realistic browsing simulation
                random_pause = random.uniform(2, 5)
                print(f"  Pausing for {random_pause:.2f} seconds before next video...")
                time.sleep(random_pause)

            except Exception as e:
                # Catch any unexpected errors during an iteration and log them
                print(f"  ❌ An unexpected error occurred during iteration {i+1}: {e}")
                current_video_data["error"] = str(e) # Add error message to current video's data
                if "stats" not in current_video_data: # Ensure stats key exists even if error occurred before collection
                    current_video_data["stats"] = {}
                telemetry.append(current_video_data) # Append partial data or error data
                # Add a longer pause for stability if an error occurs
                time.sleep(random.uniform(5, 10))

        # Close the browser context and browser after all iterations are complete
        context.close()
        browser.close()
        print("\n--- Test Finished ---")

    # 11. Output results to console
    print(f"\n💾 Collected telemetry for {len(telemetry)} videos:")
    print(json.dumps(telemetry, indent=2, ensure_ascii=False))

    # 12. Optionally write telemetry to a JSON file
    try:
        with open("twitch_telemetry.json", "w", encoding="utf-8") as f:
            json.dump(telemetry, f, indent=2, ensure_ascii=False)
        print("Telemetry saved to twitch_telemetry.json")
    except Exception as e:
        print(f"Error saving telemetry to file: {e}")

# Main execution block to prompt user for input and run the test
if __name__ == "__main__":
    try:
        num_videos_to_process = int(input("How many random Twitch videos should I process? "))
        if num_videos_to_process <= 0:
            print("Please enter a positive number for the number of videos.")
        else:
            run_twitch_test(num_videos_to_process)
    except ValueError:
        print("Invalid input. Please enter a numerical value.")
    except KeyboardInterrupt:
        print("\nTest interrupted by user. Exiting gracefully.")
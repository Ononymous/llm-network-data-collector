import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
import random
import json

def run_twitch_test(num_videos: int, collection_seconds: int):
    telemetry = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            headless=False
        )
        context = browser.new_context()
        page = context.new_page()

        print(f"Starting Twitch video stats collection for {num_videos} videos, "
              f"{collection_seconds}s per video sample...")

        for i in range(num_videos):
            print(f"\n--- Processing Video {i+1}/{num_videos} ---")
            current_video_data = {"iteration": i + 1}

            try:
                # 1. Navigate to random channel preview
                page.goto(
                    "https://twitch-tools.rootonline.de/random_channel_previews.php",
                    wait_until="load"
                )
                print("  Navigated to random channel preview page.")

                # 2. Locate iframe
                iframe_locator = page.locator("iframe")
                iframe_locator.wait_for(state="visible", timeout=15000)
                iframe_frame = iframe_locator.content_frame
                if not iframe_frame:
                    raise RuntimeError("Iframe content frame not found.")

                # 3. Dismiss audience popup if present
                popup_btn = iframe_frame.get_by_role("button", name="Start Watching")
                if popup_btn.is_visible(timeout=2000):
                    print("  Dismissing 'Intended for certain audiences' popup.")
                    popup_btn.click()
                    time.sleep(1)
                    iframe_frame = iframe_locator.content_frame

                # 4. OFFLINE check: skip if streamer is offline
                offline_label = iframe_frame.locator(
                    "strong.CoreText-sc-1txzju1-0.krncnP", has_text="Offline"
                )
                if offline_label.count() and offline_label.first.is_visible(timeout=2000):
                    print("  ⚠️ Streamer is offline. Skipping this video.")
                    telemetry.append(current_video_data)
                    num_videos -= 1
                    continue

                # 5. AD check: skip if ad banner text appears
                ad_banner = iframe_frame.locator(
                    "span[data-a-target='video-ad-banner-default-text'],"
                    "p.CoreText-sc-1txzju1-0.dXULtJ",
                    has_text="stick around to support the stream"
                )
                if ad_banner.count() and ad_banner.first.is_visible(timeout=2000):
                    print("  ⚠️ Advertisement detected. Skipping this video.")
                    telemetry.append(current_video_data)
                    num_videos -= 1
                    continue

                # 6–8. Open Settings → Advanced → ensure Video Stats checked
                iframe_frame.get_by_role("button", name="Settings").click()
                iframe_frame.get_by_role("menuitem", name="Advanced").click()
                chk = iframe_frame.get_by_role("checkbox", name="Video Stats")
                if not chk.is_checked():
                    chk.check()
                print("  'Video Stats' enabled.")

                # 9. Collect stats once per second for collection_seconds
                print(f"  Collecting stats for {collection_seconds} seconds (1 sample/sec)...")
                stats_samples = []
                for sec in range(collection_seconds):
                    time.sleep(1)
                    sample = {}
                    rows = iframe_frame.locator(
                        "tbody.tw-table-body tr[data-a-target='player-overlay-video-stats-row']"
                    )
                    for j in range(rows.count()):
                        row = rows.nth(j)
                        label = row.locator("td").nth(0).locator("p").inner_text().strip()
                        value = row.locator("td").nth(1).locator("p").inner_text().strip()
                        sample[label] = value
                    stats_samples.append(sample)
                    print(f"    [Sample {sec+1}] {sample}")

                current_video_data["stats_samples"] = stats_samples
                current_video_data["source_page_url"] = page.url

                # 10. Close stats panel if present
                close_btn = iframe_frame.get_by_role("button", name="Close video stats")
                if close_btn.is_visible(timeout=3000):
                    close_btn.click()

                telemetry.append(current_video_data)
                print(f"  Telemetry collected for video {i+1}.")

                # 11. Random pause before next iteration
                time.sleep(random.uniform(2, 5))

            except Exception as e:
                print(f"  ❌ Error on iteration {i+1}: {e}")
                current_video_data["error"] = str(e)
                current_video_data.setdefault("stats_samples", [])
                telemetry.append(current_video_data)
                time.sleep(random.uniform(5, 10))

        context.close()
        browser.close()
        print("\n--- Test Finished ---")

    # Output & save
    print(f"\n💾 Collected telemetry for {len(telemetry)} videos:")
    print(json.dumps(telemetry, indent=2, ensure_ascii=False))
    with open("twitch_telemetry.json", "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2, ensure_ascii=False)
    print("Telemetry saved to twitch_telemetry.json")
    
if __name__ == "__main__":
    try:
        num_videos_to_process = int(input("How many random Twitch videos should I process? "))
        duration_seconds = int(input("How many seconds of stats to collect per video? "))
        if num_videos_to_process <= 0 or duration_seconds <= 0:
            print("Please enter positive numbers for both inputs.")
        else:
            run_twitch_test(num_videos_to_process, duration_seconds)
    except ValueError:
        print("Invalid input. Please enter numerical values.")
    except KeyboardInterrupt:
        print("\nTest interrupted by user. Exiting.")

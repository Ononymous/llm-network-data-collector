import json
import re

def parse_stats_block(stats_text):
    """Extract individual metrics from a stats-for-nerds block."""
    def match(pattern):
        found = re.search(pattern, stats_text)
        return found.group(1).strip() if found else None

    return {
        "video_id": match(r"Video ID / sCPN ([\w-]+) /"),
        "viewport": match(r"Viewport / Frames ([\dx]+(?:\*\d\.\d+)?)"),
        "dropped_frames": match(r"Viewport / Frames .*? / (\d+ dropped of \d+|\-)"),
        "current_res": match(r"Current / Optimal Res ([\dx@]+)"),
        "optimal_res": match(r"Current / Optimal Res [\dx@]+ / ([\dx@]+)"),
        "volume": match(r"Volume / Normalized ([\d%]+)"),
        "normalized_volume": match(r"Volume / Normalized [\d%]+ / ([\w\s().%-]+)\n"),
        "codecs": match(r"Codecs (.*?) /"),
        "audio_codec": match(r"Codecs .*? / (.*?)\n"),
        "connection_speed": match(r"Connection Speed ([\d,]+ Kbps)"),
        "network_activity": match(r"Network Activity ([\d.]+ [KM]B)"),
        "buffer_health": match(r"Buffer Health ([\d.]+ s)"),
        "live_mode": match(r"Live Mode (.*?)\n"),
        "mystery_text": match(r"Mystery Text (.*?)\n"),
        "date": match(r"Date (.*)")
    }

def parse_file(filepath):
    """Load the JSON and parse each stats block."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for video in data:
        for stat_entry in video.get("stats_collections", []):
            stats_raw = stat_entry.get("stats", "")
            stat_entry["stats"] = parse_stats_block(stats_raw)

    return data

# Example usage
if __name__ == "__main__":
    input_path = "generated_test/youtube_telemetry.json"  # replace with actual path
    output_path = "generated_test/youtube_telemetry_parsed.json"

    parsed_data = parse_file(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Parsed telemetry saved to {output_path}")

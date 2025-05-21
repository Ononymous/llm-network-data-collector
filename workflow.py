from playwright.sync_api import sync_playwright
import time
import random
import json

# your existing list of nouns…
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
    "शहर", "गांव", "देश", "जल", "अन्न", "आदमी", "औरत", "बच्चा", "पिता", "माता",
    
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


def run(num_videos: int):
    telemetry = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page    = browser.new_page()

        for i in range(num_videos):
            print(f"\n▶️  Video {i+1}/{num_videos}")

            # 1) pick and search a random noun
            query = random.choice(nouns)
            page.goto(f"https://www.youtube.com/results?search_query={query}")
            page.wait_for_load_state("networkidle")

            # 2) click the first video result
            first = page.locator("a#video-title").first
            href  = first.get_attribute("href")
            if not href or not href.startswith("/watch?v="):
                print("  ⚠️ no video found for", query)
                continue
            video_url = "https://www.youtube.com" + href
            page.goto(video_url)
            page.wait_for_selector("video")
            print("  🎬 opened:", video_url)

                        # 4) open Stats for nerds
            # Right-click on video to bring up context menu
            video = page.locator("#player")
            video.wait_for()
            box = video.bounding_box()
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, button="right")
            time.sleep(1)

            stats = []
            # Click on "Stats for nerds"
            nerds = page.get_by_text("Stats for nerds")
            if nerds.is_visible():
                nerds.click()
                panel = page.wait_for_selector(".html5-video-info-panel", timeout=5000)
            else:
                print("Stats for nerds not found.")
                return

            # 3) get the full duration of the video
            duration = page.evaluate("() => document.querySelector('video').duration")
            # pick a random watch time between 0 and full duration
            watch_time = random.uniform(0, duration)
            print(f"  ⏱ watching for {watch_time:.1f}s out of {duration:.1f}s")
            #page.wait_for_timeout(watch_time * 1000)

            start = time.time()
            while time.time() - start < watch_time:
                # re-evaluate innerText each loop
                vid_stats = page.evaluate(
                    "() => document.querySelector('.html5-video-info-panel').innerText"
                )
                stats.append(vid_stats)
                print("   •", stats[0])  # just preview first line
                time.sleep(1)


            # 5) record telemetry
            telemetry.append({
                "video_url": video_url,
                "query": query,
                "duration": duration,
                "watched": watch_time,
                "stats": stats
            })

            # optional small pause between iterations
            time.sleep(1)

        browser.close()

    # 6) output results
    print("\n💾 Collected telemetry for", len(telemetry), "videos")
    print(json.dumps(telemetry, indent=2))

    # optionally write to file
    with open("telemetry.json", "w", encoding="utf-8") as f:
        json.dump(telemetry, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    n = int(input("How many random videos should I process? "))
    run(n)

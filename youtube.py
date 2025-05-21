from playwright.sync_api import sync_playwright
from time import sleep
import time
import random
import json

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

def run():
    telemetry = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        # Pick a random noun and go to YouTube search page
        query = random.choice(nouns)
        page.goto(f"https://www.youtube.com/results?search_query={query}")
        page.wait_for_load_state("networkidle")

        # Click the first video result directly
        first_video = page.locator("a#video-title").first
        href = first_video.get_attribute("href")
        if not href or not href.startswith("/watch?v="):
            print("No video found.")
            return

        video_url = "https://www.youtube.com" + href
        page.goto(video_url)
        page.wait_for_load_state("load")

        # Right-click on video to bring up context menu
        video = page.locator("#player")
        video.wait_for()
        box = video.bounding_box()
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, button="right")
        time.sleep(1)

        # Click on "Stats for nerds"
        nerds = page.get_by_text("Stats for nerds")
        if nerds.is_visible():
            nerds.click()
        else:
            print("Stats for nerds not found.")
            return

        time.sleep(1)

        # Monitor and print stats
        stats_panel = page.locator(".html5-video-info-panel")
        if stats_panel.is_visible():
            for _ in range(100):
                print(stats_panel.inner_text())
                time.sleep(1)
        else:
            print("Stats panel not visible.")

        browser.close()

run()
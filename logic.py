# logic.py
import json
import random

with open("assets/hotel.json", encoding="utf-8") as f:
    HOTELS = json.load(f)
with open("assets/tour.json", encoding="utf-8") as f:
    TOURS = json.load(f)
with open("assets/food_cafe.json", encoding="utf-8") as f:
    FOOD_CAFE = json.load(f)

REGIONS = ["서울", "부산", "제주도"]
CATEGORIES = ["인기 숙소", "관광지", "맛집 및 카페", "일정"]

def show_result(category, region):
    if category == "인기 숙소":
        items = HOTELS.get(region, [])
        if not items:
            cards = f"{region} 숙소 데이터가 없습니다."
        else:
            cards = "".join(
                f"""<div style='padding:14px; border-radius:10px; background:#fff; 
                border: 2.5px solid #FFD600; margin-bottom:8px; box-shadow: 0 2px 8px #0001;'>
                <b>{item.get('name', '')}</b><br>
                📍 {item.get('addr','')}
                <br>📞 {item.get('phone', '')}
                <br><a href='{item.get('url', '#')}' target='_blank'>상세보기</a>
                </div>""" for item in items
            )
        return cards, True
    elif category == "관광지":
        items = TOURS.get(region, [])
        if not items:
            cards = f"{region} 관광지 데이터가 없습니다."
        else:
            cards = "".join(
                f"""<div style='padding:14px; border-radius:10px; background:#fff; 
                border: 2.5px solid #FFD600; margin-bottom:8px; box-shadow: 0 2px 8px #0001;'>
                <b>{item.get('name', '')}</b><br>
                📍 {item.get('addr','')}
                <br><a href='{item.get('url', '#')}' target='_blank'>상세보기</a>
                </div>""" for item in items
            )
        return cards, True
    else:
        return "", False

def chatbot_fn(msg, chat_history):
    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": msg})
    chat_history.append({"role": "assistant", "content": f"'{msg}'에 대한 추천 결과 예시입니다."})
    return "", chat_history

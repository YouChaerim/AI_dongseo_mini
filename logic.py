# logic.py
import json
import random
import base64
import os

def img_to_base64_html(img_path):
    # img_path가 실제 파일 경로(예: ./assets/image/부산/숙소/웨스틴 조선 부산.jpg)
    if not os.path.exists(img_path):
        return ""  # 파일 없으면 빈 문자열
    ext = os.path.splitext(img_path)[-1].lower().replace('.', '')
    if ext not in ["jpg", "jpeg", "png"]:
        return ""  # 지원하지 않는 확장자
    with open(img_path, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode('utf-8')
    return f'<img src="data:image/{ext};base64,{base64_str}" style="width:120px;height:95px;object-fit:cover;border-radius:16px;box-shadow:0 2px 8px #0002;display:block;" alt="">'

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
                f"""<div style='display:flex;justify-content:space-between;align-items:flex-start; 
                padding:14px; border-radius:10px; background:#fff; 
                border: 2.5px solid #FFD600; margin-bottom:8px; box-shadow: 0 2px 8px #0001;'>
                <div>
                    <b>{item.get('name', '')}</b><br>
                    📍 {item.get('addr','')}
                    <br>📞 {item.get('phone', '')}
                    <br><a href='{item.get('url', '#')}' target='_blank'>상세보기</a>
                </div>
                <div style='margin-left:18px;display:flex;align-items:center;'>
                    {img_to_base64_html('.' + item.get('img', ''))}
                </div>
                </div>""" for item in items
            )
        return cards, True
    # 관광지도 동일하게 적용!
    elif category == "관광지":
        items = TOURS.get(region, [])
        if not items:
            cards = f"{region} 관광지 데이터가 없습니다."
        else:
            cards = "".join(
                f"""<div style='display:flex;justify-content:space-between;align-items:flex-start; 
                padding:14px; border-radius:10px; background:#fff; 
                border: 2.5px solid #FFD600; margin-bottom:8px; box-shadow: 0 2px 8px #0001;'>
                <div>
                    <b>{item.get('name', '')}</b><br>
                    📍 {item.get('addr','')}
                    <br>📞 {item.get('phone', '')}
                    <br><a href='{item.get('url', '#')}' target='_blank'>상세보기</a>
                </div>
                <div style='margin-left:18px;display:flex;align-items:center;'>
                    {img_to_base64_html('.' + item.get('img', ''))}
                </div>
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

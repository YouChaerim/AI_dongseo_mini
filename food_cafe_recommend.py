import json
import random
import base64
import os

# 1. 이미지 base64 변환 함수
def get_image_base64(image_path):
    # '/assets/...' → 'assets/...'로 보정
    image_path = image_path.lstrip('/')
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = image_path.split('.')[-1].lower()
    mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
    return f"data:image/{mime};base64,{encoded}"

# 2. 데이터 로드
with open("assets/food_cafe.json", encoding="utf-8") as f:
    FOOD_CAFE = json.load(f)

# 3. 추천 함수 (카드+이미지 base64 임베딩)
def recommend_food_cafe(region, food_type, n=5):
    region_map = {"제주도": "제주"}
    region = region_map.get(region, region)
    if food_type == "카페":
        items = FOOD_CAFE[region]["카페"]
    else:
        items = FOOD_CAFE[region]["음식점"]
        if food_type not in ["랜덤", "기타"]:
            items = [item for item in items if item["type"] == food_type]
        elif food_type == "기타":
            items = [item for item in items if item["type"] not in ["한식", "중식", "일식", "양식", "카페"]]
        elif food_type == "랜덤":
            items = FOOD_CAFE[region]["음식점"] + FOOD_CAFE[region]["카페"]
    if not items:
        return ["""<div style="margin-bottom:10px;">추천할 데이터가 없습니다.</div>"""]
    pick = random.sample(items, min(n, len(items)))
    result = []
    for item in pick:
        img_html = ""
        if item.get('img', ''):
            # base64 변환하여 직접 임베딩
            img_base64 = get_image_base64(item['img'])
            if img_base64:
                img_html = (
                    f'<div style="flex:0 0 120px;height:95px;margin-left:24px;display:flex;align-items:center;">'
                    f'<img src="{img_base64}" style="width:120px;height:95px;object-fit:cover;'
                    f'border-radius:16px;box-shadow:0 2px 8px #0002;display:block;" alt="이미지">'
                    '</div>'
                )
        card = f"""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; 
                    border-radius: 18px; background: #fffcf0; border: 3px solid #FFD600;
                    box-shadow: 0 2px 8px #0001; margin-bottom: 18px; padding: 18px 18px 18px 18px; min-height: 140px;">
            <div style="flex: 1 1 60%;">
                <b style="font-size: 1.17em;">{item['name']}</b> <span style="color:#7f7f7f;">({item['type']})</span><br>
                <span style="font-size: 15px;">📍 {item['addr']}</span><br>
                <span style="font-size: 15px;">📞 {item.get('phone', '-')}</span><br>
                <a href="{item.get('url', '#')}" target="_blank" style="color:#2874A6;text-decoration:underline;">상세보기</a>
            </div>
            {img_html}
        </div>
        """
        result.append(card)
    return result

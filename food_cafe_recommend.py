import json
import random

with open("assets/food_cafe.json", encoding="utf-8") as f:
    FOOD_CAFE = json.load(f)

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
        card = f"""
        <div style="border-radius: 12px; background: #fffbe9; border: 2px solid #FFD600;
            box-shadow: 0 2px 8px #0001; margin-bottom: 18px; padding: 18px 18px 14px 18px;">
            <b>{item['name']}</b> <span style="color:#7f7f7f;">({item['type']})</span><br>
            <span style="font-size: 15px;">📍 {item['addr']}</span><br>
            <span style="font-size: 15px;">📞 {item.get('phone', '-')}</span><br>
            <a href="{item.get('url', '#')}" target="_blank" style="color:#2874A6;text-decoration:underline;">상세보기</a>
        </div>
        """
        result.append(card)
    return result

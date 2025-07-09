import requests
import os
from dotenv import load_dotenv

load_dotenv()
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

def search_kakao_place(query, category=None, size=10):
    """
    query: 검색 키워드(예: 부산 맛집, 해운대 호텔)
    category: 카카오 카테고리코드(숙박: AD5, 음식점: FD6 등, 선택)
    size: 반환 결과 개수(최대 15)
    """
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    print(query)
    print(size)
    params = {"query": query, "size": size}
    if category:
        params["category_group_code"] = category
    resp = requests.get(url, headers=headers, params=params)
    print(resp)
    if resp.ok:
        return resp.json()["documents"]
    return []

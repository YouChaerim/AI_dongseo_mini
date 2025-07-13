# api_kakao.py에서 장소 검색 함수 가져오기
from api_kakao import search_kakao_place

# 카테고리 이름과 카카오 API에서 사용하는 코드 매핑
CATEGORY_MAP = {
    "인기 숙소": "AD5",  # AD5: 숙박업소 코드
    "관광지": "AT4",    # AT4: 관광명소 코드
    "맛집 및 카페": "FD6"  # FD6: 음식점 코드
}

# 지역 목록 (사용자 선택용)
REGIONS = ["서울", "부산", "제주도"]

# 각 지역별 '구' 목록
REGION_GUS = {
    "서울": ["강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구",
            "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구",
            "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"],
    "부산": ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구",
            "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
    "제주도": ["제주시", "서귀포시"]
}

# 사용자 선택 가능한 카테고리 목록
CATEGORIES = ["인기 숙소", "관광지", "맛집 및 카페", "일정"]

# 사용자에게 보여줄 검색어와 실제 카카오 API 쿼리용 단어 매핑
QUERY_MAP = {
    "인기 숙소": "호텔",
    "관광지": "명소",
    "맛집 및 카페": "맛집"
}

# 선택된 카테고리, 지역, 구에 맞게 장소 검색 후 결과 HTML 카드로 반환하는 함수
def show_result(category, region, gu):
    kakao_category = CATEGORY_MAP.get(category)  # 카카오 API용 카테고리 코드 찾기
    query = f"{region} {gu} {QUERY_MAP.get(category, category)}"  # 실제 검색어 만들기
    places = search_kakao_place(query, category=kakao_category, size=5)  # API 요청 (최대 5개 결과)

    # 결과 없을 경우 메시지 반환
    if not places:
        return f"{region} {gu} {category} 데이터가 없습니다.", True

    # 검색된 장소들을 HTML 카드 형식으로 만들기
    cards = "".join(
        f"""<div style='display:flex;justify-content:space-between;align-items:flex-start; 
            padding:14px; border-radius:10px; background:#fff; 
            border: 2.5px solid #FFD600; margin-bottom:8px; box-shadow: 0 2px 8px #0001;'>
            <div>
                <b>{p['place_name']}</b><br>
                📍 {p.get('road_address_name', p.get('address_name', ''))}
                <br>📞 {p.get('phone', '-')}
                <br><a href='{p.get('place_url', '#')}' target='_blank'>상세보기</a>
            </div>
        </div>"""
        for p in places
    )

    return cards, True  # HTML 카드와 표시 여부(True) 반환

# 간단한 챗봇 예시 함수
def chatbot_fn(msg, chat_history):
    chat_history = chat_history or []  # 기존 대화 기록이 없으면 빈 리스트로 초기화
    chat_history.append({"role": "user", "content": msg})  # 사용자 메시지 추가
    chat_history.append({"role": "assistant", "content": f"'{msg}'에 대한 추천 결과 예시입니다."})  # 예시 답변 추가
    return "", chat_history  # 입력 칸 비우고, 업데이트된 대화 내역 반환

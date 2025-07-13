import requests  # HTTP 요청을 보내기 위한 라이브러리
import os        # 운영체제 환경변수 등을 다루기 위한 라이브러리
from dotenv import load_dotenv  # .env 파일에서 환경변수 불러오는 라이브러리

# .env 파일의 내용을 읽어서 환경변수로 등록
load_dotenv()

# KAKAO_API_KEY라는 환경변수에서 API 키 값을 가져옴
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

# 카카오 API를 사용하여 장소 검색을 수행하는 함수
def search_kakao_place(query, category=None, size=10):
    """
    query: 검색 키워드 (예: '부산 맛집', '해운대 호텔')
    category: 카카오 카테고리 코드 (예: AD5=숙박, FD6=음식점) - 선택적으로 사용
    size: 결과 개수 제한 (최대 15개까지 반환 가능)
    """
    # 카카오 API의 키워드 검색 URL
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    # API 요청에 필요한 인증 헤더 (API 키를 사용)
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

    # 검색에 사용할 파라미터 설정
    params = {"query": query, "size": size}
    if category:
        params["category_group_code"] = category  # category가 주어졌을 때만 추가

    # 실제 API 요청 보내기 (GET 요청)
    resp = requests.get(url, headers=headers, params=params)

    # (개발용) 디버깅을 위해 검색어와 결과 상태 출력
    print(query)
    print(size)
    print(resp)

    # 요청 성공 시 검색 결과의 'documents' 리스트 반환
    if resp.ok:
        return resp.json()["documents"]

    # 요청 실패 시 빈 리스트 반환
    return []

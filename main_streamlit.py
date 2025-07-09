import streamlit as st
from api_kakao import search_kakao_place
import pandas as pd

st.title("카카오 맛집/숙박 대시보드")

with st.form("search_form"):
    query = st.text_input("검색어 (예: 부산 맛집, 해운대 호텔)", value="부산 맛집")
    category = st.selectbox("카테고리", ["전체", "맛집", "숙박"])
    submitted = st.form_submit_button("검색")

if submitted:
    category_map = {"전체": "", "맛집": "FD6", "숙박": "AD5"}
    category_code = category_map.get(category, "")
    results = search_kakao_place(query, category=category_code)
    if results:
        df = pd.DataFrame([{
            "이름": r['place_name'],
            "주소": r['road_address_name'],
            "전화": r['phone'],
            "URL": r['place_url'],
            "x": float(r['x']),
            "y": float(r['y'])
        } for r in results])
        st.dataframe(df[["이름", "주소", "전화", "URL"]])

        # 지도 시각화 (위도/경도)
        st.map(df.rename(columns={'y':'lat', 'x':'lon'})[['lat','lon']])
    else:
        st.warning("검색 결과가 없습니다.")
else:
    st.info("위 검색어와 카테고리를 입력한 뒤 '검색'을 눌러주세요.")

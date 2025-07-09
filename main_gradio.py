import gradio as gr
from api_kakao import search_kakao_place

def chatbot_fn(message, history):
    """
    message: 사용자가 방금 입력한 내용 (예: "부산 맛집 추천해줘")
    history: [(질문, 답변), ...] 형태의 이전 대화 내역 리스트
    """
    # 카테고리 자동 인식 예시 (간단 버전)
    if "호텔" in message or "숙소" in message:
        category = "AD5"
    elif "맛집" in message or "음식점" in message:
        category = "FD6"
    else:
        category = ""
    # API 호출
    results = search_kakao_place(message, category=category)
    if not results:
        answer = "검색 결과가 없습니다."
    else:
        answer = ""
        for r in results[:5]:
            answer += (
                f"🏷️ <b>{r['place_name']}</b><br>"
                f"주소: {r['road_address_name']}<br>"
                f"전화: {r['phone']}<br>"
                f"<a href='{r['place_url']}' target='_blank'>지도 보기</a><br>"
                "<hr>"
            )
    return answer

# Gradio 최신 챗봇UI
demo = gr.ChatInterface(
    fn=chatbot_fn,
    title="카카오 맛집/숙박 챗봇",
    description="예: '부산 맛집 추천해줘', '해운대 호텔', '서면 숙소 알려줘' 등 자연어로 입력해보세요!",
    theme=gr.themes.Default()
)

if __name__ == "__main__":
    demo.launch()

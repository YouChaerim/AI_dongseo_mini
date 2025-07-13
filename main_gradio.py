import random
import gradio as gr

# logic.py에 정의된 상수(지역, 구 목록, 카테고리)와 결과 표시 함수 불러오기
from logic import REGIONS, REGION_GUS, CATEGORIES, show_result

# 각 챗봇 기능 불러오기
from food_cafe_chatbot import food_cafe_chatbot, START_MSG_FOOD
from schedule_chatbot import schedule_chatbot_fn as schedule_chatbot, START_MSG

# 전체 앱 실행 함수 정의
def run_app():
    gu_names = [""] * 25  # 구 버튼에 표시될 이름 저장용 리스트 (최대 25개)

    # Gradio UI 전체를 Blocks 단위로 정의
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("## 딸깍이의 여행 도우미")  # 화면 상단 제목 출력
        result_html = gr.HTML(visible=False, elem_id="result_html")  # 결과 카드 출력 영역 (초기에는 숨김)

        # 챗봇 대화 UI 영역 정의 (초기에는 숨김)
        with gr.Column(visible=False, elem_id="chatbot_col") as chatbot_col:
            chatbot = gr.Chatbot(visible=False, elem_id="main_chatbot", type="messages", render_markdown=True)
            with gr.Row(visible=False, elem_id="chat_input_row") as chat_input_row:
                txt = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요...", scale=4, visible=False)
                send_btn = gr.Button("전송", scale=1, visible=False)

        # 대화 상태(단계, 지역, 구, 음식 종류)를 관리할 변수
        chat_state = gr.State(value={"step": 1, "region": None, "gu": None, "food_type": None})

        # 화면 하단 고정 영역 (카테고리, 지역, 구 선택 버튼들이 들어감)
        with gr.Column(elem_id="footer_fixed"):
            # 구 버튼 25개 생성 (초기에는 숨김)
            with gr.Row(visible=False, elem_id="gu_btn_row") as gu_btn_row:
                gu_buttons = [gr.Button(visible=False) for _ in range(25)]

            # 지역 버튼 생성 (서울, 부산 등)
            with gr.Row(visible=False, elem_id="region_btn_row") as region_btn_row:
                region_buttons = [gr.Button(region) for region in REGIONS]

            # 카테고리 버튼 생성 (맛집, 숙소, 일정 등)
            with gr.Row(elem_id="cat_row"):
                btns = [gr.Button(cat, variant="secondary") for cat in CATEGORIES]

        # 선택 상태를 저장할 숨김 텍스트박스
        category_box = gr.Textbox(value="", visible=False, interactive=False, show_label=False)
        region_box = gr.Textbox(value="", visible=False, interactive=False, show_label=False)

        # 카테고리 선택 시 UI 상태 변경 함수
        def set_category(idx):
            btn_states = [gr.update(variant="primary" if i == idx else "secondary") for i in range(len(CATEGORIES))]
            cat = CATEGORIES[idx]

            # '맛집 및 카페' 또는 '일정' 선택 시 챗봇 화면 표시
            if cat in ["맛집 및 카페", "일정"]:
                init_msg = START_MSG if cat == "일정" else START_MSG_FOOD
                return btn_states + [
                    cat,  # category_box에 저장할 값
                    gr.update(visible=False),  # 지역 버튼 숨김
                    gr.update(visible=False),  # 구 버튼 숨김
                    gr.update(visible=False),  # 결과 카드 숨김
                    gr.update(visible=True),   # 챗봇 UI 표시
                    gr.update(visible=True),
                    gr.update(visible=True),
                    gr.update(visible=True),
                    gr.update(visible=True),
                    [{"role": "assistant", "content": init_msg}]  # 챗봇 초기 메시지
                ]
            else:
                # 다른 카테고리 선택 시 기본 UI만 표시
                return btn_states + [
                    cat,
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    []
                ]

        # set_category에서 반환하는 모든 UI 컴포넌트를 한 번에 업데이트할 리스트
        output_list = btns + [
            category_box,
            region_btn_row,
            gu_btn_row,
            result_html,
            chatbot_col,
            chatbot,
            chat_input_row,
            txt,
            send_btn,
            chatbot
        ]

        # 각 카테고리 버튼에 클릭 이벤트 등록
        for i, btn in enumerate(btns):
            def make_click(idx):
                def click_fn():
                    return set_category(idx)
                return click_fn
            btn.click(make_click(i), inputs=[], outputs=output_list)

        # 각 지역 버튼에 클릭 이벤트 등록
        for i, btn in enumerate(region_buttons):
            def make_region_click(idx):
                def fn(category):
                    region = REGIONS[idx]
                    gu_list = REGION_GUS.get(region, [])

                    # 구 이름을 gu_names 리스트에 저장
                    for j in range(25):
                        if j < len(gu_list):
                            gu_names[j] = gu_list[j]
                        else:
                            gu_names[j] = ""

                    # 구 버튼 상태 업데이트
                    updates = [
                        gr.update(visible=(j < len(gu_list)), value=gu_list[j] if j < len(gu_list) else "")
                        for j in range(25)
                    ]

                    return region, gr.update(visible=True), *updates
                return fn

            btn.click(make_region_click(i), inputs=[category_box], outputs=[region_box, gu_btn_row] + gu_buttons)

        # 각 구 버튼에 클릭 이벤트 등록
        for j, btn in enumerate(gu_buttons):
            def make_gu_click(idx):
                def fn(category, region):
                    gu_name = gu_names[idx]
                    if gu_name:
                        cards, visible = show_result(category, region, gu_name)
                        return gr.update(value=cards, visible=visible)
                    else:
                        return gr.update(value="", visible=False)
                return fn

            btn.click(make_gu_click(j), inputs=[category_box, region_box], outputs=result_html)

        # 챗봇 '전송' 버튼 클릭/엔터 시 동작 함수
        def send_chat(txt_val, chat_val, state_val, category_val):
            if category_val == "맛집 및 카페":
                return food_cafe_chatbot(txt_val, chat_val, state_val)
            elif category_val == "일정":
                return schedule_chatbot(txt_val, chat_val, state_val)
            else:
                return "", chat_val, state_val

        # '전송' 버튼과 Enter 키에 이벤트 연결
        send_btn.click(send_chat, inputs=[txt, chatbot, chat_state, category_box], outputs=[txt, chatbot, chat_state])
        txt.submit(send_chat, inputs=[txt, chatbot, chat_state, category_box], outputs=[txt, chatbot, chat_state])

        # custom.css를 불러와서 화면 스타일 적용
        with open("styles/custom.css", encoding="utf-8") as f:
            css = f.read()
        gr.HTML(f"<style>{css}</style>")

    # Gradio 앱 실행
    demo.launch()

# 프로그램 시작점: run_app() 실행
if __name__ == "__main__":
    run_app()

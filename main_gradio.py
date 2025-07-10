import random
import gradio as gr
from logic import REGIONS, CATEGORIES, show_result
from food_cafe_prompts import STEP1_QUESTIONS, food_cafe_chatbot
from schedule_chatbot import schedule_chatbot_fn as schedule_chatbot, START_MSG, REGION_MSG

def run_app():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("## 🏨 카카오 스타일 숙소/맛집 챗봇")
        gr.Markdown("> **카테고리 → 지역**을 선택하면 결과가 위에 카드 형식으로 나옵니다.")
        result_html = gr.HTML(visible=False, elem_id="result_html")

        # 챗봇 영역 (초기엔 숨김)
        with gr.Column(visible=False, elem_id="chatbot_col") as chatbot_col:
            chatbot = gr.Chatbot(visible=False, elem_id="main_chatbot", type="messages", render_markdown=True)
            with gr.Row(visible=False, elem_id="chat_input_row") as chat_input_row:
                txt = gr.Textbox(show_label=False, placeholder="메시지를 입력하세요...", scale=4, visible=False)
                send_btn = gr.Button("전송", scale=1, visible=False)
        # 챗봇 상태 State(중요)
        chat_state = gr.State(value={"step": 1, "region": None, "food_type": None}) # 일정챗봇은 step:0

        # 하단 고정 버튼
        with gr.Column(elem_id="footer_fixed"):
            with gr.Row(visible=False, elem_id="region_btn_row") as region_btn_row:
                region_buttons = [gr.Button(region) for region in REGIONS]
            with gr.Row(elem_id="cat_row"):
                btns = [gr.Button(cat, variant="secondary") for cat in CATEGORIES]

        category_box = gr.Textbox(value="", visible=False, interactive=False, show_label=False)

        # --- 카테고리 버튼 클릭 시 처리 ---
        def set_category(idx):
            btn_states = [gr.update(variant="primary" if i == idx else "secondary") for i in range(len(CATEGORIES))]
            cat = CATEGORIES[idx]
            if cat == "맛집 및 카페":
                first_msg = {"role": "assistant", "content": random.choice(STEP1_QUESTIONS)}
                return (
                    btn_states +
                    [cat, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False, value=""),
                        gr.update(visible=True, value=[first_msg]),
                        gr.update(visible=True), gr.update(visible=True), gr.update(visible=True),
                        {"step": 1, "region": None, "food_type": None}]
                )
            elif cat in ["인기 숙소", "관광지"]:
                return (
                    btn_states +
                    [cat, gr.update(visible=True), gr.update(visible=False), gr.update(visible=False, value=""),
                        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), {"step": 1, "region": None, "food_type": None}]
                )
            elif cat == "일정":
                first_msgs = [
                    {"role": "assistant", "content": START_MSG},
                    {"role": "assistant", "content": REGION_MSG}
                ]
                return (
                    btn_states +
                    [cat, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False, value=""),
                    gr.update(visible=True, value=first_msgs),
                    gr.update(visible=True), gr.update(visible=True), gr.update(visible=True),
                    {"step": 1, "region": None, "mbti": None, "history": []}]
                )
            else:
                return (
                    btn_states +
                    [cat, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False, value=""),
                        gr.update(visible=True, value=[]), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), {"step": 1, "region": None, "food_type": None}]
                )

        # **출력 컴포넌트 순서 맞추기**
        output_list = btns + [category_box, region_btn_row, chatbot_col, result_html, chatbot, chat_input_row, txt, send_btn, chat_state]
        for i, btn in enumerate(btns):
            def make_click(idx):
                def click_fn():
                    return set_category(idx)
                return click_fn
            btn.click(
                make_click(i),
                inputs=[],
                outputs=output_list,
                preprocess=False,
                show_progress=False
            )

        # 지역 버튼 클릭
        for i, btn in enumerate(region_buttons):
            def show_region(idx):
                def fn(category):
                    cards, visible = show_result(category, REGIONS[idx])
                    return gr.update(value=cards, visible=visible)
                return fn
            btn.click(
                show_region(i),
                inputs=[category_box],
                outputs=result_html
            )

        # ---- 핵심! send_chat 함수 하나만 등록! ----
        def send_chat(txt_val, chat_val, state_val, category_val):
            if category_val == "맛집 및 카페":
                return food_cafe_chatbot(txt_val, chat_val, state_val)
            elif category_val == "일정":
                return schedule_chatbot(txt_val, chat_val, state_val)
            else:
                return "", chat_val, state_val

        send_btn.click(
            send_chat,
            inputs=[txt, chatbot, chat_state, category_box],
            outputs=[txt, chatbot, chat_state]
        )
        txt.submit(
            send_chat,
            inputs=[txt, chatbot, chat_state, category_box],
            outputs=[txt, chatbot, chat_state]
        )

        # --- CSS: 하얀 바탕화면 + 고정 ---
        with open("styles/custom.css", encoding="utf-8") as f:
            css = f.read()
        gr.HTML(f"<style>{css}</style>")

    demo.launch()

if __name__ == "__main__":
    run_app()

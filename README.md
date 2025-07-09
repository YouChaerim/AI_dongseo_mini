# 🛫 Travel Recommend Bot

맛집, 숙소, 항공권 정보를 통합 추천해주고 일정표를 자동으로 만들어주는  
파이썬 기반 웹 챗봇/대시보드 프로젝트  
(Gradio/Streamlit + 카카오로컬API + Skyscanner API + Fly.io 배포)

---

## 1 개발 환경 세팅

### 🔸 Anaconda(Conda) 설치

#### [공식 다운로드 아카이브](https://repo.anaconda.com/archive/)

- **Windows:**  
  `Anaconda3-2024.10-1-Windows-x86_64.exe`
- **Mac:**  
  - **Intel:** `Anaconda3-2024.10-1-MacOSX-x86_64.pkg`
  - **Apple Silicon(M1/M2/M3):** `Anaconda3-2024.10-1-MacOSX-arm64.pkg`

---

### 🔸 Conda 가상환경 생성

```bash
conda create -n mini python=3.10
conda activate mini

---
## 설치 명령어

### gradio, streamlit 설치
- pip install gradio streamlit requests python-dotenv


---
## 실행 명령어
strealit 실행
- streamlit run main_streamlit.py
gradio 실행
- python main_gradio.py
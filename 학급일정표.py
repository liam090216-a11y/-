import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(
    page_title="학급 일정표",
    page_icon="📅",
    layout="wide"
)

# 세션 상태 초기화 (앱 실행 동안 데이터 유지)
if "events" not in st.session_state:
    st.session_state.events = pd.DataFrame(
        [
            {"날짜": "2026-03-02", "반": "1반", "일정 내용": "입학식 및 오리엔테이션", "비고": "강당"},
            {"날짜": "2026-03-15", "반": "전체", "일정 내용": "학급 임원 선거", "비고": "각 교실"},
            {"날짜": "2026-04-20", "반": "2반", "일정 내용": "과학의 날 행사", "비고": "준비물 지참"},
        ]
    )

st.title("📅 우리 반 학급 일정표")
st.caption("Streamlit Cloud를 통해 공유되는 학급 일정 관리 앱입니다.")

# 사이드바: 새 일정 추가
st.sidebar.header("➕ 새 일정 추가")
with st.sidebar.form("add_event_form", clear_on_submit=True):
    event_date = st.date_input("날짜 선택", datetime.now())
    event_class = st.selectbox("대상 학급/범위", ["전체", "1반", "2반", "3반", "기타"])
    event_title = st.text_input("일정 내용")
    event_note = st.text_input("비고 (장소, 준비물 등)")
    
    submitted = st.form_submit_button("일정 등록")
    
    if submitted:
        if event_title.strip() == "":
            st.sidebar.error("일정 내용을 입력해주세요.")
        else:
            new_data = pd.DataFrame([
                {
                    "날짜": event_date.strftime("%Y-%m-%d"),
                    "반": event_class,
                    "일정 내용": event_title,
                    "비고": event_note
                }
            ])
            st.session_state.events = pd.concat([st.session_state.events, new_data], ignore_index=True)
            st.sidebar.success("새 일정이 등록되었습니다!")

# 메인 화면: 일정 필터 및 조회
col1, col2 = st.columns([1, 2])

with col1:
    selected_class = st.selectbox("🔍 학급 필터", ["전체보기"] + list(st.session_state.events["반"].unique()))

# 데이터 정렬 및 필터링
df = st.session_state.events.sort_values(by="날짜").reset_index(drop=True)

if selected_class != "전체보기":
    filtered_df = df[df["반"].isin([selected_class, "전체"])]
else:
    filtered_df = df

# 일정 목록 출력
st.subheader("📋 일정 목록")
st.dataframe(
    filtered_df,
    column_config={
        "날짜": st.column_config.DateColumn("날짜", format="YYYY-MM-DD"),
        "반": "구분",
        "일정 내용": "일정 내용",
        "비고": "비고"
    },
    use_container_width=True,
    hide_index=True
)

# 하단 안내
st.info("💡 **참고:** 입력한 일정 데이터는 앱이 재시작되거나 일정 시간 동안 사용되지 않으면 초기화될 수 있습니다. (영구 저장을 위해서는 Google Sheets 연동 등이 필요합니다.)")

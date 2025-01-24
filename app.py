import streamlit as st
from streamlit_option_menu import option_menu
import random
import pandas as pd
import altair as alt
import my_sql

# 데이터 로드
file_path = 'C:/Users/Admin/Desktop/프로젝트_11월2차/Conversation_History_Analysis/data/6개월_상담데이터.csv'
df = my_sql.db_to_df()

# 와이드 레이아웃 설정
st.set_page_config(layout="wide")

# 날짜 형식 변환
df['통화시작'] = pd.to_datetime(df['통화시작'])

select_month = 1

data_len = len(df)
df['고객만족도'] = random.choices([1,2,3,4,5], weights=[0.1,0.03,0.4,0.13,0.34], k=data_len)

df_filtered = df[df['통화시작'].dt.to_period('M') == select_month]

st.markdown(
    """
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)

# 사이드바 CSS 커스텀
st.markdown(
    """
    <style>
    /* 사이드바 넓이 조정 */
    [data-testid="stSidebar"] {
        width: 100px;
        background-color: rgba(240, 240, 240, 0.7); /* 반투명 배경 */
    }

    /* 사이드바 내부 패딩 및 텍스트 조정 */
    [data-testid="stSidebar"] .css-18e3th9 {
        margin-top:0px;
    }

    /* 사이드바 내부 패딩 및 텍스트 조정 */
    [data-testid="stSidebar"] .css-1d391kg {
        padding: 5px;
        font-size: 8px;
        color: #333;
    }

    /* 사이드바 선택된 항목 스타일 */
    [data-testid="stSidebar"] .css-qrbaxs {
        font-weight: bold;
        color: #e6007e; /* 강조색 */
    }

    /* 옵션 메뉴 간 간격 조정 */
    [data-testid="stSidebar"] .css-1v3fvcr {
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# 사이드바에서 월 선택
with st.sidebar:
    st.markdown("### **월 선택**")
    # 월 선택 (사용자가 선택할 수 있는 월 목록 생성)
    month_options = sorted(df['통화시작'].dt.to_period('M').unique())
    selected_month = st.selectbox("월 선택", month_options)

    # 선택된 월에 해당하는 데이터 필터링
    df_filtered = df[df['통화시작'].dt.to_period('M') == selected_month]

# 첫 번째 사이드바 블록
with st.sidebar:
    st.markdown("### **메뉴**")
    choose_1 = option_menu(
        "",
        ["대시보드", "통화기록", "상담사 관리", "상담사 일정 관리", "설정"],
        icons=['bar-chart-fill', 'headphones', 'people-fill', 'calendar-check', 'gear-fill'],
        menu_icon="person-fill-gear",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "deep pink", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

# 두 번째 사이드바 블록
with st.sidebar:
    st.markdown("### **관리**")
    choose_2 = option_menu(
        "",
        ["로그 분석", "레포트 관리", "회의 일정 관리", "VOC 관리", "지원"],
        icons=['graph-up', 'file-earmark-text', 'calendar-check', 'folder', 'info-circle'],
        menu_icon="list-ul",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "blue", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0288d1"},
        }
    )

# 세 번째 사이드바 블록
with st.sidebar:
    st.markdown("### **이동**")
    choose_3 = option_menu(
        "",
        ["유플러스닷컴", "고객센터 페이지", "공식 온라인 스토어", "LGU+ 그룹웨어", "지원"],
        icons=['house', 'house', 'house', 'house', 'house'],
        menu_icon="list-ul",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "red", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0288d1"},
        }
    )

# 대시보드 타이틀
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h1 style="margin-right: 20px; margin-top: -80px; ">LGU+ 고객센터 관리자 모니터링</h1>
    </div>
    """,
    unsafe_allow_html=True
)

###########################################################################################
from scipy.stats import norm
import numpy as np


def generate_random_index(count):
    return [
        max(0, int(norm.rvs(loc=4, scale=0.3)))
        for _ in range(count)
    ]



# 전체 레이아웃 컨테이너
with st.container():
    col1, col2 = st.columns([2, 8])  # 비율을 조정하여 타이틀과 KPI 너비를 설정
    with col1:
        st.markdown(
            """
            <h1 style="font-family: 'Arial'; font-size: 36px; text-align: center; color: #e6007e;">2팀 KPI</h1>
            """,
            unsafe_allow_html=True
        )  # 타이틀 폰트 수정 및 가운데 정렬
    with col2:
        # 각 메트릭을 담을 박스 스타일 설정
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 10px; padding: 10px 1px 3px 1px; text-align: center;">
                    <h5>금일 상담 건수</h5>
                    <p style="font-size: 16px; color: #333;">{:,} 건</p>
                </div>
                """.format(len(df_filtered)),
                unsafe_allow_html=True
            )
        with kpi_col2:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 10px; padding: 10px 1px 3px 1px; text-align: center;">
                    <h5>근무중</h5>
                    <p style="font-size: 18px; color: #333;">25명</p>
                </div>
                """.format((df_filtered['발신유형'].value_counts().get('IB', 0) / len(df) * 100)),
                unsafe_allow_html=True
            )
        with kpi_col3:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 10px; padding: 10px 1px 3px 1px; text-align: center;">
                    <h5>후처리</h5>
                    <p style="font-size: 18px; color: #333;">7명</p>
                </div>
                """.format(df_filtered['통화시간'].mean()),
                unsafe_allow_html=True
            )
        with kpi_col4:
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.1); border-radius: 10px; padding: 10px 1px 3px 1px; text-align: center;">
                    <h5>고객 만족도 평균</h5>
                    <p style="font-size: 18px; color: #333;">{:.1f} 점</p>
                </div>
                """.format(df_filtered['고객만족도'].mean()),
                unsafe_allow_html=True
            )

    # 두 번째 줄: 상담 분류별 건수, 월별 상담 건수
    row1_col1, row1_col2, row1_col3 = st.columns([1, 1, 1])
    with row1_col1:
        st.markdown("### 상담 유형별 상담 건수")

        result = df_filtered['상담유형'].value_counts().reset_index()
        result.columns = ['상담유형', '건수']

        category_chart = alt.Chart(result).mark_bar().encode(
            x=alt.X('상담유형', sort='-y'),
            y='건수',
            color=alt.Color('상담유형', legend=None)  # 범례 제거
        ).properties(width=450, height=300)

        st.altair_chart(category_chart)

    with row1_col2:
        st.markdown("### 월별 상담 건수")
        monthly_counts = df.groupby(df['통화시작'].dt.to_period('M')).size().reset_index(name='건수')
        monthly_chart = alt.Chart(monthly_counts).mark_line(point=True).encode(
            x=alt.X('통화시작:T'),
            y='건수',
            tooltip=['통화시작:T', '건수']
        ).properties(width=450, height=300)
        st.altair_chart(monthly_chart)

    with row1_col3:
        st.markdown("### 고객 만족도 분포")

        result = df_filtered['고객만족도'].value_counts().reset_index().sort_values(by=['고객만족도'], axis=0, ignore_index=True)
        result.columns = ['고객만족도', '건수']
        print(result)

        satisfaction_chart = alt.Chart(result).mark_bar().encode(
            x=alt.X('고객만족도:O', title='고객만족도'),
            y='건수',
            color=alt.Color('고객만족도:O', legend=None)  # 범례 제거
        ).properties(width=450, height=300)
        st.altair_chart(satisfaction_chart)

    # 세 번째 줄: 고객 만족도, 상담사별 처리 건수
    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])
    with row2_col1:
        st.markdown("### 상담사별 처리 건수 Top 10")

        result = df_filtered['상담사'].value_counts().reset_index()
        result.columns = ['상담사', '건수']

        agent_chart = alt.Chart(result).mark_bar().encode(
            x=alt.X('상담사', sort='-y'),
            y='건수',
            color='상담사'
        ).properties(width=450, height=300)
        st.altair_chart(agent_chart)

    with row2_col2:
        st.markdown("### 키워드 분포도")
        # 키워드별 빈도 계산
        keyword_counts = df['키워드'].value_counts().reset_index()
        keyword_counts.columns = ['키워드', '건수']

        # 막대 그래프 생성
        keyword_chart = alt.Chart(keyword_counts).mark_bar().encode(
            x=alt.X('키워드', sort='-y', title='키워드'),
            y=alt.Y('건수', title='건수'),
            color=alt.Color('키워드', legend=None)  # 범례 제거
        ).properties(width=450, height=300)

        st.altair_chart(keyword_chart)

    # 다섯 번째 줄: 공지사항
    with row2_col3:
        st.markdown("### 공지사항")
        st.info(
            """
            - [교육] 24년 12월 정규 교육 안내
            - [인사] 24년 하반기 KPI 공지
            - [마케팅] 12월 프로모션 관련 안내
            """
        )
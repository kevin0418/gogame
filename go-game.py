#
# 바둑이란  ? 
#

import streamlit as st

# 페이지 설정 (배경색 등 추가 가능)
st.set_page_config(page_title="바둑 이란 ", layout="wide")

# CSS 스타일 적용
st.markdown("""
<style>
    /* 버튼 색상 커스텀 */
    .stButton>button {
        background-color: #4CAF50;  /* 초록색 계열 */
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;  /* 호버 시 색상 변경 */
    }
    
    /* 특정 버튼 별도 색상 지정 */
    #video-btn { background-color: #FF5722 !important; }  /* 주황색 */
    #talk-btn { background-color: #2196F3 !important; }   /* 파란색 */
    #ppt-btn { background-color: #9C27B0 !important; }     /* 보라색 */
    
    /* 강조 텍스트 스타일 */
    .highlight {
        font-weight: bold;
        color: #FF5722;  /* 주황색 */
    }
    .note {
        font-size: 14px;
        color: #666;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.write("### 바둑 이란 ? 👋")
st.write("##### by Brisbane 바둑회")

# 설명 텍스트 (bold 및 색상 적용)
st.markdown("""
<span class="highlight">바둑이 뭘까요, 단순히 시간보내는 게임일까요</span>  
여기 Kevin이 맛깔나게 여러 인공지능을 통해 풀어 봅니다. 

<span class="highlight">바둑: 수양과 통찰의 장</span>           

선비들이 바둑을 통해 **"정중동, 선견지명, 군자의 덕목"** 을  
            
바둑이 유교, 불교, 도교가 융합된 조선 시대에 자기 성찰의 실천적 수단으로   
            
바둑과 기도는 무욕과 진심을 닦는 길

            기본 자료: 홍 회원 제공  
<span class="highlight">아래 몇편의 비디오를 보시길</span>  
""", unsafe_allow_html=True)


# Video 링크 버튼
st.link_button("Video 로 보기 by Kevin", "https://youtu.be/MJ5TkSeyqgk")

# # 대화 링크 버튼
st.link_button("대화 를 통해 듣기", "https://youtu.be/675u_xrTxIY")
# Video 링크 버튼
st.link_button("Video 로 보기 by AI", "https://youtu.be/U5ElKAQTJVo")

# # 대화 링크 버튼
# st.link_button("바둑회원 자격문제 ", "https://youtu.be/Nwl5T50elYU")


st.caption("화면이 안나오면 (zzz) 클릭하고 기다리면 됩니다, 1-2 분정도")



import streamlit as st
import pdfplumber
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import openai
from transformers import pipeline
import tempfile
import os

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Brisbane 바둑회",
    page_icon="📚",
    layout="wide"
)

# 타이틀
st.title("📚 Brisnane 바둑 회")
st.markdown("정신 수양을 위한 도장,  입회 시험문제")

# 사이드바 설정
with st.sidebar:
    st.header("")
    
    # API 키 입력
    # openai_api_key = st.text_input(
    #     "OpenAI API 키",
    #     type="password",
    #     placeholder="sk-...",
    #     help="OpenAI API 키를 입력하세요"
    # )
    
    openai_api_key = st.secrets["api_keys"]["my_api_key"] 

    # 문제 생성 옵션
    st.subheader("문제 생성 옵션")
    use_openai = st.checkbox("OpenAI GPT-4 사용", value=True)
    use_huggingface = st.checkbox("HuggingFace 모델 사용", value=False)
    use_openai = st.checkbox("", value=True)
    use_huggingface = st.checkbox("", value=False)
    
    # 텍스트 길이 제한
    text_limit = st.slider(
        "텍스트 길이 제한 (문자)",
        min_value=500,
        max_value=5000,
        value=3000,
        step=500
    )

# 파일 업로드 섹션
# uploaded_file = st.file_uploader(
#     "PDF 파일을 업로드하세요",
#     type="pdf",
#     help="문제를 생성할 PDF 파일을 선택하세요"
# )
uploaded_file = "go-question.pdf"

with open(uploaded_file, 'rb') as f:
    pdf_content = f.read()
    # 이제 pdf_content를 사용하여 필요한 작업 수행

def extract_text_from_pdf(pdf_file_path):
    """PDF에서 텍스트 추출"""
    with open(pdf_file_path, 'rb') as pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_file.read())
            tmp_path = tmp_file.name

    try:
        with pdfplumber.open(tmp_path) as pdf:
            text = "".join(page.extract_text() or "" for page in pdf.pages)
        return text
    finally:
        # tmp_path 파일 삭제 (optional)
        os.remove(tmp_path)


# def extract_text_from_pdf(pdf_file):
#     """PDF에서 텍스트 추출"""
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#         tmp_file.write(pdf_file.read())
#         tmp_path = tmp_file.name
    
#     try:
#         with pdfplumber.open(tmp_path) as pdf:
#             text = "".join(page.extract_text() or "" for page in pdf.pages)
#         return text
#     finally:
#         os.unlink(tmp_path)

def preprocess_text(text):
    """텍스트 전처리"""
    # 문장 분할
    sentences = sent_tokenize(text)
    
    # 키워드 추출
    # keywords =  # 또는 None
    keywords = []
    if 'keywords' in locals() and keywords:
    # keywords가 존재하고 비어있지 않은 경우의 처리
    #f keywords.any():  # 또는 if len(keywords) > 0:
        try:
            vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
            keywords_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            keywords = feature_names[:10]  # 상위 10개 키워드
        except:
            keywords = []
    
    return sentences, keywords

def generate_questions_with_openai(text, api_key, text_limit):
    """OpenAI를 사용하여 문제 생성"""
    if not api_key:
        return "❌ OpenAI API 키를 입력해주세요."
    
    openai.api_key = api_key
    
    prompt = f"""
    다음 텍스트에서 다양한 유형의 문제를 각각 1개씩 생성해주세요.
    각 문제에는 정답과 설명을 포함해주세요.
    
    생성할 문제 유형:
    - 객관식 문제 (Multiple Choice)
    - 주관식 문제 (Short Answer)
    - 진위형 문제 (True/False)
    - 빈칸 채우기 문제 (Fill-in-the-Blank)
    - 연결형 문제 (Matching)
    
    텍스트: {text[:text_limit]}
    
    출력 형식:
    각 문제는 다음과 같은 형식으로 작성해주세요:
    [유형] 문제 제목
    ❓ 문제 내용
    ✅ 정답: 
    💡 설명:
    ---
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ OpenAI API 호출 중 오류 발생: {str(e)}"

def generate_questions_with_huggingface(text):
    """HuggingFace 모델을 사용하여 문제 생성"""
    try:
        qa_generator = pipeline(
            "text2text-generation", 
            model="mrm8488/t5-base-finetuned-question-generation-ap"
        )
        generated_questions = qa_generator(text[:512])
        return generated_questions
    except Exception as e:
        return f"❌ HuggingFace 모델 호출 중 오류 발생: {str(e)}"

# 메인 처리 로직
if uploaded_file is not None:
    # 진행률 표시기
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 1. 텍스트 추출
    status_text.text("PDF에서 텍스트 추출 중...")
    extracted_text = extract_text_from_pdf(uploaded_file)
    progress_bar.progress(25)
    
    if not extracted_text.strip():
        st.error("❌ PDF에서 텍스트를 추출할 수 없습니다. 다른 파일을 시도해주세요.")
        st.stop()
    
    # 2. 텍스트 전처리
    status_text.text("텍스트 전처리 중...")
    sentences, keywords = preprocess_text(extracted_text)
    progress_bar.progress(50)
    
    # 추출된 정보 표시
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("📄 추출된 텍스트 미리보기", expanded=False):
            st.text_area("텍스트", extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text, height=200)
    
    with col2:
        with st.expander("🔍 추출된 키워드", expanded=False):
            if keywords:
                st.write(", ".join(keywords))
            else:
                st.write("키워드를 추출할 수 없습니다.")
        
        with st.expander("📊 통계", expanded=False):
            st.write(f"- 총 문자 수: {len(extracted_text):,}")
            st.write(f"- 문장 수: {len(sentences)}")
            st.write(f"- 사용된 텍스트 길이: {min(len(extracted_text), text_limit):,}")
    
    # 3. 문제 생성
    status_text.text("문제 생성 중...")
    progress_bar.progress(75)
    
    # 결과를 표시할 탭 생성
    tab1, tab2 = st.tabs(["📝 생성된 문제", "🔧 상세 정보"])
    
    with tab1:
        st.subheader("🤖 AI 생성 문제")
        
        # OpenAI를 사용한 문제 생성
        if use_openai:
            st.markdown("### OpenAI GPT-4로 생성된 문제")
            with st.spinner("OpenAI가 문제를 생성 중입니다..."):
                openai_questions = generate_questions_with_openai(
                    extracted_text, openai_api_key, text_limit
                )
            
            if openai_questions.startswith("❌"):
                st.error(openai_questions)
            else:
                # 생성된 문제를 보기 좋게 formatting
                questions_display = openai_questions.replace("✅", "\n✅")
                questions_display = questions_display.replace("💡", "\n💡")
                questions_display = questions_display.replace("---", "\n" + "="*50 + "\n")
                
                st.markdown(questions_display)
        
        # HuggingFace를 사용한 문제 생성
        if use_huggingface:
            st.markdown("### HuggingFace 모델로 생성된 문제")
            with st.spinner("HuggingFace 모델이 문제를 생성 중입니다..."):
                hf_questions = generate_questions_with_huggingface(extracted_text)
            
            if isinstance(hf_questions, list):
                for i, q in enumerate(hf_questions, 1):
                    st.write(f"**Q{i}:** {q.get('generated_text', '')}")
            else:
                st.error(hf_questions)
    
    with tab2:
        st.subheader("상세 정보")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 문장 목록")
            for i, sentence in enumerate(sentences[:10], 1):
                st.write(f"{i}. {sentence}")
            
            if len(sentences) > 10:
                st.info(f"... 외 {len(sentences) - 10}개 문장 더 있음")
        
        with col2:
            st.markdown("#### 처리 로그")
            st.success("✅ PDF 텍스트 추출 완료")
            st.success("✅ 텍스트 전처리 완료")
            if use_openai:
                if openai_questions and not openai_questions.startswith("❌"):
                    st.success("✅ OpenAI 문제 생성 완료")
                else:
                    st.error("❌ OpenAI 문제 생성 실패")
            if use_huggingface:
                if isinstance(hf_questions, list):
                    st.success("✅ HuggingFace 문제 생성 완료")
                else:
                    st.error("❌ HuggingFace 문제 생성 실패")
    
    # 진행률 완료
    progress_bar.progress(100)
    status_text.text("✅ 문제 생성 완료!")
    
    # 다운로드 버튼
    if use_openai and openai_questions and not openai_questions.startswith("❌"):
        st.download_button(
            label="📥 생성된 문제 다운로드",
            data=openai_questions,
            file_name="generated_questions.txt",
            mime="text/plain"
        )

else:
    # 파일 업로드 전 안내 메시지
    st.info("👆 사이드바에서 설정을调整하고 PDF 파일을 업로드해주세요.")
    
    # 사용법 안내
    with st.expander("📖 사용법", expanded=True):
        st.markdown("""
        1. **파일 업로드**: 문제를 생성할 PDF 파일을 업로드하세요
        2. **API 설정**: OpenAI API 키를 입력하세요 (선택사항)
        3. **모델 선택**: 사용할 AI 모델을 선택하세요
        4. **생성 시작**: 파일 업로드 후 자동으로 문제가 생성됩니다
        
        **지원되는 문제 유형:**
        - 객관식 문제
        - 주관식 문제  
        - 진위형 문제
        - 빈칸 채우기
        - 연결형 문제
        """)

# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "PDF 문제 생성기 | AI-powered Quiz Generator"
    "</div>",
    unsafe_allow_html=True
)
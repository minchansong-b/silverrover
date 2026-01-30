import streamlit as st
from pypdf import PdfReader
from analysis_logic import analyze_report
import os

# Streamlit Page Config
st.set_page_config(
    page_title="딥앤그로우 AI 아동 기질발달 분석 리포트",
    page_icon="👶",
    layout="wide"
)

# Logo
st.image("logo.png", width=400) 
st.title("딥앤그로우 AI 아동 기질발달 분석 리포트")
st.markdown("""
임상심리 전문지식을 학습한 AI를 통해 아이의 기질과 발달에 대한 분석을 기반의 심층 리포트를 제공하는 서비스입니다.
""")

# Sidebar for API Key
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("OpenAI API Key", type="password", help="분석을 위해 API 키가 필요합니다.")
    st.info("API 키는 서버에 저장되지 않으며 일회성 요청에만 사용됩니다.")

# Main Input Section
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 보고서 업로드")
    uploaded_files = st.file_uploader("K-CDI, J-TCI, K-TABS 등 보고서만 업로드해주세요 (최대 3개)", type=['pdf', 'txt'], accept_multiple_files=True)
    
    if uploaded_files and len(uploaded_files) > 3:
        st.error("최대 3개의 파일까지만 업로드가 가능합니다.")
        uploaded_files = uploaded_files[:3]

    input_text = st.text_area("초기상담신청서 내용을 붙여넣어주세요", height=300)

    analyze_btn = st.button("분석 시작", type="primary", use_container_width=True)

# Analysis Logic
if analyze_btn:
    if not api_key:
        st.error("API Key를 입력해주세요.")
    else:
        text_content = ""
        
        # 1. Process Files
        if uploaded_files:
            for uploaded_file in uploaded_files:
                text_content += f"\n--- File: {uploaded_file.name} ---\n"
                if uploaded_file.name.endswith('.pdf'):
                    try:
                        pdf_reader = PdfReader(uploaded_file)
                        for page in pdf_reader.pages:
                            text_content += page.extract_text()
                    except Exception as e:
                        st.error(f"{uploaded_file.name} 읽기 오류: {e}")
                elif uploaded_file.name.endswith('.txt'):
                    text_content += uploaded_file.read().decode("utf-8")
        
        # 2. Append Manual Input
        if input_text:
            text_content += "\n" + input_text

        # 3. Call Analysis
        if not text_content.strip():
            st.warning("분석할 내용을 입력하거나 파일을 업로드해주세요.")
        else:
            with col2:
                st.subheader("📊 분석 결과")
                with st.spinner("전문가가 분석 중입니다... 잠시만 기다려주세요."):
                    result = analyze_report(api_key, text_content)
                    st.markdown(result)

# Footer
st.markdown("---")
st.caption("본 서비스는 AI 기반 분석 도구입니다. 정확한 진단은 전문의와 상의하십시오.")

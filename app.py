import streamlit as st
from pypdf import PdfReader
from analysis_logic import analyze_report
import os

# Streamlit Page Config
st.set_page_config(
    page_title="영유아 발달 & 기질 분석 서비스",
    page_icon="👶",
    layout="wide"
)

st.title("👶 영유아 기질 및 발달 검사 분석 서비스")
st.markdown("""
임상심리 전문가 AI가 아이의 기질과 발달라 보고서를 분석하여 양육 가이드와 액션 아이템을 제공합니다.
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
    uploaded_file = st.file_uploader("PDF 또는 텍스트 파일을 업로드하세요", type=['pdf', 'txt'])
    
    input_text = st.text_area("또는 텍스트를 직접 입력하세요", height=300)

    analyze_btn = st.button("분석 시작", type="primary", use_container_width=True)

# Analysis Logic
if analyze_btn:
    if not api_key:
        st.error("API Key를 입력해주세요.")
    else:
        text_content = ""
        
        # 1. Process File
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.pdf'):
                try:
                    pdf_reader = PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text()
                except Exception as e:
                    st.error(f"PDF 읽기 오류: {e}")
            elif uploaded_file.name.endswith('.txt'):
                text_content = uploaded_file.read().decode("utf-8")
        
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

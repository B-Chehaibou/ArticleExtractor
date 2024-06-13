import streamlit as st
import pandas as pd
import openai_helper
import PyPDF2
import openai

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

st.markdown(
    """
    <style>
    .stColumns > div {
        padding-left: 2rem;
        font-size: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Streamlit layout
st.title("Information Extractor")

openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if openai_api_key:
    openai.api_key = openai_api_key
# Create columns
    left_column,_, right_column = st.columns([3,0.3, 3])

    # Left column: PDF upload and extract button
    with left_column:
        st.header("Insert your article")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            if st.button("Extract"):
                pdf_text = extract_text_from_pdf(uploaded_file)
                df = openai_helper.extract(pdf_text)
                st.session_state['df'] = df  # Store DataFrame in session state
            else:
                df = st.session_state.get('df', None)
        else:
            df = None

    # Right column: Display DataFrame
    with right_column:
        st.header("Extracted Information")
        if df is not None:
            st.dataframe(df)
        else:
            st.write("No data to display")

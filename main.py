import streamlit as st
import pandas as pd
import PyPDF2
import openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
import json
import pandas as pd




system_message = """
I will provide you with a text excerpt from a scientific paper in the field of colloidal nanocrystals.

Your task is to extract the following key information:
1. **First author name**: The name of the first author of the paper.
2. **Journal name**: The name of the journal where the paper is published.
3. **Date of publication**: The date when the paper was published.
4. **Nanocrystal composition (NC composition)**: The chemical composition of the nanocrystals. Note that "nanocrystal" can be abbreviated as "NC". Examples of NC compositions include:
   - Single materials: PbS, CdSe, HgTe
   - Mixed materials: PbS/CdSe
   - Different materials: PbS and CdSe
5. **Diameter of the NC in nanometers (nm)**: The size of the nanocrystals. If the study includes multiple sizes, provide the range (e.g., 3-5 nm).
6. **DOI**: The DOI (Digital Object Identifier) of the article is a unique identifier.
**Attention**: If you cannot find any of the information, output an empty string (""). Do not make up any information.

Output the extracted information in the following JSON format:
{
    "First author": "First author name",
    "Journal": "Journal name",
    "Date of publication": "Date of publication",
    "NC composition": "NC composition",
    "NC diameter": "NC diameter",
    "DOI": "DOI"
}
"""

def extract(text,openai_key):
    # Initialize model and parser
    model = ChatOpenAI(openai_api_key = openai_key)
    parser = StrOutputParser()

    chain = model | parser
    messages = [
        SystemMessage(
            content=system_message
        ),
        HumanMessage(
            content=text
        ),
    ]
    try:
        response = chain.invoke(messages)
        data = json.loads(response)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error processing JSON: {e}")
        return pd.DataFrame(columns=["Measure", "Value"])



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

#openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

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
                df = extract(pdf_text,openai_api_key)
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

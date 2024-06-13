from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.output_parsers import StrOutputParser
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

# Example usage (this part would be used in your Streamlit app or other interface)
if __name__ == "__main__":
    example_text = """Your scientific paper text goes here."""
    df = extract(example_text)
    print(df)

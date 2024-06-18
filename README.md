# ArticleExtractor

ArticleExtractor is a tool designed to extract key information from scientific papers, including author names, journal names, publication dates, and nanocrystal compositions.

## Files

openai_helper.py : contain the openai api to extract information from a text
main.py : call the openai_helper to obtain the information and create the streamlit app
requirements.txt : contain the librairies used

## Features

- Extracts first author name
- Extracts journal name
- Extracts date of publication
- Extracts nanocrystal composition
- Extracts diameter of nanocrystals in nanometers (nm)

## How to use it

pip install -r requirements.txt
streamlit run main.py

You need to create an account on openai website.
Once you get an api key from your account add it the prompt.


import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs

def extract_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

def parse_utm_params(url):
    parsed_url = urlparse(url)
    utm_params = parse_qs(parsed_url.query)
    return {k: v[0] if v else None for k, v in utm_params.items()}

def main():
    st.title("Email Campaign URL Extractor")

    uploaded_file = st.file_uploader("Upload your HTML file", type=['html'])
    if uploaded_file is not None:
        html_content = uploaded_file.getvalue().decode()
        urls = extract_urls(html_content)
        
        if urls:
            st.success(f"Found {len(urls)} URLs in the document")
            url_data = pd.DataFrame({
                "URL": urls,
                "UTM Parameters": [parse_utm_params(url) for url in urls]
            })
            st.write(url_data)
            frequency = url_data['URL'].value_counts().reset_index()
            frequency.columns = ['URL', 'Count']
            st.write(frequency)
        else:
            st.error("No URLs found in the uploaded HTML file.")

if __name__ == "__main__":
    main()

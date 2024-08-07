from streamlit_pdf_viewer import pdf_viewer
from dotenv import load_dotenv
import streamlit as st
import requests
import os

load_dotenv()

QUOTATION_API_URL = os.getenv("QUOTATION_API_URL")

st.title("Quote Generator")
st.write("Enter the text to generate a quote in PDF")

input_text = st.text_area("Input text", height=200,
                          placeholder="Example: \n make a quote for Eco \n 10 cap \n 5 t-shirt short \n 100 meter of low res canvas \n Agent John Doe")

if "pdf_ref" not in st.session_state:
    st.session_state["pdf_ref"] = None

if st.button("Generate quotation", type='primary', use_container_width=True):
    # Call to the FastAPI endpoint
    try:
        response = requests.post(
            url=QUOTATION_API_URL, # type: ignore
            json={"text": input_text}
        )
        response.raise_for_status()

        # Read the PDF content from the response
        pdf_content = response.content

        st.session_state["pdf_ref"] = pdf_content

    except requests.exceptions.RequestException as e:
        st.error(f"Error generating the PDF: {e}")

# Display the PDF file if available in the session state
if st.session_state["pdf_ref"]:
    st.write("PDF Preview:")
    pdf_viewer(input=st.session_state["pdf_ref"], width=700)
    
    # Provide an option to download the PDF
    st.download_button(
        label="Download PDF",
        data=st.session_state["pdf_ref"],
        file_name="Quotation.pdf",
        mime="application/pdf",
        type="primary"
    )
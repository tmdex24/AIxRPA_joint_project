import streamlit as st
import requests
import base64

BACKEND_URL = "http://localhost:8000/upload"

st.set_page_config(
    page_title="AI Invoice Processing",
    layout="wide"
)

st.title("📄 AI Invoice Processing System")

uploaded_file = st.file_uploader(
    "Upload PDF Invoice",
    type=["pdf"]
)

if uploaded_file:

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("PDF Preview")

        pdf_bytes = uploaded_file.read()

        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

        pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="800"
            type="application/pdf">
        </iframe>
        """
        st.markdown(
            pdf_display,
            unsafe_allow_html=True)
        
    with col2: 
        
        st.markdown("Extracted Data")

        if st.button("Process Invoice"):

            files = {
                "file": (
                    uploaded_file.name,
                    pdf_bytes,
                    "application/pdf"
                )
            }

            with st.spinner("Processing invoice..."):

                response = requests.post(
                    BACKEND_URL,
                    files=files
                )

            if response.status_code == 200:

                st.write(response.status_code)
                st.write(response.text)
                
                data = response.json()

                st.json(data)

                invoice = data.get("invoice")

                if invoice is None:
                    st.error("Invoice data not found.")
                    st.stop()
                
                st.success("Invoice processed successfully!")

                st.text_input(
                    "Invoice Number",
                    invoice.get(
                        "invoice_number",
                        ""
                    ),
                    disabled=True
                )

                st.text_input(
                    "Date of Issue",
                    invoice.get(
                        "date_of_issue",
                        ""
                    ),
                    disabled=True
                )

                st.text_input(
                    "Client Name",
                    invoice.get(
                        "client_name",
                        ""
                    ),
                    disabled=True
                )

                st.text_input(
                    "Client Tax ID",
                    invoice.get(
                        "client_tax_id",
                        ""
                    ),
                    disabled=True
                )

                st.text_input(
                    "Total Amount",
                    str(
                        invoice.get(
                            "total_amount",
                            ""
                        )
                    ),
                    disabled=True
                )

                st.text_input(
                    "Currency",
                    invoice.get(
                        "currency",
                        ""
                    ),
                    disabled=True
                )

            else:
                st.error(
                    f"Backend error: {response.status_code}"
                )
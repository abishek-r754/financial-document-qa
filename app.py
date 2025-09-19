import streamlit as st
import pandas as pd
import pdfplumber

st.title("📊 Financial Document Q&A Assistant (Fresher Demo)")

# Upload a file (Excel or PDF) - unique key
uploaded_file = st.file_uploader("Upload a financial document (PDF or Excel)", type=["pdf", "xlsx"], key="file_upload")

if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        st.success("✅ You uploaded a PDF file")
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        st.text_area("PDF Content Preview", text[:1000], height=200)

    elif uploaded_file.name.endswith(".xlsx"):
        st.success("✅ You uploaded an Excel file")
        df = pd.read_excel(uploaded_file)
        st.dataframe(df.head())

        # Q&A Section
        question = st.text_input("Ask a question (try 'revenue', 'expenses', 'profit'):", key="qna_box")

        if question:
            q = question.lower()
            answer = None

            # Try to find values by column names
            if "revenue" in q and "Revenue" in df.columns:
                answer = df["Revenue"].sum()
            elif "expenses" in q and "Expenses" in df.columns:
                answer = df["Expenses"].sum()
            elif "profit" in q and "Profit" in df.columns:
                answer = df["Profit"].sum()

            if answer is not None:
                st.success(f"Answer: {answer}")
            else:
                st.warning("Sorry, I couldn't find that information in the Excel file.")
else:
    st.info("Please upload a file to continue.")

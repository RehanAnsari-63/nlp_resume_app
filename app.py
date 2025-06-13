import os
import zipfile
import pandas as pd
import streamlit as st
from resume_parser import parse_resume

st.title("🧠 AI Resume Parser App")
st.write("Upload a **single resume** or a **ZIP file** of multiple resumes to extract:")
st.markdown("**Name | Email | Phone | Company | Skills**")

uploaded_file = st.file_uploader("Upload a single resume or a ZIP file", type=["pdf", "docx", "zip"])
output_data = []

if uploaded_file:
    temp_dir = "temp_resumes"
    os.makedirs(temp_dir, exist_ok=True)

    if uploaded_file.type == "application/zip":
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        st.success("✅ ZIP extracted successfully.")
        resume_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]

    else:
        resume_path = os.path.join(temp_dir, uploaded_file.name)
        with open(resume_path, "wb") as f:
            f.write(uploaded_file.read())
        resume_files = [resume_path]
        st.success("✅ Single resume uploaded.")

    for resume in resume_files:
        data = parse_resume(resume)
        if data:
            output_data.append(data)

    if output_data:
        df = pd.DataFrame(output_data)
        st.dataframe(df)

        output_excel = "parsed_resumes.xlsx"
        df.to_excel(output_excel, index=False)
        with open(output_excel, "rb") as f:
            st.download_button("📥 Download Excel", f, file_name="parsed_resumes.xlsx")

    else:
        st.warning("⚠️ No data extracted. Please check the file format or content.")

if os.path.exists("temp_resumes"):
    for f in os.listdir("temp_resumes"):
        os.remove(os.path.join("temp_resumes", f))

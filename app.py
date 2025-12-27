import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄")

# 2. إضافة خيار تحويل اللغة في الشريط الجانبي (Sidebar)
# هذا الجزء هو المسؤول عن "الزر" الذي طلبته
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. تخصيص النصوص بناءً على اختيار اللغة
if language == "العربية":
    title = "📄 YouToPDF - دمج ملفات PDF"
    desc = "أداة مجانية وسريعة لدمج ملفات PDF في ملف واحد."
    upload_msg = "اختر ملفات PDF"
    btn_msg = "دمج الملفات الآن"
    success_msg = "تم الدمج بنجاح!"
    dl_btn = "تحميل الملف"
else:
    title = "📄 YouToPDF - PDF Merger"
    desc = "Free and fast tool to merge PDF files into one."
    upload_msg = "Choose PDF files"
    btn_msg = "Merge Files Now"
    success_msg = "Merged successfully!"
    dl_btn = "Download File"

# 4. عرض محتوى الواجهة
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{desc}</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(upload_msg, type="pdf", accept_multiple_files=True)

if st.button(btn_msg):
    if uploaded_files and len(uploaded_files) >= 2:
        merger = PdfMerger()
        for pdf in uploaded_files:
            merger.append(pdf)
        
        output = BytesIO()
        merger.write(output)
        
        st.success(success_msg)
        st.download_button(dl_btn, output.getvalue(), "merged.pdf", "application/pdf")
    else:
        st.warning("يرجى رفع ملفين على الأقل / Please upload at least 2 files")

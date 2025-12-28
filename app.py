import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄")

# 2. خيار اللغة في الشريط الجانبي
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. تخصيص النصوص بناءً على اختيار اللغة
if language == "العربية":
    title = "📄 YouToPDF - دمج ملفات PDF"
    desc = "أداة مجانية وسريعة لدمج ملفات PDF في ملف واحد."
    upload_msg = "اختر ملفات PDF (سيتم الدمج حسب ترتيب الاختيار)"
    btn_msg = "دمج الملفات الآن"
    success_msg = "تم الدمج بنجاح!"
    dl_btn = "تحميل الملف"
    warning_msg = "يرجى رفع ملفين على الأقل"
    processing_msg = "جاري الدمج..."
else:
    title = "📄 YouToPDF - PDF Merger"
    desc = "Free and fast tool to merge PDF files into one."
    upload_msg = "Choose PDF files (Files will be merged in selection order)"
    btn_msg = "Merge Files Now"
    success_msg = "Merged successfully!"
    dl_btn = "Download File"
    warning_msg = "Please upload at least 2 files"
    processing_msg = "Merging..."

# 4. عرض محتوى الواجهة
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{desc}</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(upload_msg, type="pdf", accept_multiple_files=True)

if st.button(btn_msg):
    if uploaded_files and len(uploaded_files) >= 2:
        with st.spinner(processing_msg):
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            
            output = BytesIO()
            merger.write(output)
            merger.close()  # إغلاق الكائن لتحرير الموارد
            
            st.success(success_msg)
            st.download_button(
                label=dl_btn,
                data=output.getvalue(),
                file_name="merged_document.pdf",
                mime="application/pdf"
            )
    else:
        st.warning(warning_msg)

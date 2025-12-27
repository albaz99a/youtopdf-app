import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="YouToPDF - Merge PDF Online",
    page_icon="📄",
    layout="centered"
)

# 2. إضافة خيار اللغة في الشريط الجانبي
language = st.sidebar.selectbox("Choose Language / اختر اللغة", ["العربية", "English"])

# إعدادات النصوص بناءً على اللغة المختارة
if language == "العربية":
    title = "📄 YouToPDF - دمج ملفات PDF"
    description = "أداة مجانية وسريعة لدمج ملفات PDF في ملف واحد احترافي."
    upload_label = "اختر ملفات PDF لدمجها"
    button_label = "دمج الملفات الآن"
    success_msg = "تم دمج الملفات بنجاح!"
    download_label = "تحميل الملف المدمج"
    error_msg = "الرجاء رفع ملفين على الأقل للدمج."
    footer_text = "حقوق النشر © 2025 YouToPDF. جميع الحقوق محفوظة."
else:
    title = "📄 YouToPDF - Merge PDF Files"
    description = "Free and fast tool to merge multiple PDF files into one professional document."
    upload_label = "Choose PDF files to merge"
    button_label = "Merge Files Now"
    success_msg = "Files merged successfully!"
    download_label = "Download Merged File"
    error_msg = "Please upload at least two files to merge."
    footer_text = "Copyright © 2025 YouToPDF. All rights reserved."

# 3. عرض الواجهة
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{description}</p>", unsafe_allow_html=True)
st.divider()

# 4. منطقة رفع الملفات
uploaded_files = st.file_uploader(upload_label, type="pdf", accept_multiple_files=True)

if st.button(button_label):
    if uploaded_files and len(uploaded_files) >= 2:
        merger = PdfMerger()
        for pdf in uploaded_files:
            merger.append(pdf)
        
        # حفظ النتيجة في الذاكرة
        output = BytesIO()
        merger.write(output)
        
        st.success(success_msg)
        st.download_button(
            label=download_label,
            data=output.getvalue(),
            file_name="YouToPDF_Merged.pdf",
            mime="application/pdf"
        )
    else:
        st.error(error_msg)

# 5. تذييل الصفحة (Footer) مهم جداً للمصداقية
st.divider()
st.caption(footer_text)

import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄")

# 2. خيار اللغة في الشريط الجانبي
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. تخصيص النصوص والستايل بناءً على اللغة
if language == "العربية":
    st.markdown("""<style> .main {text-align: right; direction: rtl;} div.stButton > button {width: 100%;} </style>""", unsafe_allow_html=True)
    title = "📄 YouToPDF - دمج ملفات PDF"
    desc = "أداة مجانية وسريعة لدمج ملفات PDF في ملف واحد بشكل آمن."
    upload_msg = "اختر ملفات PDF لدمجها"
    btn_msg = "ابدأ عملية الدمج"
    privacy_title = "🔒 سياسة الخصوصية والأمان"
    privacy_text = "نحن نهتم بخصوصيتك؛ يتم معالجة الملفات في متصفحك ولا يتم تخزينها على خوادمنا نهائياً."
    terms_title = "⚖️ شروط الاستخدام"
    terms_text = "هذه الأداة مجانية للاستخدام الشخصي والتجاري. يمنع استخدامها في أي محتوى يخالف القوانين."
else:
    st.markdown("""<style> .main {text-align: left; direction: ltr;} div.stButton > button {width: 100%;} </style>""", unsafe_allow_html=True)
    title = "📄 YouToPDF - PDF Merger"
    desc = "Fast and free tool to merge PDF files into one secure document."
    upload_msg = "Select PDF files to merge"
    btn_msg = "Merge Now"
    privacy_title = "🔒 Privacy & Security"
    privacy_text = "We value your privacy. Files are processed in your browser and are never stored on our servers."
    terms_title = "⚖️ Terms of Service"
    terms_text = "This tool is free for personal and commercial use. Illegal use is strictly prohibited."

# --- واجهة التطبيق الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{desc}</p>", unsafe_allow_html=True)
st.divider()

# منطقة الرفع والدمج
uploaded_files = st.file_uploader(upload_msg, type="pdf", accept_multiple_files=True)

if st.button(btn_msg):
    if uploaded_files and len(uploaded_files) >= 2:
        with st.spinner("Processing..." if language == "English" else "جاري المعالجة..."):
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            merger.close()
            st.success("Done!" if language == "English" else "تم الدمج!")
            st.download_button("Download PDF" if language == "English" else "تحميل الملف", 
                               output.getvalue(), "merged.pdf", "application/pdf")
    else:
        st.warning("Please upload at least 2 files" if language == "English" else "يرجى رفع ملفين على الأقل")

# --- قسم الشروط (Footer) بشكل أنيق أسفل الصفحة ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)

with col1:
    with st.expander(privacy_title):
        st.write(privacy_text)

with col2:
    with st.expander(terms_title):
        st.write(terms_text)

# إضافة حقوق الحقوق في الأسفل
st.markdown(f"<p style='text-align: center; color: gray; font-size: 0.8em;'>© 2024 YouToPDF - All Rights Reserved</p>", unsafe_allow_html=True)

import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄", layout="centered")

# 2. خيار اللغة في الشريط الجانبي
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS) لضمان المحاذاة الصحيحة وشكل الأزرار
if language == "العربية":
    st.markdown("""
        <style>
        .main { text-align: right; direction: rtl; }
        div.stButton > button { width: 100%; border-radius: 10px; background-color: #ff4b4b; color: white; }
        .footer-text { text-align: center; color: #888; font-size: 0.9em; margin-top: 50px; }
        </style>
    """, unsafe_allow_html=True)
    title = "📄 YouToPDF - دمج ملفات PDF"
    desc = "أداة مجانية وسريعة لدمج ملفات PDF في ملف واحد. آمنة 100%."
    upload_msg = "اسحب وأفلت ملفات PDF هنا"
    btn_msg = "ابدأ دمج الملفات"
    privacy_label = "🔒 سياسة الخصوصية"
    terms_label = "⚖️ شروط الاستخدام"
    privacy_content = "نحن لا نقوم بتخزين ملفاتك. تتم معالجة جميع عمليات الدمج محلياً في ذاكرة التخزين المؤقت وتُحذف فور إغلاق الصفحة."
    terms_content = "باستخدامك لهذا الموقع، فإنك تقر بأنك تملك الحقوق القانونية للملفات المرفوعة. الخدمة مقدمة 'كما هي' بدون ضمانات."
else:
    st.markdown("""
        <style>
        .main { text-align: left; direction: ltr; }
        div.stButton > button { width: 100%; border-radius: 10px; }
        .footer-text { text-align: center; color: #888; font-size: 0.9em; margin-top: 50px; }
        </style>
    """, unsafe_allow_html=True)
    title = "📄 YouToPDF - PDF Merger"
    desc = "Free and fast tool to merge PDF files into one. 100% Secure."
    upload_msg = "Drag and drop PDF files here"
    btn_msg = "Merge Files Now"
    privacy_label = "🔒 Privacy Policy"
    terms_label = "⚖️ Terms of Service"
    privacy_content = "We do not store your files. All processing is done in-memory and cleared instantly after use."
    terms_content = "By using this tool, you agree to our terms. Service is provided 'as is' without warranties."

# --- المحتوى الأساسي (يظهر دائماً في الصفحة الرئيسية) ---
st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{desc}</p>", unsafe_allow_html=True)
st.write("---")

# منطقة الرفع
uploaded_files = st.file_uploader(upload_msg, type="pdf", accept_multiple_files=True)

# زر الدمج
if st.button(btn_msg):
    if uploaded_files and len(uploaded_files) >= 2:
        with st.spinner("Processing..." if language == "English" else "جاري المعالجة..."):
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            merger.close()
            st.success("Success!" if language == "English" else "تم الدمج بنجاح!")
            st.download_button(
                label="Download Result" if language == "English" else "تحميل الملف المدمج",
                data=output.getvalue(),
                file_name="merged.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please upload 2+ files" if language == "English" else "يرجى رفع ملفين على الأقل للبدء")

# --- قسم شروط أدسنس (يظهر في أسفل الصفحة الرئيسية مباشرة) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.write("---")
st.markdown(f"<h3 style='text-align: center;'>Legal Information / معلومات قانونية</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    with st.expander(privacy_label):
        st.info(privacy_content)

with col2:
    with st.expander(terms_label):
        st.info(terms_content)

# تذييل الصفحة الثابت
st.markdown(f"<div class='footer-text'>© 2026 YouToPDF | Professional PDF Tools</div>", unsafe_allow_html=True)

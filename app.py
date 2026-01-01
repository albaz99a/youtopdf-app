import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄", layout="centered")

# 2. خيار اللغة - تم نقله إلى الصفحة الرئيسية بدلاً من الشريط الجانبي
# استخدام columns لوضع زر اللغة في جهة محددة أو في المنتصف
lang_col1, lang_col2 = st.columns([3, 1])
with lang_col2:
    language = st.selectbox("Language / اللغة", ["العربية", "English"])

# 3. إعدادات التصميم والتنسيق (CSS)
if language == "العربية":
    st.markdown("""
        <style>
        .main { text-align: right; direction: rtl; }
        div.stButton > button { width: 100%; border-radius: 8px; background-color: #ff4b4b; color: white; height: 3em; font-size: 1.2em; }
        .footer-note { text-align: center; color: #666; font-size: 0.8em; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px; }
        </style>
    """, unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - دمج ملفات PDF"
    t_desc = "أداة مجانية واحترافية لدمج ملفات PDF في ملف واحد بسرعة وأمان."
    t_upload = "قم برفع ملفات PDF هنا"
    t_btn = "دمج وتحميل الملف الآن"
    t_privacy_h = "🔒 سياسة الخصوصية والأمان"
    t_privacy_b = "خصوصيتك هي أولويتنا. جميع الملفات يتم معالجتها داخل ذاكرة النظام المؤقتة ولا يتم تخزينها نهائياً."
    t_terms_h = "⚖️ شروط الخدمة"
    t_terms_b = "يوافق المستخدم على استخدام الأداة للأغراض القانونية فقط. الخدمة مقدمة 'كما هي' بدون ضمانات."
    t_about_h = "💡 عن الأداة"
    t_about_b = "أداة YouToPDF مصممة لتكون أسرع وسيلة لدمج المستندات مع الحفاظ على خصوصية المستخدم الكاملة."
else:
    st.markdown("""
        <style>
        .main { text-align: left; direction: ltr; }
        div.stButton > button { width: 100%; border-radius: 8px; height: 3em; font-size: 1.2em; }
        .footer-note { text-align: center; color: #666; font-size: 0.8em; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px; }
        </style>
    """, unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - PDF Merger"
    t_desc = "A free, professional tool to merge PDF files quickly and securely."
    t_upload = "Upload your PDF files here"
    t_btn = "Merge & Download Now"
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Your privacy is our priority. Files are processed in-memory and are never stored on our servers."
    t_terms_h = "⚖️ Terms of Service"
    t_terms_b = "Users agree to use the tool for legal purposes only. Service is provided 'as is'."
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF is designed to be the fastest way to merge documents while maintaining total user privacy."

# --- [القسم الأول: أداة الدمج] ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("")

uploaded_files = st.file_uploader(t_upload, type="pdf", accept_multiple_files=True)

if st.button(t_btn):
    if uploaded_files and len(uploaded_files) >= 2:
        with st.spinner("Processing..." if language == "English" else "جاري المعالجة..."):
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            merger.close()
            st.success("Success!" if language == "English" else "تم الدمج!")
            st.download_button("Download PDF", output.getvalue(), "merged_document.pdf", "application/pdf")
    else:
        st.warning("Please upload 2+ files" if language == "English" else "يرجى رفع ملفين على الأقل")

st.write("---")

# --- [القسم الثاني: شروط أدسنس والمعلومات القانونية] ---
st.markdown(f"### {t_about_h}")
st.write(t_about_b)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {t_privacy_h}")
    st.info(t_privacy_b)
with col2:
    st.markdown(f"#### {t_terms_h}")
    st.info(t_terms_b)

st.markdown(f"<div class='footer-note'>© 2026 YouToPDF | All Rights Reserved</div>", unsafe_allow_html=True)

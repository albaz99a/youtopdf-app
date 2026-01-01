import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄", layout="centered")

# 2. خيار اللغة في الشريط الجانبي (فقط لتغيير النصوص)
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. إعدادات التصميم والتنسيق (CSS) لضمان ظهور كل شيء بشكل مرتب
if language == "العربية":
    st.markdown("""
        <style>
        .main { text-align: right; direction: rtl; }
        div.stButton > button { width: 100%; border-radius: 8px; background-color: #ff4b4b; color: white; height: 3em; font-size: 1.2em; }
        .footer-note { text-align: center; color: #666; font-size: 0.8em; margin-top: 50px; border-top: 1px solid #eee; padding-top: 20px; }
        h1, h3 { color: #31333F; }
        </style>
    """, unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - دمج ملفات PDF"
    t_desc = "أداة مجانية واحترافية لدمج ملفات PDF في ملف واحد بسرعة وأمان."
    t_upload = "قم برفع ملفات PDF هنا (ملفين أو أكثر)"
    t_btn = "دمج وتحميل الملف الآن"
    t_privacy_h = "🔒 سياسة الخصوصية والأمان"
    t_privacy_b = "خصوصيتك هي أولويتنا. جميع الملفات التي ترفعها يتم معالجتها داخل ذاكرة النظام المؤقتة ولا يتم تخزينها أو الاطلاع عليها من قبل أي طرف ثالث، وتُحذف تلقائياً بمجرد إغلاق المتصفح."
    t_terms_h = "⚖️ شروط الخدمة"
    t_terms_b = "يوفر YouToPDF هذه الخدمة مجاناً 'كما هي'. يوافق المستخدم على عدم استخدام الأداة في معالجة ملفات تنتهك حقوق الملكية أو القوانين العامة. نحن غير مسؤولين عن أي سوء استخدام ناتج عن الأداة."
    t_about_h = "💡 عن الأداة"
    t_about_b = "تم تطوير YouToPDF لتسهيل إدارة المستندات الرقمية للمستخدمين حول العالم، مع التركيز على السرعة والبساطة."
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
    t_upload = "Upload your PDF files (2 or more)"
    t_btn = "Merge & Download Now"
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Your privacy is our priority. All uploaded files are processed in-memory and are never stored on our servers. Files are permanently deleted after the session ends."
    t_terms_h = "⚖️ Terms of Service"
    t_terms_b = "YouToPDF provides this service for free 'as is'. Users agree not to use this tool for any illegal content. We are not liable for any misuse of the provided service."
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF was built to simplify digital document management for users worldwide, focusing on speed and simplicity."

# --- [القسم الأول: أداة الدمج الرئيسية] ---
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
            st.success("Success!" if language == "English" else "تم الدمج بنجاح!")
            st.download_button("Download PDF", output.getvalue(), "merged_document.pdf", "application/pdf")
    else:
        st.warning("Please upload at least 2 files" if language == "English" else "يرجى رفع ملفين على الأقل للبدء")

st.write("---") # خط فاصل

# --- [القسم الثاني: شروط أدسنس والمعلومات القانونية] ---
# تظهر هذه الأقسام مباشرة أسفل الأداة في الصفحة الرئيسية
st.markdown(f"### {t_about_h}")
st.write(t_about_b)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### {t_privacy_h}")
    st.info(t_privacy_b)

with col2:
    st.markdown(f"#### {t_terms_h}")
    st.info(t_terms_b)

# --- [القسم الثالث: تذييل الصفحة] ---
st.markdown(f"<div class='footer-note'>© 2026 YouToPDF | All Rights Reserved | Your Trusted PDF Tool</div>", unsafe_allow_html=True)

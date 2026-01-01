import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="centered")

# 2. اختيار اللغة (أعلى الصفحة)
lang_col1, lang_col2 = st.columns([4, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS) والنصوص
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px; font-weight: bold;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF"
    t_desc = "أدوات احترافية، سريعة، وآمنة تماماً لمعالجة ملفاتك."
    t_service_label = "اختر الخدمة المطلوبة:"
    # قائمة الخدمات الـ 5
    options = ["دمج ملفات PDF", "تحويل صور إلى PDF", "تقسيم ملف PDF", "حماية بكلمة سر", "ضغط ملف PDF"]
    t_btn = "تنفيذ العملية الآن"
    t_about_h = "💡 عن الموقع"
    t_about_b = "YouToPDF منصة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات."
    t_privacy_h = "🔒 الخصوصية والأمان"
    t_privacy_b = "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً. نحن لا نحتفظ بأي بيانات نهائياً."
    t_terms_h = "⚖️ شروط الاستخدام"
    t_terms_b = "باستخدامك للموقع، توافق على معالجة ملفاتك قانونياً."
    t_contact_h = "📧 اتصل بنا"
    t_contact_b = "لديك استفسار؟ تواصل معنا عبر: support@youtopdf.com"
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%; border-radius: 8px; font-weight: bold;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - All-in-One PDF Tools"
    t_desc = "Professional, fast, and 100% secure tools for your documents."
    t_service_label = "Choose a Service:"
    options = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_btn = "Process Now"
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF provides essential tools for document management with total privacy."
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Files are processed in-memory and deleted instantly."
    t_terms_h = "⚖️ Terms of Use"
    t_terms_b = "By using this tool, you agree to lawful use."
    t_contact_h = "📧 Contact Us"
    t_contact_b = "Questions? Reach out to us at: support@youtopdf.com"

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# استخدام القائمة المنسدلة لإظهار الخدمات الـ 5
service = st.selectbox(t_service_label, options)

output = BytesIO()
is_ready = False

# 4. تنفيذ العمليات
if service in ["دمج ملفات PDF", "Merge PDF"]:
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(t_btn) and files:
        merger = PdfMerger()

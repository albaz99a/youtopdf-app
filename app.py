import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="centered")

# 2. اختيار اللغة في أعلى الصفحة
lang_col1, lang_col2 = st.columns([4, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS)
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF"
    t_desc = "أدوات احترافية، سريعة، وآمنة تماماً لمعالجة ملفاتك."
    t_service_label = "اختر الخدمة المطلوبة:"
    t_merge_option = "دمج ملفات PDF"
    t_img_option = "تحويل صور إلى PDF"
    t_btn_merge = "ابدأ دمج الملفات"
    t_btn_img = "ابدأ تحويل الصور"
    t_about_h = "💡 عن الموقع"
    t_about_b = "YouToPDF منصة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات، مما يضمن لك الخصوصية والسرعة."
    t_privacy_h = "🔒 الخصوصية والأمان"
    t_privacy_b = "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً. نحن لا نحتفظ بأي بيانات نهائياً لضمان خصوصيتك الكاملة."
    t_terms_h = "⚖️ شروط الاستخدام"
    t_terms_b = "باستخدامك للموقع، توافق على معالجة ملفاتك قانونياً. الخدمة مقدمة مجاناً 'كما هي' وبدون ضمانات."
    t_contact_h = "📧 اتصل بنا"
    t_contact_b = "لديك استفسار أو اقتراح؟ يسعدنا تواصلك معنا عبر البريد الإلكتروني التالي:"
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%; border-radius: 8px;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - PDF Toolset"
    t_desc = "Professional, fast, and 100% secure tools for your documents."
    t_service_label = "Choose a Service:"
    t_merge_option = "Merge PDF Files"
    t_img_option = "Images to PDF"
    t_btn_merge = "Merge Files Now"
    t_btn_img = "Convert Images Now"
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF provides essential tools for document management with total privacy and high efficiency."
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Files are processed in-memory and deleted instantly. No data is ever stored on our servers."
    t_terms_h = "⚖️ Terms of Use"
    t_terms_b = "By using this tool, you agree to lawful use. Service is provided 'as is' without warranties."
    t_contact_h = "📧 Contact Us"
    t_contact_b = "Have a question or suggestion

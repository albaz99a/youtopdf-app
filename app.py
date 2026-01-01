import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الموقع الأساسية
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS صارم لإلغاء أي عناصر منبثقة أو جانبية
st.markdown("""
<style>
    /* إخفاء القائمة الجانبية نهائياً */
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    
    /* إخفاء الهيدر والمنيو الافتراضي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* تنسيق صور الخدمات */
    .service-icon { width: 90px; height: 90px; margin-bottom: 5px; }
    
    /* تنسيق الفوتر (أدنسنس) */
    .footer-container {
        background-color: #f1f3f6;
        padding: 30px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
    }
    
    /* تنسيق أزرار اللغة والخدمات لمنع البروز المنبثق */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; transition: 0.2s; }
</style>
""", unsafe_allow_html=True)

# 3. إدارة اللغة (بدون أي قائمة منسدلة أو جانبية)
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

# الهيدر: العنوان واللغة في أقصى اليمين
h_col1, h_col2, h_col3 = st.columns([6, 3, 3])

with h_col1:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -10px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with h_col2:
    if st.button("العربية"):
        st.session_state.lang = "العربية"
with h_col3:
    if st.button("English"):
        st.session_state.lang = "English"

st.write("---")

# 4. تعريف النصوص بناءً على الاختيار
lang = st.session_state.lang
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة مجانية بالكامل لأدوات PDF الاحترافية."
    t_priv = "🔒 الخصوصية: معالجة فورية للملفات دون أي تخزين."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
    btn_run = "بدء التنفيذ"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: A free platform for professional PDF tools."
    t_priv = "🔒 Privacy: Instant file processing with zero storage."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    btn_run = "Run Process"

# 5. الأيقونات الخمس (صور احترافية واضحة جداً)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "

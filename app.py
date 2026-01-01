import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS المتقدم (مطابق للصورة تماماً)
st.markdown("""
<style>
    /* إخفاء القوائم الافتراضية لمنع ظهور أي صفحات منبثقة */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}

    /* تنسيق الحاوية العلوية */
    .main-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; }
    
    /* تنسيق الأيقونات الاحترافية */
    .icon-container { text-align: center; padding: 10px; }
    .service-icon { width: 90px; height: 90px; margin-bottom: 10px; filter: grayscale(20%); }
    
    /* تكبير وتنسيق أسماء الخدمات بوضوح عالي */
    .stButton>button { 
        width: 100%; 
        height: 80px !important; 
        font-size: 22px !important; 
        font-weight: 900 !important; 
        border-radius: 15px !important;
        border: 2px solid #f1f3f6 !important;
        background-color: #ffffff !important;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        border-color: #ff4b4b !important; 
        color: #ff4b4b !important;
        transform: translateY(-3px);
    }
    
    /* تمييز كلمة PDF باللون الأحمر */
    .pdf-brand { color: #ff4b4b; font-weight: bold; }

    /* الفوتر المؤطر باللون الأحمر (متطلبات أدسنس) */
    .adsense-footer-container {
        background-color: #fafafa;
        padding: 40px;
        border: 2px solid #ff4b4b;
        border-radius: 20px;
        text-align: center;
        margin-top: 60px;
    }
</style>
""", unsafe_allow_html=True)

# 3. الجزء العلوي (الشعار واللغة)
col_logo, col_lang = st.columns([8, 2])
with col_logo:
    st.markdown("<h1 style='color: #ff4b4b; margin: 0;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
with col_lang:
    lang = st.radio("", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

st.markdown("<hr style='margin-top: 5px; border: 0.5px solid #eee;'>", unsafe_allow_html=True)

# 4. تعريف النصوص بناءً على اللغة المختار
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة ملفات مجانية وآمنة."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك؛ المعالجة فورية وتتم في الذاكرة فقط."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
    btn_txt = "بدء التنفيذ"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform for free and secure PDF tools."
    t_priv = "🔒 Privacy: No files are stored; processing is instant and in-memory."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    btn_txt = "Run Now"

# 5. الأيقونات الاحترافية (تم اختيارها لتدل على PDF)
icons = [
    "https://cdn-icons-png.flaticon.com/512/9464/9464136.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

# عرض شبكة الخدمات كما في صورتك
cols = st.columns(5)
if 'active' not in st.session_state: st.session_state.active = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icons

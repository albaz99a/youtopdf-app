import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="YouToPDF - أدوات PDF احترافية", page_icon="📄", layout="wide")

# 2. تصميم الواجهة (CSS) لتنسيق اللغة والأيقونات والفوتر
st.markdown("""
<style>
    /* إخفاء العناصر الافتراضية المزعجة */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تنسيق أيقونات الخدمات لتبدو احترافية */
    .service-icon { width: 100px; height: 100px; margin-bottom: 10px; transition: 0.3s; }
    .service-icon:hover { transform: translateY(-5px); }
    
    /* تنسيق الفوتر (متطلبات Google AdSense) */
    .footer-section {
        background-color: #f1f3f6;
        padding: 40px;
        border-top: 5px solid #ff4b4b;
        margin-top: 60px;
        border-radius: 20px;
        text-align: center;
        color: #333;
    }
    
    /* تحسين شكل أزرار الخدمات واللغة */
    .stButton>button { width: 100%; border-radius: 12px; font-weight: bold; height: 45px; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر: اختيار اللغة في أعلى اليمين
h_col1, h_col2, h_col3 = st.columns([7, 2, 3])

with h_col1:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -15px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with h_col3:
    # اختيار اللغة يظهر في أعلى اليمين بشكل مباشر
    lang = st.radio("اللغة / Language", ["العربية", "English"], horizontal=True)

st.write("---")

# 4. تعريف النصوص بناءً على اللغة المختار
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة PDF مجانية وآمنة للجميع."
    t_priv = "🔒 سياسة الخصوصية: نحن نحترم خصوصيتك؛ لا يتم تخزين ملفاتك، المعالجة فورية."
    t_terms = "⚖️ شروط الاستخدام: الخدمة مقدمة للاستخدام العادل والقانوني فقط."
    t_contact = "📧 للتواصل والدعم: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform providing free and secure PDF tools."
    t_priv = "🔒 Privacy Policy: We respect your privacy; files are processed instantly and never stored."
    t_terms = "⚖️ Terms: Service provided for fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"

# 5. أيقونات الخدمات (صور احترافية محدثة)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

cols = st.columns(5)

# إدارة اختيار الأداة عبر session_state لمنع الصفحات المنبثقة
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"tool_btn_{i}"):
            st.session_state.current_tool = labels[i]

st.divider()

# 6. منطقة العمل الديناميكية
active = st.session_state.current_tool
st.subheader(f"🛠️ {active}")

res_buffer = BytesIO()
is_ready = False

# منطق عمل الأدوات المبرمج بدقة
if active in [labels

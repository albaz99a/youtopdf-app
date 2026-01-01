import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF الشاملة", page_icon="📄", layout="wide")

# 2. اختيار اللغة
lang_col1, lang_col2 = st.columns([6, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS) - أيقونات كبيرة وثبات الفوتر
if language == "العربية":
    st.markdown("""
        <style>
        .main {text-align: right; direction: rtl;}
        .service-box { text-align: center; padding: 15px; border: 2px solid #ff4b4b; border-radius: 15px; background-color: #fff5f5; margin-bottom: 10px;}
        .icon-size { font-size: 60px; }
        .stButton > button {width: 100%; border-radius: 10px; font-weight: bold;}
        </style>
    """, unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF"
    t_desc = "جميع الأدوات تظهر أدناه، اختر ما تحتاجه:"
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about_h, t_about_b = "💡 عن الموقع", "منصة YouToPDF توفر أدوات مجانية تماماً لمعالجة ملفاتك بسرعة وسهولة."
    t_privacy_h, t_privacy_b = "🔒 الخصوصية والأمان", "ملفاتك آمنة؛ نقوم بمعالجتها في الذاكرة المؤقتة ونحذفها فوراً بعد التحميل."
    t_terms_h, t_terms_b = "⚖️ شروط الاستخدام", "باستخدامك للموقع، أنت توافق على سياسة الاستخدام العادل والمعالجة القانونية للملفات."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    st.markdown("""
        <style>
        .main {text-align: left; direction: ltr;}
        .service-box { text-align: center; padding: 15px; border: 2px solid #007bff; border-radius: 15px; background-color: #f0f7ff; margin-bottom: 10px;}
        .icon-size { font-size: 60px; }
        .stButton > button {width: 100%; border-radius: 10px; font-weight: bold;}
        </style>
    """, unsafe_allow_html=True)
    t_title = "📄 YouToPDF - Professional PDF Tools"
    t_desc = "All tools are available below, select one to start:"
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about_h, t_about_b = "💡 About Us", "YouToPDF offers free, high-quality tools for document management."
    t_privacy_h, t_privacy_b = "🔒 Privacy & Security", "Your privacy is our priority. Files are processed in-memory and deleted instantly."
    t_terms_h, t_terms_b = "⚖️ Terms of Use", "By using this site, you agree to our terms of service and lawful file processing."
    t_contact = "📧 Contact Us: support@youtopdf.com"

st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# 4. عرض الخدمات الـ 5 بأيقونات كبيرة في صف واحد
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
output = BytesIO()
ready = False

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='service-box'><div class='icon-size'>{icons[i]}</div><b>{labels[i]}</b></div>", unsafe_allow_html=True)
        if st.button(f"فتح / Open", key=f"btn_{i}"):
            st.session_state.active_tool = i

# تحديد الأداة النشطة (الافتراضي دمج)
active = st.session_state.get("active_tool", 0)
st.markdown(f"### 🛠️ {labels[active]}")

# 5. منطق العمل للأدوات
if active == 0: # دمج
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="u0")
    if st.button("Start Process") and f:
        merger = PdfMerger()
        for x in f: merger.append(x)
        merger.write(output); ready = True
elif active == 1: # صور
    f = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="u1")
    if st.button("Start Process") and f:
        imgs = [Image.open(x).convert("RGB") for x in

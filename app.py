import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS ثابت وقوي لضمان ظهور الفوتر والأيقونات
st.markdown("""
<style>
    .big-icon-display { font-size: 70px !important; text-align: center; margin-bottom: 0px; }
    .footer-container {
        background-color: #f8f9fa;
        padding: 30px;
        border-top: 4px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
        width: 100%;
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 45px; }
</style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    about_text = "💡 عن الموقع: منصة مجانية بالكامل لمعالجة ملفات PDF."
    privacy_text = "🔒 الخصوصية: ملفاتك تُعالج في الذاكرة ولا يتم تخزينها نهائياً."
    terms_text = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    contact_text = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    about_text = "💡 About Us: A 100% free platform for PDF tools."
    privacy_text = "🔒 Privacy: Files are processed in-memory and never stored."
    terms_text = "⚖️ Terms: Fair and lawful use only."
    contact_text = "📧 Contact Us: support@youtopdf.com"

st.title("📄 YouToPDF")
st.write("---")

# 4. عرض الأيقونات الخمس كأزرار تحكم
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

if 'current_tool' not in st.session_state:
    st.session_state.current_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon-display'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.current_tool = labels[i]

st.write("---")

# 5. منطقة العمل
tool = st.session_state.current_tool
st.subheader(f"🛠️ {tool}")

output = BytesIO()
ready = False

if tool in [labels[0]]: # دمج
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="up1")
    if st.button("تنفيذ الآن", key="run1") and f:
        m = PdfMerger(); [m.append(x) for x in f]; m.write(output); ready = True

elif tool in [labels[1]]: # صور
    f = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="up2")
    if st.button("تنفيذ الآن", key="run2") and f:
        imgs = [Image.open(x).convert("RGB") for x in f]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif tool in [labels[2]]: # تقسيم
    f = st.file_uploader("Upload PDF", type="pdf", key="up3")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تنفيذ الآن", key="run3") and f:
        r, w = PdfReader(f), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); ready = True

elif tool in [labels[3]]: # حماية
    f = st.file_uploader("Upload PDF", type="pdf", key="up4")
    pw

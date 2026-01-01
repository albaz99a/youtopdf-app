import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة - العرض الواسع ضروري لظهور الأيقونات بجانب بعضها
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="wide")

# 2. اختيار اللغة
lang_col1, lang_col2 = st.columns([6, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. تصميم CSS مكثف لضمان ظهور الأيقونات بشكل ضخم وثبات الفوتر
st.markdown("""
    <style>
    .main {text-align: center;}
    .stButton > button {
        width: 100%; 
        height: 100px; 
        font-size: 24px !important; 
        border-radius: 15px; 
        border: 2px solid #ff4b4b;
        background-color: #ffffff;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #ff4b4b;
        color: white;
    }
    .big-icon { font-size: 80px; margin-bottom: -10px; }
    .footer-box { 
        padding: 20px; 
        background-color: #f1f3f6; 
        border-radius: 10px; 
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# نصوص الواجهة
if language == "العربية":
    t_title = "📄 منصة YouToPDF الشاملة"
    t_desc = "جميع أدوات PDF في مكان واحد - اختر أداة للبدء"
    labels = ["دمج", "صور", "تقسيم", "حماية", "ضغط"]
    t_about = "💡 عن الموقع: منصة مجانية بالكامل تهدف لمعالجة ملفات PDF بأمان عالٍ دون تخزين بيانات."
    t_privacy = "🔒 الخصوصية: ملفاتك تُعالج في الذاكرة وتُحذف فوراً."
    t_terms = "⚖️ الشروط: باستخدامك للموقع توافق على سياسة الاستخدام العادل."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    t_title = "📄 YouToPDF All-in-One"
    t_desc = "All PDF tools in one place - Select a tool to start"
    labels = ["Merge", "Images", "Split", "Protect", "Compress"]
    t_about = "💡 About: A free platform to process PDF files securely without storing data."
    t_privacy = "🔒 Privacy: Files are processed in-memory and deleted instantly."
    t_terms = "⚖️ Terms: By using this site, you agree to our fair use policy."
    t_contact = "📧 Contact Us: support@youtopdf.com"

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# 4. عرض الـ 5 خدمات كأيقونات كبيرة جداً
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
output = BytesIO()
ready = False

# جعل الاختيار يعتمد على الضغط المباشر
if 'tool' not in st.session_state:
    st.session_state.tool = 0

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><div class='big-icon'>{icons[i]}</div><p style='font-weight:bold;'>{labels[i]}</p></div>", unsafe_allow_html=True)
        if st.button(f"GO", key=f"btn_{i}"):
            st.session_state.tool = i

st.write("---")

# 5. منطقة العمل (تتغير حسب الزر المظغوط)
active = st.session_state.tool
st.markdown(f"<h2 style='text-align: center;'>{icons[active]} {labels[active]}</h2>", unsafe_allow_html=True)

if active == 0: # دمج
    f = st.file_uploader("PDFs", type="pdf", accept_multiple_files=True, key="m")
    if st.button("Process") and f:
        merger = PdfMerger()
        for x in f: merger.append(x)
        merger.write(output); ready = True
elif active == 1: # صور
    f = st.file_uploader("Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="i")
    if st.button("Process") and f:
        imgs = [Image.open(x).convert("RGB") for x in f]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready = True
elif active == 2: # تقسيم
    f = st.file_uploader("PDF", type="pdf", key="s")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("Process") and f:
        reader, writer = PdfReader(f), PdfWriter()
        start, end = map(int, p.split("-"))
        for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
        writer.write(output); ready = True
elif active == 3: # حماية
    f = st.file_uploader("PDF", type="pdf", key="p")
    pwd = st.text_input("Password", type="password")
    if st.button("Process") and f and pwd:
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages: writer.add_page(page)
        writer.encrypt(pwd); writer.write(output); ready = True
elif active == 4: # ضغط
    f = st.file_uploader("PDF", type="pdf", key="c")
    if st.button("Process") and f:
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages: page.compress_content_streams(); writer.add_page(page)
        writer.write(output); ready = True

if ready:
    st.success("Done!")
    st.download_button("📥 Download Result", output.getvalue(), "YouToPDF_Result.pdf")

# 6. شروط أدسنس - ثابتة تماماً في أسفل الصفحة
st.markdown("<div class='footer-box'>", unsafe_allow_html=True)
st.markdown(f"### {t_about}")
col_1, col_2 = st.columns(2)
with col_1:
    st.info(t_privacy)
with col_2:
    st.info(t_terms)
st.markdown(f"<p style='text-align: center; font-weight: bold; margin-top:20px;'>{t_contact}</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>© 2026 YouToPDF - Secure PDF Tools</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

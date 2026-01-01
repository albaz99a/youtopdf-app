import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS (جعل الأيقونات ضخمة جداً وثبات شروط أدسنس)
st.markdown("""
    <style>
    .big-icon { font-size: 100px !important; text-align: center; display: block; margin: 10px auto; }
    .service-label { font-size: 24px !important; font-weight: bold; text-align: center; color: #333; }
    .footer-section { background-color: #f9f9f9; padding: 30px; border-top: 3px solid #ff4b4b; margin-top: 50px; border-radius: 10px; }
    .stButton > button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة في الأعلى
lang = st.radio("Language/اللغة", ["العربية", "English"], horizontal=True)

# نصوص الواجهة بناءً على اللغة
if lang == "العربية":
    t_title = "📄 منصة YouToPDF الشاملة"
    t_about = "💡 عن الموقع: منصة مجانية بالكامل لمعالجة ملفات PDF بأمان عالٍ دون تخزين بيانات."
    t_privacy = "🔒 الخصوصية والأمان: ملفاتك تُعالج في الذاكرة وتُحذف فوراً بعد التحميل."
    t_terms = "⚖️ شروط الاستخدام: باستخدامك للموقع توافق على سياسة الاستخدام العادل."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
    services = ["دمج", "صور", "تقسيم", "حماية", "ضغط"]
else:
    t_title = "📄 YouToPDF Complete Platform"
    t_about = "💡 About Us: A free platform to process PDF files securely without storing any data."
    t_privacy = "🔒 Privacy & Security: Files are processed in-memory and deleted instantly."
    t_terms = "⚖️ Terms of Use: By using this site, you agree to our fair use policy."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    services = ["Merge", "Images", "Split", "Protect", "Compress"]

st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.write("---")

# 4. عرض الخدمات الـ 5 بوضوح تام (أيقونات ضخمة)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

# استخدام اختيار بسيط لضمان عدم حدوث أخطاء
active_service = st.radio("اختر الخدمة / Select Service", services, horizontal=True)

st.write("---")

# 5. منطقة العمل (تتغير حسب الاختيار)
output = BytesIO()
ready = False

if active_service in ["دمج", "Merge"]:
    st.markdown("<div class='big-icon'>🔗</div>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Start Merge") and f:
        m = PdfMerger()
        for x in f: m.append(x)
        m.write(output); ready = True

elif active_service in ["صور", "Images"]:
    st.markdown("<div class='big-icon'>🖼️</div>", unsafe_allow_html=True)
    f = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Convert to PDF") and f:
        imgs = [Image.open(x).convert("RGB") for x in f]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif active_service in ["تقسيم", "Split"]:
    st.markdown("<div class='big-icon'>✂️</div>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Pages (e.g. 1-3)", "1-2")
    if st.button("Split PDF") and f:
        r, w = PdfReader(f), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); ready = True

elif active_service in ["حماية", "Protect"]:
    st.markdown("<div class='big-icon'>🔒</div>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDF", type="pdf")
    pwd = st.text_input("Password", type="password")
    if st.button("Encrypt PDF") and f and pwd:
        r, w = PdfReader(f), PdfWriter()
        for p in r.pages: w.add_page(p)
        w.encrypt(pwd); w.write(output); ready = True

elif active_service in ["ضغط", "Compress"]:
    st.markdown("<div class='big-icon'>📉</div>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Compress Now") and f:
        r, w = PdfReader(f), PdfWriter()
        for p in r.pages: p.compress_content_streams(); w.add_page(p)
        w.write(output); ready = True

if ready:
    st.success("Done!")
    st.download_button("📥 Download Result", output.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم أدسنس والفوتر (ثابت لا يتغير أبداً)
st.markdown(f"""
    <div class='footer-section'>
        <h3 style='text-align: center;'>{t_about}</h3>
        <hr>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='flex: 1; min-width: 300px; padding: 10px;'>{t_privacy}</div>
            <div style='flex: 1; min-width: 300px; padding: 10px;'>{t_terms}</div>
        </div>
        <p style='text-align: center; font-weight: bold; margin-top: 20px;'>{t_contact}</p>
        <p style='text

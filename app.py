import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS (أيقونات ضخمة + إجبار ظهور الفوتر)
st.markdown("""
    <style>
    .big-icon { font-size: 100px !important; text-align: center; margin-bottom: 10px; }
    .service-box { 
        text-align: center; 
        padding: 20px; 
        border: 2px solid #ff4b4b; 
        border-radius: 20px; 
        background-color: #fffafa;
    }
    .footer-container {
        background-color: #f1f3f6 !important;
        padding: 50px !important;
        border-top: 10px solid #ff4b4b !important;
        margin-top: 50px !important;
        display: block !important;
        visibility: visible !important;
        border-radius: 20px;
    }
    .stButton > button { width: 100%; height: 60px; font-size: 20px; font-weight: bold; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
language = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if language == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 عن الموقع: منصة YouToPDF هي أداة مجانية واحترافية لمعالجة ملفات PDF."
    t_privacy = "🔒 الخصوصية: ملفاتك آمنة تماماً، تعالج في الذاكرة وتُحذف فوراً."
    t_terms = "⚖️ الشروط: الخدمة مقدمة للاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: YouToPDF is a free professional tool for PDF management."
    t_privacy = "🔒 Privacy: Your files are 100% secure, processed in-memory and deleted instantly."
    t_terms = "⚖️ Terms: Service is provided for fair and lawful use only."
    t_contact = "📧 Contact: support@youtopdf.com"

# --- العرض الرئيسي ---
st.markdown(f"<h1 style='text-align: center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
st.write("---")

# 4. عرض الخدمات الـ 5 (أيقونات ضخمة)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-weight:bold;'>{labels[i]}</p>", unsafe_allow_html=True)

# اختيار الخدمة
active_tool = st.selectbox("إختر الأداة / Select Tool", labels)
st.write("---")

# 5. منطق العمل
output = BytesIO()
is_ready = False

if active_tool in ["دمج PDF", "Merge PDF"]:
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="f1")
    if st.button("Start / ابدأ") and f:
        m = PdfMerger()
        for x in f: m.append(x)
        m.write(output); is_ready = True
elif active_tool in ["صور إلى PDF", "Images to PDF"]:
    f = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="f2")
    if st.button("Start / ابدأ") and f:
        imgs = [Image.open(x).convert("RGB") for x in f]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); is_ready = True
elif active_tool in ["تقسيم PDF", "Split PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf", key="f3")
    p = st.text_input("Pages (1-2)", "1-2")
    if st.button("Start / ابدأ") and f:
        r, w = PdfReader(f), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); is_ready = True
elif active_tool in ["حماية PDF", "Protect PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf", key="f4")
    pwd = st.text_input("Password", type="password")
    if st.button("Start / ابدأ") and f and pwd:
        r, w = PdfReader(f), PdfWriter()
        for x in r.pages: w.add_page(x)
        w.encrypt(pwd); w.write(output); is_ready = True
elif active_tool in ["ضغط PDF", "Compress PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf", key="f5")
    if st.button("Start / ابدأ") and f:
        r, w = PdfReader(f), PdfWriter()
        for x in r.pages: x.compress_content_streams(); w.add_page(x)
        w.write(output); is_ready = True

if is_ready:
    st.success("Success!")
    st.download_button("Download", output.getvalue(), "YouToPDF_Result.pdf")

# 6. شروط أدسنس (إجبار الظهور بـ HTML ثابت)
st.markdown(f"""
    <div class="footer-container">
        <h2 style="text-align: center; color: #ff4b4b;">Google AdSense Requirements / شروط الموقع</h2>
        <p style="text-align: center;

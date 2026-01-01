import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS للأيقونات والفوتر (معدل لضمان الاستقرار)
st.markdown("""
<style>
    /* تصميم الأيقونات لتكون تفاعلية وضخمة */
    .icon-container {
        text-align: center;
        transition: 0.3s;
        padding: 10px;
    }
    .big-icon-label {
        font-size: 70px !important;
        display: block;
        margin-bottom: 5px;
    }
    /* فوتر أدسنس الثابت */
    .adsense-footer {
        background-color: #f8f9fa;
        padding: 40px;
        border-top: 5px solid #ff4b4b;
        margin-top: 80px;
        border-radius: 20px;
        text-align: center;
    }
    /* إخفاء القوائم الجانبية المزعجة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 عن الموقع: منصة مجانية بالكامل لمعالجة ملفات PDF بأمان."
    t_privacy = "🔒 الخصوصية: ملفاتك تُعالج في الذاكرة ولا يتم تخزينها نهائياً."
    t_terms = "⚖️ الشروط: باستخدامك للموقع توافق على سياسة الاستخدام القانوني."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: A 100% free and secure platform for PDF tools."
    t_privacy = "🔒 Privacy: Your files are processed in-memory and never stored."
    t_terms = "⚖️ Terms: By using this site, you agree to our legal use policy."
    t_contact = "📧 Contact: support@youtopdf.com"

st.title("📄 YouToPDF")
st.write("---")

# 4. تفعيل الأيقونات الخمس كأزرار مباشرة
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

# استخدام session_state لتحديد الأداة المفعلة
if 'tool' not in st.session_state:
    st.session_state.tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='icon-container'><span class='big-icon-label'>{icons[i]}</span></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.tool = labels[i]

st.write("---")

# 5. منطقة العمل الديناميكية (تظهر تحت الأيقونة المختارة مباشرة)
current_tool = st.session_state.tool
st.subheader(f"🛠️ {current_tool}")

output = BytesIO()
ready = False

if current_tool in ["دمج PDF", "Merge PDF"]:
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="u1")
    if st.button("Start / تنفيذ") and up:
        m = PdfMerger()
        for f in up: m.append(f)
        m.write(output); ready = True

elif current_tool in ["صور إلى PDF", "Images to PDF"]:
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="u2")
    if st.button("Start / تنفيذ") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif current_tool in ["تقسيم PDF", "Split PDF"]:
    up = st.file_uploader("Upload PDF", type="pdf", key="u3")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("Start / تنفيذ") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); ready = True

elif current_tool in ["حماية PDF", "Protect PDF"]:
    up = st.file_uploader("Upload PDF", type="pdf", key="u4")
    pw = st.text_input("Password", type="password")
    if st.button("Start / تنفيذ") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pge in r.pages: w.add_page(pge)
        w.encrypt(pw); w.write(output); ready = True

elif current_tool in ["ضغط PDF", "Compress PDF"]:
    up = st.file_uploader("Upload PDF", type="pdf", key="u5")
    if st.button("Start / تنفيذ") and up:
        r, w = PdfReader(up), PdfWriter

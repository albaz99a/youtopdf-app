import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Professional PDF Tools", page_icon="📄", layout="wide")

# 2. تصميم CSS محسن (إلغاء المنبثقات وتجميل الأيقونات)
st.markdown("""
<style>
    .icon-img { width: 80px; height: 80px; margin-bottom: 10px; transition: transform 0.3s; }
    .icon-img:hover { transform: scale(1.1); }
    .footer-box {
        background-color: #f8f9fa;
        padding: 30px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 45px; }
</style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة (مباشرة في أعلى الصفحة بدون قوائم منبثقة)
lang_col1, lang_col2 = st.columns([8, 2])
with lang_col2:
    lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

# نصوص اللغات
if lang == "العربية":
    services = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 عن الموقع: منصة احترافية مجانية بالكامل لمعالجة ملفات PDF."
    t_priv = "🔒 الخصوصية: ملفاتك تُعالج فورياً في الذاكرة ولا يتم تخزينها أبداً."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    services = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About: Professional platform for free PDF tools."
    t_priv = "🔒 Privacy: Files are processed instantly and never stored."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"

st.markdown("<h1 style='text-align:center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
st.write("---")

# 4. الأيقونات الخمس (صور واضحة بدلاً من الرموز)
# روابط صور أيقونات احترافية
icon_urls = [
    "https://cdn-icons-png.flaticon.com/128/2991/2991132.png", # Merge
    "https://cdn-icons-png.flaticon.com/128/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/128/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/128/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/128/2991/2991124.png"  # Compress
]

cols = st.columns(5)

if 'tool' not in st.session_state:
    st.session_state.tool = services[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='icon-img'></div>", unsafe_allow_html=True)
        if st.button(services[i], key=f"btn_{i}"):
            st.session_state.tool = services[i]

st.write("---")

# 5. منطقة تنفيذ العمليات
active_tool = st.session_state.tool
st.subheader(f"🛠️ {active_tool}")

output = BytesIO()
done = False

if active_tool == services[0]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("بدأ العمل") and up:
        m = PdfMerger()
        for f in up: m.append(f)
        m.write(output); done = True

elif active_tool == services[1]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("بدأ العمل") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); done = True

elif active_tool == services[2]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (e.g. 1-2)", "1-2")
    if st.button("بدأ العمل") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); done = True

elif active_tool == services[3]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button("بدأ العمل") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(output); done = True

elif active_tool == services[4]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button("بدأ العمل") and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(output); done = True

if done:
    st.success("تم التجهيز بنجاح!")
    st.download_button("📥 تحميل الملف الآن", output.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم الفوتر القانوني (شروط أدسنس)
st.write("---")
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
st.write(f"**{t_about}**")
st.write(f"{t_priv} | {t_terms}")
st.write(f"**{t_contact}**")
st.markdown('<p style="color:gray; font-size:12px; margin-top:10px;">© 2026 YouToPDF - Fast & Secure Services</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

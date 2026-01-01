import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS مبسط جداً لضمان عدم حدوث خطأ Syntax
st.markdown("""
<style>
    .icon-container { font-size: 60px; text-align: center; }
    .footer-box {
        background-color: #f1f3f6;
        padding: 20px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 10px;
        text-align: center;
    }
    #MainMenu, footer, header {visibility: hidden;}
    .stButton>button { width: 100%; font-weight: bold; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    services = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    txt_about = "💡 عن الموقع: منصة مجانية بالكامل لأدوات PDF."
    txt_priv = "🔒 الخصوصية: ملفاتك تُعالج فورياً ولا يتم تخزينها."
    txt_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    txt_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    services = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    txt_about = "💡 About: Free and secure PDF tools platform."
    txt_priv = "🔒 Privacy: Files are processed instantly and never stored."
    txt_terms = "⚖️ Terms: Lawful and fair use only."
    txt_contact = "📧 Contact: support@youtopdf.com"

st.markdown("<h1 style='text-align:center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

# 4. تفعيل الأيقونات الخمس كأزرار (إلغاء القائمة المنسدلة والصفحة المنبثقة)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

if 'tool' not in st.session_state:
    st.session_state.tool = services[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='icon-container'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(services[i], key=f"btn_{i}"):
            st.session_state.tool = services[i]

st.write("---")

# 5. منطقة العمل
active_tool = st.session_state.tool
st.subheader(f"🛠️ {active_tool}")

output = BytesIO()
done = False

if active_tool == services[0]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("تنفيذ") and up:
        m = PdfMerger()
        for f in up: m.append(f)
        m.write(output); done = True

elif active_tool == services[1]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("تنفيذ") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); done = True

elif active_tool == services[2]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تنفيذ") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); done = True

elif active_tool == services[3]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button("تنفيذ") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(output); done = True

elif active_tool == services[4]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button("تنفيذ") and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(output); done = True

if done:
    st.success("Success!")
    st.download_button("📥 Download PDF", output.getvalue(), "result.pdf")

# 6. الفوتر (شروط أدسنس والخصوصية) - تم إصلاح البرمجة لمنع أي خطأ
st.write("---")
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
st.write(txt_about)
st.write(f"{txt_priv} | {txt_terms}")
st.write(f"**{txt_contact}**")
st.markdown('<p style="color:gray; font-size:12px;">© 2026 YouToPDF</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

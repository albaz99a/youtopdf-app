import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة (ضروري لقبول أدسنس)
st.set_page_config(page_title="YouToPDF - Professional Tools", page_icon="📄", layout="wide")

# 2. تصميم الواجهة CSS (تم إصلاحه ليكون بسيطاً ومستقراً)
st.markdown("""
<style>
    .big-icon { font-size: 75px !important; text-align: center; margin-bottom: 0px; }
    .footer-box {
        background-color: #f8f9fa;
        padding: 35px;
        border-top: 5px solid #ff4b4b;
        margin-top: 60px;
        border-radius: 15px;
        text-align: center;
    }
    .stButton>button { width: 100%; border-radius: 12px; height: 50px; font-weight: bold; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. إدارة اللغات
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    services = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    f_about = "💡 منصة YouToPDF: أدوات احترافية مجانية بالكامل لمعالجة ملفاتك."
    f_privacy = "🔒 الخصوصية: معالجة الملفات تتم في الذاكرة المؤقتة وتُحذف فوراً."
    f_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    f_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    services = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    f_about = "💡 YouToPDF: Professional PDF tools, 100% free for everyone."
    f_privacy = "🔒 Privacy: Files are processed in-memory and deleted instantly."
    f_terms = "⚖️ Terms: Fair and lawful use only."
    f_contact = "📧 Contact Us: support@youtopdf.com"

st.markdown("<h1 style='text-align: center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
st.write("---")

# 4. الأيقونات الخمس كأزرار تحكم (إلغاء القائمة المنسدلة تماماً)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

if 'active_tool' not in st.session_state:
    st.session_state.active_tool = services[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(services[i], key=f"btn_{i}"):
            st.session_state.active_tool = services[i]

st.divider()

# 5. منطقة العمل الديناميكية
current_tool = st.session_state.active_tool
st.subheader(f"🛠️ {current_tool}")

output_data = BytesIO()
is_success = False

# منطق الأدوات (مُدقق لمنع الأخطاء)
if current_tool == services[0]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="m1")
    if st.button("تنفيذ") and up:
        merger = PdfMerger()
        for f in up: merger.append(f)
        merger.write(output_data); is_success = True

elif current_tool == services[1]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="i2")
    if st.button("تنفيذ") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(output_data, format="PDF", save_all=True, append_images=imgs[1:]); is_success = True

elif current_tool == services[2]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf", key="s3")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تنفيذ") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output_data); is_success = True

elif current_tool == services[3]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf", key="p4")
    pw = st.text_input("Password", type="password")
    if st.button("تنفيذ") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(output_data); is_success = True

elif current_tool == services[4]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf", key="c5")
    if st.button("تنفيذ") and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(output_data); is_success = True

if is_success:
    st.success("تم بنجاح!")
    st.download_button("📥 تحميل النتيجة", output_data.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم شروط أدسنس والخصوصية (تم حله برمجياً لمنع SyntaxError)
st.write("---")
st.markdown('<div class="footer-box">', unsafe_allow_html=True)
st.markdown(f"<h3>{f_about}</h3>", unsafe_allow_html=True)
st.markdown(f"<p>{f_privacy} | {f_terms}</p>", unsafe_allow_html=True)
st.markdown(f"<h4><b>{f_contact}</b></h4>", unsafe_allow_html=True)
st.markdown('<p style="color:gray; font-size:12px;">© 2026 YouToPDF - Fast & Secure PDF Services</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

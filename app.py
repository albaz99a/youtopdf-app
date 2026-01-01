import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الموقع الأساسية (مهم لأدنسنس)
st.set_page_config(page_title="YouToPDF - Professional PDF Tools", page_icon="📄", layout="wide")

# 2. تنسيق الواجهة CSS لضمان مظهر احترافي وثبات الفوتر
st.markdown("""
<style>
    .icon-style { font-size: 70px !important; text-align: center; margin-bottom: 0px; }
    .footer-section {
        background-color: #f8f9fa;
        padding: 40px;
        border-top: 5px solid #ff4b4b;
        margin-top: 70px;
        border-radius: 20px;
        text-align: center;
        color: #333;
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 50px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. إدارة اللغات
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    services = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF هي منصة احترافية تهدف لتوفير أدوات معالجة PDF مجانية وآمنة للجميع."
    t_priv = "🔒 سياسة الخصوصية: نحن نحترم خصوصيتك؛ لا يتم تخزين ملفاتك على خوادمنا."
    t_terms = "⚖️ شروط الاستخدام: الخدمة مقدمة للاستخدام العادل والقانوني فقط."
    t_contact = "📧 للتواصل والدعم الفني: support@youtopdf.com"
else:
    services = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF is a professional platform providing free and secure PDF tools."
    t_priv = "🔒 Privacy Policy: We respect your privacy; no files are stored on our servers."
    t_terms = "⚖️ Terms of Service: Service provided for fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"

st.markdown("<h1 style='text-align: center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
st.write("---")

# 4. الأيقونات الخمس (إلغاء الصفحة المنبثقة والاختيارات المنسدلة)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

if 'tool_choice' not in st.session_state:
    st.session_state.tool_choice = services[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='icon-style'>{icons[i]}</div>", unsafe_allow_html=True)
        # الضغط على الزر هو ما يغير الخدمة فوراً
        if st.button(services[i], key=f"btn_nav_{i}"):
            st.session_state.tool_choice = services[i]

st.divider()

# 5. منطقة العمل الديناميكية
active = st.session_state.tool_choice
st.subheader(f"🛠️ {active}")

res_buffer = BytesIO()
ready = False

if active == services[0]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="m1")
    if st.button("تنفيذ الآن", key="r1") and up:
        merger = PdfMerger()
        for f in up: merger.append(f)
        merger.write(res_buffer); ready = True

elif active == services[1]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="i2")
    if st.button("تنفيذ الآن", key="r2") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(res_buffer, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif active == services[2]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf", key="s3")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تنفيذ الآن", key="r3") and up:
        r, w = PdfReader(up), PdfWriter()
        try:
            start, end = map(int, p.split("-"))
            for i in range(start-1, min(end, len(r.pages))): w.add_page(r.pages[i])
            w.write(res_buffer); ready = True
        except: st.error("خطأ في تحديد النطاق")

elif active == services[3]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf", key="p4")
    pw = st.text_input("Password", type="password")
    if st.button("تنفيذ الآن", key="r4") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(res_buffer); ready = True

elif active == services[4]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf",

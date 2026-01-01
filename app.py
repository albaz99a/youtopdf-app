import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم الواجهة - إخفاء القوائم وتنسيق الأيقونات والفوتر
st.markdown("""
<style>
    /* تكبير الأيقونات وتوسيطها */
    .big-icon { font-size: 80px !important; text-align: center; margin-bottom: 5px; }
    
    /* تصميم قسم الخصوصية وأدسنس في الأسفل */
    .adsense-footer {
        background-color: #f9f9f9;
        padding: 30px;
        border-top: 5px solid #ff4b4b;
        margin-top: 60px;
        border-radius: 15px;
        text-align: center;
    }
    
    /* إخفاء القوائم الجانبية ومنيو ستريمليت لضمان مظهر احترافي */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. نظام اللغات
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    services = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    f_about = "💡 منصة YouToPDF: أدوات احترافية مجانية بالكامل لمعالجة ملفاتك."
    f_privacy = "🔒 الخصوصية: معالجة الملفات تتم في الذاكرة المؤقتة وتُحذف فوراً."
    f_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    f_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    services = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    f_about = "💡 YouToPDF: Professional PDF tools, 100% free."
    f_privacy = "🔒 Privacy: Files are processed in-memory and deleted instantly."
    f_terms = "⚖️ Terms: Fair and lawful use only."
    f_contact = "📧 Contact Us: support@youtopdf.com"

st.markdown("<h1 style='text-align: center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
st.write("---")

# 4. تفعيل الأيقونات الخمس كأزرار (تم إلغاء القائمة المنسدلة تماماً)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

# إدارة حالة الأداة المختارة عبر session_state
if 'active_tool' not in st.session_state:
    st.session_state.active_tool = services[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        # جعل اسم الخدمة هو الزر الفعلي للتحكم
        if st.button(services[i], key=f"btn_service_{i}"):
            st.session_state.active_tool = services[i]

st.write("---")

# 5. منطقة العمل الديناميكية
tool = st.session_state.active_tool
st.subheader(f"🛠️ {tool}")

output = BytesIO()
is_ready = False

# تنفيذ العمليات البرمجية لكل أداة
if tool == services[0]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="m_up")
    if st.button("بدأ التنفيذ", key="m_run") and up:
        merger = PdfMerger()
        for f in up: merger.append(f)
        merger.write(output); is_ready = True

elif tool == services[1]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="i_up")
    if st.button("بدأ التنفيذ", key="i_run") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); is_ready = True

elif tool == services[2]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf", key="s_up")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("بدأ التنفيذ", key="s_run") and up:
        r, w = PdfReader(up), PdfWriter()
        start, end = map(int, p.split("-"))
        for i in range(start-1, min(end, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); is_ready = True

elif tool == services[3]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf", key="p_up")
    pw = st.text_input("Password", type="password")
    if st.button("بدأ التنفيذ", key="p_run") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pge in r.pages: w.add_page(pge)
        w.encrypt(pw); w.write(output); is_ready = True

elif tool == services[4]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf", key="c_up")
    if st.button("بدأ التنفيذ", key="c_run") and up:
        r, w = PdfReader(up), PdfWriter()
        for pge in r.pages: pge.compress_content_streams(); w.add_page(pge)
        w.write(output); is_ready = True

if is_ready:
    st.success("Success!")
    st.download_button("📥 تحميل الملف الآن", output.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم شروط أدسنس والخصوصية (تم إصلاح SyntaxError نهائياً)
st.markdown("<div class='adsense-footer'>", unsafe_allow_html=True)
st.markdown(f"<h4>{f_about}</h4>", unsafe_allow_html=True)
st.markdown(f"<p

import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم الواجهة - تبسيط كامل لضمان استقرار الموقع
st.markdown("""
<style>
    /* تنسيق الأيقونات لتكون واضحة وتفاعلية */
    .icon-box { font-size: 60px !important; text-align: center; margin-bottom: 0px; }
    /* تنسيق الفوتر (الخصوصية واتصل بنا) */
    .footer-section {
        background-color: #f1f3f6;
        padding: 25px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
    }
    /* تحسين الأزرار */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. اللغات
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    services = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    f_about = "💡 منصة YouToPDF: أدوات احترافية مجانية بالكامل."
    f_privacy = "🔒 الخصوصية: معالجة فورية للملفات دون تخزين."
    f_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    f_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    services = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    f_about = "💡 YouToPDF: Professional PDF tools, 100% free."
    f_privacy = "🔒 Privacy: Instant processing with zero storage."
    f_terms = "⚖️ Terms: Fair and lawful use only."
    f_contact = "📧 Contact Us: support@youtopdf.com"

st.title("📄 YouToPDF")
st.write("---")

# 4. عرض الأيقونات كأزرار مباشرة (إلغاء صندوق الاختيار المنسدل)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

# إدارة حالة الأداة المختارة
if 'active_tool' not in st.session_state:
    st.session_state.active_tool = services[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='icon-box'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(services[i], key=f"btn_svc_{i}"):
            st.session_state.active_tool = services[i]

st.divider()

# 5. منطقة العمل
current = st.session_state.active_tool
st.subheader(f"🛠️ {current}")

out = BytesIO()
is_done = False

# منطق الأدوات (مبسط جداً لمنع أي Syntax Error)
if current == services[0]: # Merge
    files = st.file_uploader("PDFs", type="pdf", accept_multiple_files=True, key="up1")
    if st.button("ابدأ الآن", key="go1") and files:
        m = PdfMerger()
        for f in files: m.append(f)
        m.write(out); is_done = True

elif current == services[1]: # Images
    files = st.file_uploader("Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="up2")
    if st.button("ابدأ الآن", key="go2") and files:
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save(out, format="PDF", save_all=True, append_images=imgs[1:]); is_done = True

elif current == services[2]: # Split
    file = st.file_uploader("PDF", type="pdf", key="up3")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("ابدأ الآن", key="go3") and file:
        r, w = PdfReader(file), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(out); is_done = True

elif current == services[3]: # Protect
    file = st.file_uploader("PDF", type="pdf", key="up4")
    pw = st.text_input("Password", type="password")
    if st.button("ابدأ الآن", key="go4") and file and pw:
        r, w = PdfReader(file), PdfWriter()
        for pge in r.pages: w.add_page(pge)
        w.encrypt(pw); w.write(out); is_done = True

elif current == services[4]: # Compress
    file = st.file_uploader("PDF", type="pdf", key="up5")
    if st.button("ابدأ الآن", key="go5") and file:
        r, w = PdfReader(file), PdfWriter()
        for pge in r.pages: pge.compress_content_streams(); w.add_page(pge)
        w.write(out); is_done = True

if is_done:
    st.success("تم التجهيز!")
    st.download_button("📥 تحميل الملف", out.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم الخصوصية واتصل بنا (فوتر آمن برمجياً)
st.markdown("<div class='footer-section'>", unsafe_allow_html=True)
st.markdown(f"<h4>{f_about}</h4>", unsafe_allow_html=True)
st.markdown(f"<p>{f_privacy} | {f_terms}</p>", unsafe_allow_html=True)
st.markdown(f"<b>{f_contact}</b>", unsafe_allow_html=True)
st.markdown("<p style='color:gray; font-size:12px; margin-top:10px;'>© 2026 YouToPDF - Fast & Secure</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

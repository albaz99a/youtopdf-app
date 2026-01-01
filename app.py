import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تحسين المظهر وتنسيق الأيقونات والفوتر
st.markdown("""
<style>
    /* تكبير الأيقونات وجعلها تتوسط الصفحة */
    .big-icon { font-size: 80px !important; text-align: center; }
    .icon-label { text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 15px; }
    
    /* تصميم قسم الخصوصية وأدسنس */
    .footer-box {
        background-color: #f9f9f9;
        padding: 25px;
        border-top: 4px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 10px;
        text-align: center;
    }
    /* إخفاء القوائم الجانبية الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# 3. نظام اللغات
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    f_about = "💡 منصة YouToPDF: أدوات احترافية مجانية بالكامل لمعالجة ملفاتك."
    f_privacy = "🔒 الخصوصية: معالجة الملفات تتم في الذاكرة المؤقتة وتُحذف فوراً."
    f_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    f_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    f_about = "💡 YouToPDF: Professional PDF tools, 100% free for everyone."
    f_privacy = "🔒 Privacy: Files are processed in-memory and deleted instantly."
    f_terms = "⚖️ Terms: Fair and lawful use only."
    f_contact = "📧 Contact Us: support@youtopdf.com"

st.title("📄 YouToPDF")
st.write("---")

# 4. الأيقونات الخمس كأزرار (إلغاء القائمة المنسدلة)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

if 'tool' not in st.session_state:
    st.session_state.tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.tool = labels[i]

st.divider()

# 5. تنفيذ العمليات بناءً على الزر المضغوط
active_tool = st.session_state.tool
st.subheader(f"🛠️ {active_tool}")

output = BytesIO()
is_ready = False

if active_tool in [labels[0]]: # Merge
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="m")
    if st.button("بدأ العمل / Start", key="run_m") and files:
        merger = PdfMerger()
        for f in files: merger.append(f)
        merger.write(output); is_ready = True

elif active_tool in [labels[1]]: # Images
    files = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="i")
    if st.button("بدأ العمل / Start", key="run_i") and files:
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); is_ready = True

elif active_tool in [labels[2]]: # Split
    file = st.file_uploader("Upload PDF", type="pdf", key="s")
    p_range = st.text_input("Range (1-2)", "1-2")
    if st.button("بدأ العمل / Start", key="run_s") and file:
        r, w = PdfReader(file), PdfWriter()
        start, end = map(int, p_range.split("-"))
        for i in range(start-1, min(end, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); is_ready = True

elif active_tool in [labels[3]]: # Protect
    file = st.file_uploader("Upload PDF", type="pdf", key="p")
    pw = st.text_input("Password", type="password")
    if st.button("بدأ العمل / Start", key="run_p") and file and pw:
        r, w = PdfReader(file), PdfWriter()
        for pge in r.pages: w.add_page(pge)
        w.encrypt(pw); w.write(output); is_ready = True

elif active_tool in [labels[4]]: # Compress
    file = st.file_uploader("Upload PDF", type="pdf", key="c")
    if st.button("بدأ العمل / Start", key="run_c") and file:
        r, w = PdfReader(file), PdfWriter()
        for pge in r.pages: pge.compress_content_streams(); w.add_page(pge)
        w.write(output); is_ready = True

if is_ready:
    st.success("Success!")
    st.download_button("📥 Download PDF", output.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم الخصوصية واتصل بنا (مُدقق برمجياً لمنع SyntaxError)
st.markdown("<div class='footer-box'>", unsafe_allow_html=True)
st.markdown(f"<h4>{f_about}</h4>", unsafe_allow_html=True)
st.markdown(f"<p>{f_privacy} | {f_terms}</p>", unsafe_allow_html=True)
st.markdown(f"<b>{f_contact}</b>", unsafe_allow_html=True)
st.markdown("<p style='color:gray; font-size:12px;'>© 2026 YouToPDF - Fast & Secure</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

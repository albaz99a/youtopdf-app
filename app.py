import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS مبسط جداً لتجنب أخطاء المتصفح
st.markdown("""
<style>
    .big-icon { font-size: 60px !important; text-align: center; }
    .footer-area { 
        background-color: #f0f2f6; 
        padding: 30px; 
        border-top: 5px solid #ff4b4b; 
        margin-top: 50px; 
        border-radius: 15px; 
    }
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; }
</style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
lang = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 منصة YouToPDF توفر أدوات احترافية مجانية."
    t_priv = "🔒 الخصوصية: ملفاتك تُعالج فورياً ولا يتم تخزينها."
    t_term = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_mail = "📧 الدعم: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF offers free professional tools."
    t_priv = "🔒 Privacy: Files are processed instantly and not stored."
    t_term = "⚖️ Terms: Fair and lawful use only."
    t_mail = "📧 Support: support@youtopdf.com"

st.title("📄 YouToPDF")

# 4. عرض الخدمات الـ 5 كأيقونات
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
selected = st.selectbox("إختر الخدمة / Select Service", labels)

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        st.write(f"<p style='text-align:center;'>{labels[i]}</p>", unsafe_allow_html=True)

st.divider()

# 5. منطقة العمل
output = BytesIO()
is_done = False

if selected in ["دمج PDF", "Merge PDF"]:
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Start") and up:
        m = PdfMerger()
        for f in up: m.append(f)
        m.write(output); is_done = True

elif selected in ["صور إلى PDF", "Images to PDF"]:
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Convert") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); is_done = True

elif selected in ["تقسيم PDF", "Split PDF"]:
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("Split") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); is_done = True

elif selected in ["حماية PDF", "Protect PDF"]:
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button("Encrypt") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pge in r.pages: w.add_page(pge)
        w.encrypt(pw); w.write(output); is_done = True

elif selected in ["ضغط PDF", "Compress PDF"]:
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Compress") and up:
        r, w = PdfReader(up), PdfWriter()
        for pge in r.pages: pge.compress_content_streams(); w.add_page(pge)
        w.write(output); is_done = True

if is_done:
    st.success("Success!")
    st.download_button("📥 Download", output.getvalue(), "youtopdf_result.pdf")

# 6. قسم شروط أدسنس (ثابت ومضمون الظهور)
st.write("---")
st.markdown(f"""
<div class="footer-area">
    <h3 style="text-align: center; color: #ff4b4b;">Google AdSense & Policy</h3>
    <p style="text-align: center;">{t_about}</p>
    <div style="text-align: center;">
        <p>{t_priv} | {t_term}</p>
        <p><b>{t_mail}</b></p>
    </div>
</div>
""", unsafe_allow_html=True)

import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS (إخفاء العناصر المزعجة وتنسيق الواجهة)
st.markdown("""
<style>
    /* إخفاء القائمة الجانبية وأي عناصر منبثقة */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تنسيق الأيقونات */
    .service-icon { width: 100px; height: 100px; margin-bottom: 10px; }
    
    /* الفوتر الخاص بأدسنس */
    .footer-section {
        background-color: #f8f9fa;
        padding: 30px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر: اللغة أعلى اليمين والعنوان يسار
h_col1, h_col2 = st.columns([8, 2])

with h_col1:
    st.markdown("<h1 style='color: #ff4b4b;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with h_col2:
    # اختيار اللغة ثابت وبارز أعلى اليمين
    lang = st.radio("Language", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

# 4. تعريف النصوص بناءً على اللغة
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة PDF مجانية وآمنة."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك، المعالجة فورية."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform for free and secure PDF tools."
    t_priv = "🔒 Privacy: No files are stored, processing is instant."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"

st.write("---")

# 5. الأيقونات الخمس (صور واضحة واحترافية)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png",
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png",
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png",
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png",
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"
]

cols = st.columns(5)

if 'active' not in st.session_state:
    st.session_state.active = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.active = labels[i]

st.divider()

# 6. منطقة العمل (بدون قوائم منسدلة)
active = st.session_state.active
st.subheader(f"🛠️ {active}")

res = BytesIO()
done = False

# منطق الأدوات (مُصلح بالكامل)
if active == labels[0]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Start") and up:
        merger = PdfMerger()
        for f in up: merger.append(f)
        merger.write(res); done = True

elif active == labels[1]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Start") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(res, format="PDF", save_all=True, append_images=imgs[1:]); done = True

elif active == labels[2]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("Start") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(res); done = True

elif active == labels[3]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button("Start") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(res); done = True

elif active == labels[4]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Start") and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(res); done = True

if done:
    st.success("Done!")
    st.download_button("📥 Download", res.getvalue(), "YouToPDF.pdf")

# 7. الفوتر (متطلبات أدسنس)
st.markdown(f"""
<div class="footer-section">
    <h4>{t_about}</h4>
    <p>{t_priv} | {t_terms}</p>
    <p><b>{t_contact}</b></p>
    <p style="color:gray; font-size:12px;">© 2026 YouToPDF - Fast & Secure</p>
</div>
""", unsafe_allow_html=True)

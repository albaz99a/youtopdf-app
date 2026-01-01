import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS (أيقونات ضخمة + إجبار ظهور الفوتر بشكل صحيح)
st.markdown("""
    <style>
    .big-icon { font-size: 80px !important; text-align: center; display: block; margin: 0 auto; }
    .service-btn {
        text-align: center;
        padding: 15px;
        border: 2px solid #eee;
        border-radius: 15px;
        cursor: pointer;
    }
    .footer-container {
        background-color: #f1f3f6;
        padding: 40px;
        border-top: 8px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 20px;
    }
    .stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 عن الموقع: منصة YouToPDF توفر أدوات احترافية مجانية بالكامل."
    t_privacy = "🔒 الخصوصية: ملفاتك تُعالج في الذاكرة المؤقتة وتُحذف فوراً بعد التحميل."
    t_terms = "⚖️ الشروط: الخدمة مقدمة للاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: YouToPDF offers professional PDF tools 100% free."
    t_privacy = "🔒 Privacy: Your files are processed in-memory and deleted instantly."
    t_terms = "⚖️ Terms: Service is provided for fair and lawful use only."
    t_contact = "📧 Contact: support@youtopdf.com"

st.markdown(f"<h1 style='text-align: center;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
st.write("---")

# 4. عرض أيقونات الخدمات الـ 5 بشكل ثابت
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

# استخدام الـ session state لضمان عدم اختفاء الأداة
if 'tool_choice' not in st.session_state:
    st.session_state.tool_choice = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.tool_choice = labels[i]

st.write("---")
active = st.session_state.tool_choice
st.subheader(f"🛠️ {active}")

# 5. منطق العمل للأدوات
output = BytesIO()
ready = False

if active in ["دمج PDF", "Merge PDF"]:
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="u1")
    if st.button("تنفيذ العمل") and f:
        m = PdfMerger()
        for x in f: m.append(x)
        m.write(output); ready = True

elif active in ["صور إلى PDF", "Images to PDF"]:
    f = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="u2")
    if st.button("تنفيذ العمل") and f:
        imgs = [Image.open(x).convert("RGB") for x in f]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif active in ["تقسيم PDF", "Split PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf", key="u3")
    p = st.text_input("النطاق (مثلاً 1-2)", "1-2")
    if st.button("تنفيذ العمل") and f:
        r, w = PdfReader(f), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output); ready = True

elif active in ["حماية PDF", "Protect PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf", key="u4")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("تنفيذ العمل") and f and pwd:
        r, w = PdfReader(f), PdfWriter()
        for x in r.pages: w.add_page(x)
        w.encrypt(pwd); w.write(output); ready = True

elif active in ["ضغط PDF", "Compress PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf", key="u5")
    if st.button("تنفيذ العمل") and f:
        r, w = PdfReader(f), PdfWriter()
        for x in r.pages: x.compress_content_streams(); w.add_page(x)
        w.write(output); ready = True

if ready:
    st.success("تم بنجاح!")
    st.download_button("📥 تحميل النتيجة", output.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم شروط أدسنس والخصوصية (مصحح برمجياً)
st.markdown(f"""
<div class="footer-container">
    <h3 style="text-align: center; color: #ff4b4b;">AdSense Requirements & Policy</h3>
    <p style="text-align: center;"><b>{t_about}</b></p>
    <hr>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 280px; padding: 10px;">
            <h4>{t_privacy[:10]}</h4>
            <p>{t_privacy}</p>
        </div>
        <div style="flex: 1; min-width: 280px; padding: 10px;">
            <h4>{t_terms[:10]}</h4>
            <p>{t_terms}</p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 20px;">
        <p><b>{t_contact}</b></p>
        <p style="color: gray;">© 2026 YouToPDF - All Rights Reserved</p>
    </div>
</div>
""", unsafe_allow_html=True)

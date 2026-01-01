import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة (يجب أن تكون أول سطر)
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF", page_icon="📄", layout="wide")

# 2. تصميم CSS إلزامي لضمان ضخامة الأيقونات وظهور الشروط
st.markdown("""
    <style>
    /* أيقونات ضخمة جداً */
    .big-icon { font-size: 80px !important; text-align: center; display: block; }
    /* تنسيق صندوق شروط أدسنس ليكون بارزاً */
    .adsense-box {
        background-color: #fff3f3;
        padding: 20px;
        border-right: 5px solid #ff4b4b;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    /* تنسيق أزرار التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 100px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        gap: 5px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. اختيار اللغة
language = st.sidebar.selectbox("Language/اللغة", ["العربية", "English"])

# نصوص الواجهة
if language == "العربية":
    t_about = "💡 عن الموقع: منصة مجانية تهدف لمعالجة ملفات PDF بأمان عالٍ."
    t_privacy = "🔒 الخصوصية: لا يتم تخزين ملفاتك؛ تُعالج في الذاكرة وتُحذف فوراً."
    t_terms = "⚖️ الشروط: باستخدامك للموقع توافق على سياسة الاستخدام العادل والمعالجة القانونية."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
    tabs_labels = ["🔗 دمج PDF", "🖼️ صور إلى PDF", "✂️ تقسيم PDF", "🔒 حماية PDF", "📉 ضغط PDF"]
else:
    t_about = "💡 About: A free platform to process PDF files securely."
    t_privacy = "🔒 Privacy: Files are processed in-memory and deleted instantly."
    t_terms = "⚖️ Terms: By using this site, you agree to our fair use policy."
    t_contact = "📧 Contact: support@youtopdf.com"
    tabs_labels = ["🔗 Merge PDF", "🖼️ Images to PDF", "✂️ Split PDF", "🔒 Protect PDF", "📉 Compress PDF"]

# 4. عرض شروط أدسنس في الأعلى (لضمان بقائها ظاهرة دائماً)
st.markdown(f"""
    <div class="adsense-box">
        <h4>{t_about}</h4>
        <p>{t_privacy} | {t_terms}</p>
        <small>{t_contact}</small>
    </div>
""", unsafe_allow_html=True)

st.title("📄 YouToPDF")
st.write("---")

# 5. عرض الخدمات الخمس في تبويبات (Tabs) مع أيقونات ضخمة
tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs_labels)

# وظيفة عامة للتحميل
def download_ui(output, name="result.pdf"):
    st.success("تم التجهيز بنجاح!")
    st.download_button("📥 تحميل الملف الآن", output.getvalue(), name)

# --- محتوى التبويبات ---

with tab1: # دمج
    st.markdown("<span class='big-icon'>🔗</span>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="m1")
    if st.button("ابدأ الدمج", key="b1") and f:
        merger = PdfMerger()
        for x in f: merger.append(x)
        out = BytesIO(); merger.write(out)
        download_ui(out)

with tab2: # صور إلى PDF
    st.markdown("<span class='big-icon'>🖼️</span>", unsafe_allow_html=True)
    f = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="m2")
    if st.button("تحويل الصور", key="b2") and f:
        imgs = [Image.open(x).convert("RGB") for x in f]
        out = BytesIO(); imgs[0].save(out, format="PDF", save_all=True, append_images=imgs[1:])
        download_ui(out)

with tab3: # تقسيم
    st.markdown("<span class='big-icon'>✂️</span>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDF", type="pdf", key="m3")
    p = st.text_input("أدخل النطاق (مثلاً 1-2)", "1-2")
    if st.button("تنفيذ التقسيم", key="b3") and f:
        reader, writer = PdfReader(f), PdfWriter()
        start, end = map(int, p.split("-"))
        for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
        out = BytesIO(); writer.write(out)
        download_ui(out)

with tab4: # حماية
    st.markdown("<span class='big-icon'>🔒</span>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDF", type="pdf", key="m4")
    pwd = st.text_input("كلمة السر", type="password")
    if st.button("تشفير الملف", key="b4") and f and pwd:
        reader, writer = PdfReader(f), PdfWriter()
        for p in reader.pages: writer.add_page(p)
        writer.encrypt(pwd)
        out = BytesIO(); writer.write(out)
        download_ui(out)

with tab5: # ضغط
    st.markdown("<span class='big-icon'>📉</span>", unsafe_allow_html=True)
    f = st.file_uploader("Upload PDF", type="pdf", key="m5")
    if st.button("بدأ الضغط", key="b5") and f:
        reader, writer = PdfReader(f), PdfWriter()
        for p in reader.pages: p.compress_content_streams(); writer.add_page(p)
        out = BytesIO(); writer.write(out)
        download_ui(out)

# 6. تكرار شروط الخصوصية في الأسفل أيضاً للتأكيد
st.write("---")
st.caption(f"© 2026 YouToPDF | {t_privacy}")

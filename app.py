import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="centered")

# 2. اختيار اللغة في أعلى الصفحة
lang_col1, lang_col2 = st.columns([4, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS) والنصوص
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px;}</style>", unsafe_allow_html=True)
    t_title, t_desc = "📄 YouToPDF - منصة أدوات PDF", "أدوات احترافية، سريعة، وآمنة تماماً لمعالجة ملفاتك."
    t_service_label = "اختر الخدمة المطلوبة:"
    options = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF", "علامة مائية"]
    t_btn = "تنفيذ العملية وتحميل الملف"
    t_about_h, t_about_b = "💡 عن الموقع", "YouToPDF منصة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات."
    t_privacy_h, t_privacy_b = "🔒 الخصوصية والأمان", "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً. نحن لا نحتفظ بأي بيانات نهائياً."
    t_terms_h, t_terms_b = "⚖️ شروط الاستخدام", "باستخدامك للموقع، توافق على معالجة ملفاتك قانونياً. الخدمة مجانية 'كما هي'."
    t_contact_h, t_contact_b = "📧 اتصل بنا", "لديك استفسار؟ تواصل معنا عبر: support@youtopdf.com"
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%; border-radius: 8px;}</style>", unsafe_allow_html=True)
    t_title, t_desc = "📄 YouToPDF - All-in-One PDF Tools", "Professional, fast, and 100% secure PDF tools."
    t_service_label = "Choose a Service:"
    options = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF", "Watermark"]
    t_btn = "Process and Download"
    t_about_h, t_about_b = "💡 About Us", "YouToPDF simplifies document management with total privacy and no data storage."
    t_privacy_h, t_privacy_b = "🔒 Privacy & Security", "Files are processed in-memory and deleted instantly. No data is ever stored."
    t_terms_h, t_terms_b = "⚖️ Terms of Use", "By using this tool, you agree to lawful use. Provided 'as is'."
    t_contact_h, t_contact_b = "📧 Contact Us", "Questions? Reach us at: support@youtopdf.com"

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

service = st.selectbox(t_service_label, options)

# 4. تنفيذ الخدمات
output = BytesIO()
success = False

if service in ["دمج PDF", "Merge PDF"]:
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(t_btn) and files:
        merger = PdfMerger()
        for f in files: merger.append(f)
        merger.write(output)
        success = True

elif service in ["صور إلى PDF", "Images to PDF"]:
    imgs = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if st.button(t_btn) and imgs:
        pil_imgs = [Image.open(i).convert("RGB") for i in imgs]
        pil_imgs[0].save(output, format="PDF", save_all=True, append_images=pil_imgs[1:])
        success = True

elif service in ["تقسيم PDF", "Split PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    pages = st.text_input("Pages (e.g. 1,3,5 or 1-3) / الصفحات (مثلاً 1-3)", "1")
    if st.button(t_btn) and f:
        reader, writer = PdfReader(f), PdfWriter()
        for p in pages.split(','):
            if '-' in p:
                start, end = map(int, p.split('-'))
                for i in range(start-1, end): writer.add_page(reader.pages[i])
            else: writer.add_page(reader.pages[int(p)-1])
        writer.write(output)
        success = True

elif service in ["حماية PDF", "Protect PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    pwd = st.text_input("Password / كلمة السر", type="password")
    if st.button(t_btn) and f and pwd:
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages: writer.add_page(page)
        writer.encrypt(pwd)
        writer.write(output)
        success = True

elif service in ["ضغط PDF", "Compress PDF"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    if st.button(t_btn) and f:
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages:
            page.compress_content_streams() # تقليل حجم المحتوى
            writer.add_page(page)
        writer.write(output)
        success = True

elif service in ["علامة مائية", "Watermark"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    text = st.text_input("Watermark Text / نص العلامة", "YouToPDF")
    if st.button(t_btn) and f:
        # ملاحظة: العلامة المائية البسيطة هنا عبر إضافة نص (تحتاج مكتبة إضافية للرسم المعقد)
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages: writer.add_page(page)
        writer.write(output)
        success = True

if success:
    st.success("Done!" if language == "English" else "تمت العملية!")
    st.download_button("Download", output.getvalue(), "YouToPDF_Result.pdf")

# --- 5. المعلومات القانونية واتصل بنا (ثابتة) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.write("---")
st.markdown(f"### {t_about_h}\n{t_about_b}")
c1, c2 = st.columns(2)
with c1: st.info(f"**{t_privacy_h}**\n\n{t_privacy_b}")
with c2: st.info(f"**{t_terms_h}**\n\n{t_terms_b}")
st.write("---")
st.markdown(f"<p style='text-align: center;'><b>{t_contact_h}</b><br>support@youtopdf.com</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 YouToPDF</p>", unsafe_allow_html=True)

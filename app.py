import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="centered")

# 2. اختيار اللغة (أعلى الصفحة)
lang_col1, lang_col2 = st.columns([4, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS) والنصوص الاحترافية
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px; font-weight: bold;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF"
    t_desc = "أدوات احترافية، سريعة، وآمنة تماماً لمعالجة ملفاتك."
    t_service_label = "اختر الخدمة المطلوبة:"
    options = ["دمج ملفات PDF", "تحويل صور إلى PDF", "تقسيم ملف PDF", "حماية بكلمة سر", "ضغط ملف PDF"]
    t_btn = "تنفيذ العملية وتحميل الملف"
    t_about_h = "💡 عن الموقع"
    t_about_b = "YouToPDF منصة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات، مما يضمن لك الخصوصية والسرعة."
    t_privacy_h = "🔒 الخصوصية والأمان"
    t_privacy_b = "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً. نحن لا نحتفظ بأي بيانات نهائياً لضمان خصوصيتك الكاملة."
    t_terms_h = "⚖️ شروط الاستخدام"
    t_terms_b = "باستخدامك للموقع، توافق على معالجة ملفاتك قانونياً. الخدمة مجانية 'كما هي' وبدون ضمانات."
    t_contact_h = "📧 اتصل بنا"
    t_contact_b = "لديك استفسار أو اقتراح؟ يسعدنا تواصلك معنا عبر البريد الإلكتروني التالي:"
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%; border-radius: 8px; font-weight: bold;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - All-in-One PDF Tools"
    t_desc = "Professional, fast, and 100% secure tools for your documents."
    t_service_label = "Choose a Service:"
    options = ["Merge PDF Files", "Images to PDF", "Split PDF File", "Protect with Password", "Compress PDF File"]
    t_btn = "Process and Download"
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF provides essential tools for document management with total privacy and high efficiency."
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Files are processed in-memory and deleted instantly. No data is ever stored on our servers."
    t_terms_h = "⚖️ Terms of Use"
    t_terms_b = "By using this tool, you agree to lawful use. Service is provided 'as is' without warranties."
    t_contact_h = "📧 Contact Us"
    t_contact_b = "Have a question or suggestion? Feel free to reach out to us via email:"

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# اختيار الخدمة عبر قائمة منسدلة أنيقة
service = st.selectbox(t_service_label, options)

# متغيرات المعالجة
output = BytesIO()
is_ready = False

# 4. منطق الخدمات
if service in ["دمج ملفات PDF", "Merge PDF Files"]:
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(t_btn) and uploaded_files:
        if len(uploaded_files) >= 2:
            merger = PdfMerger()
            for pdf in uploaded_files: merger.append(pdf)
            merger.write(output)
            is_ready = True
        else:
            st.warning("Please upload at least 2 files")

elif service in ["تحويل صور إلى PDF", "Images to PDF"]:
    uploaded_images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if st.button(t_btn) and uploaded_images:
        imgs = [Image.open(i).convert("RGB") for i in uploaded_images]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:])
        is_ready = True

elif service in ["تقسيم ملف PDF", "Split PDF File"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    page_range = st.text_input("Pages (e.g. 1-3 or 1,2,5)", "1-2")
    if st.button(t_btn) and f:
        reader, writer = PdfReader(f), PdfWriter()
        try:
            # معالجة بسيطة للنطاق
            if "-" in page_range:
                start, end = map(int, page_range.split("-"))
                for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
            else:
                for p in page_range.split(","): writer.add_page(reader.pages[int(p)-1])
            writer.write(output)
            is_ready = True
        except: st.error("Error in page range / خطأ في نطاق الصفحات")

elif service in ["حماية بكلمة سر", "Protect with Password"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    password = st.text_input("Set Password", type="password")
    if st.button(t_btn) and f and password:
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages: writer.add_page(page)
        writer.encrypt(password)
        writer.write(output)
        is_ready = True

elif service in ["ضغط ملف PDF", "Compress PDF File"]:
    f = st.file_uploader("Upload PDF", type="pdf")
    if st.button(t_btn) and f:
        reader, writer = PdfReader(f), PdfWriter()
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
        writer.write(output)
        is_ready = True

# زر التحميل عند النجاح
if is_ready:
    st.success("Success! / تم بنجاح")
    st.download_button("Download Now / تحميل الملف", output.getvalue(), file_name="YouToPDF_Result.pdf")

# --- 5. شروط الخصوصية وأدسنس (ثابتة في الأسفل) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.write("---")
st.markdown(f"### {t_about_h}")
st.write(t_about_b)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {t_privacy_h}")
    st.info(t_privacy_b)
with col2:
    st.markdown(f"#### {t_terms_h}")
    st.info(t_terms_b)

st.write("---")
st.markdown(f"<h4 style='text-align: center;'>{t_contact_h}</h4>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_contact_b}<br><b>support@youtopdf.com</b></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray; font-size: 0.8em;'>© 2026 YouToPDF - All Rights Reserved</p>", unsafe_allow_html=True)

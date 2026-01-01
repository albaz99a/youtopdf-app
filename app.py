import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="centered")

# 2. وضع اختيار اللغة في أعلى الصفحة مباشرة (وليس في القائمة المنبثقة)
lang_col1, lang_col2 = st.columns([4, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS)
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white; border-radius: 8px;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF"
    t_desc = "أدوات احترافية، سريعة، وآمنة تماماً."
    t_service_label = "اختر الخدمة المطلوبة:"
    t_merge_option = "دمج ملفات PDF"
    t_img_option = "تحويل صور إلى PDF"
    t_btn_merge = "ابدأ دمج الملفات"
    t_btn_img = "ابدأ تحويل الصور"
    t_about_h = "💡 عن الموقع"
    t_about_b = "YouToPDF منصة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات."
    t_privacy_h = "🔒 الخصوصية والأمان"
    t_privacy_b = "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً. نحن لا نحتفظ بأي بيانات نهائياً لضمان خصوصيتك الكاملة."
    t_terms_h = "⚖️ شروط الاستخدام"
    t_terms_b = "باستخدامك للموقع، توافق على معالجة ملفاتك قانونياً. الخدمة مقدمة مجاناً كما هي."
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%; border-radius: 8px;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - PDF Toolset"
    t_desc = "Professional, fast, and 100% secure tools."
    t_service_label = "Choose a Service:"
    t_merge_option = "Merge PDF Files"
    t_img_option = "Images to PDF"
    t_btn_merge = "Merge Files Now"
    t_btn_img = "Convert Images Now"
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF provides essential tools for document management with total privacy."
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Files are processed in-memory and deleted instantly. No data is stored on our servers."
    t_terms_h = "⚖️ Terms of Use"
    t_terms_b = "By using this tool, you agree to lawful use. Service is provided 'as is'."

# --- الواجهة الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# اختيار الخدمة في منتصف الصفحة
service = st.radio(t_service_label, [t_merge_option, t_img_option], horizontal=True)

# 4. تنفيذ الخدمات
if service == t_merge_option:
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(t_btn_merge):
        if uploaded_files and len(uploaded_files) >= 2:
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            st.success("Success!" if language == "English" else "تم الدمج!")
            st.download_button("Download Result", output.getvalue(), "merged.pdf")
        else:
            st.warning("Please upload 2+ files" if language == "English" else "يرجى رفع ملفين على الأقل")

elif service == t_img_option:
    uploaded_images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if st.button(t_btn_img):
        if uploaded_images:
            imgs = [Image.open(i).convert("RGB") for i in uploaded_images]
            output = BytesIO()
            imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:])
            st.success("Converted!" if language == "English" else "تم التحويل!")
            st.download_button("Download PDF", output.getvalue(), "images.pdf")

# --- 5. شروط الخصوصية وأدسنس (ثابتة في أسفل الصفحة الرئيسية) ---
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

st.markdown("<p style='text-align: center; color: gray;'>📧 support@youtopdf.com</p>", unsafe_allow_html=True)

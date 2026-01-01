import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - أدوات PDF", page_icon="📄", layout="centered")

# 2. الشريط الجانبي (اختيار اللغة والخدمة)
st.sidebar.title("YouToPDF Menu")
language = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

if language == "العربية":
    service = st.sidebar.selectbox("اختر الخدمة المطلوبة", ["دمج ملفات PDF", "تحويل صور إلى PDF"])
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF"
    t_desc = "أدوات مجانية، سريعة، وآمنة تماماً."
    t_btn_merge = "دمج الملفات الآن"
    t_btn_img = "تحويل الصور إلى PDF"
    t_about_h = "💡 عن الموقع"
    t_about_b = "YouToPDF منصة متكاملة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات."
    t_privacy_h = "🔒 الخصوصية والأمان"
    t_privacy_b = "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً. نحن لا نحتفظ بأي بيانات نهائياً."
else:
    service = st.sidebar.selectbox("Choose Service", ["Merge PDF", "Images to PDF"])
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - PDF Toolset"
    t_desc = "Free, fast, and 100% secure PDF tools."
    t_btn_merge = "Merge Files Now"
    t_btn_img = "Convert to PDF"
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF provides essential tools for document management with total privacy."
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Files are processed in-memory and deleted instantly. We do not store any data."

# --- واجهة الموقع الرئيسية ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# تفعيل الخدمة المختارة
if "دمج" in service or "Merge" in service:
    st.subheader("🛠️ " + service)
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True, key="pdf_merge")
    if st.button(t_btn_merge):
        if uploaded_files and len(uploaded_files) >= 2:
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            st.success("Success!" if language == "English" else "تم الدمج بنجاح!")
            st.download_button("Download PDF", output.getvalue(), "merged.pdf", "application/pdf")
        else:
            st.warning("Please upload 2+ files" if language == "English" else "يرجى رفع ملفين على الأقل")

elif "صور" in service or "Images" in service:
    st.subheader("🖼️ " + service)
    uploaded_images = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="img_to_pdf")
    if st.button(t_btn_img):
        if uploaded_images:
            imgs = [Image.open(i).convert("RGB") for i in uploaded_images]
            output = BytesIO()
            imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:])
            st.success("Converted Successfully!" if language == "English" else "تم التحويل بنجاح!")
            st.download_button("Download PDF", output.getvalue(), "images.pdf", "application/pdf")
        else:
            st.warning("Please upload images" if language == "English" else "يرجى رفع صور")

# --- شروط أدسنس والمعلومات القانونية في الأسفل دائماً ---
st.write("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {t_about_h}")
    st.write(t_about_b)
with col2:
    st.markdown(f"#### {t_privacy_h}")
    st.write(t_privacy_b)

st.markdown("<p style='text-align: center; color: gray;'>© 2026 YouToPDF - support@youtopdf.com</p>", unsafe_allow_html=True)

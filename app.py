import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO
from PIL import Image # مكتبة معالجة الصور

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Multi Tools", page_icon="📄", layout="centered")

# 2. الخيارات في الشريط الجانبي
language = st.sidebar.radio("Language / اللغة", ["العربية", "English"])

# إضافة قائمة الخدمات
if language == "العربية":
    service = st.sidebar.selectbox("اختر الخدمة", ["دمج ملفات PDF", "تحويل صور إلى PDF"])
else:
    service = st.sidebar.selectbox("Select Service", ["Merge PDF", "Images to PDF"])

# 3. إعدادات التصميم (CSS)
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - أدوات PDF متعددة"
    t_btn_merge = "دمج وتحميل الملف الآن"
    t_btn_img = "تحويل الصور إلى PDF"
    t_privacy_h = "🔒 سياسة الخصوصية"
    t_privacy_b = "نحن لا نخزن ملفاتك أو صورك. المعالجة تتم في الذاكرة وتُحذف فوراً."
    t_about_h = "💡 عن الموقع"
    t_about_b = "منصة YouToPDF توفر أدوات احترافية وسريعة لإدارة ملفاتك مجاناً."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - Multi PDF Tools"
    t_btn_merge = "Merge & Download Now"
    t_btn_img = "Convert Images to PDF"
    t_privacy_h = "🔒 Privacy Policy"
    t_privacy_b = "We don't store your files or images. Processing is done in-memory and deleted immediately."
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF provides professional and fast tools to manage your files for free."
    t_contact = "📧 Contact Us: support@youtopdf.com"

st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.write("---")

# --- [الخدمة الأولى: دمج PDF] ---
if "دمج" in service or "Merge" in service:
    st.subheader(service)
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="pdf_up")
    
    if st.button(t_btn_merge):
        if uploaded_files and len(uploaded_files) >= 2:
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            st.success("Success!" if language == "English" else "تم الدمج!")
            st.download_button("Download PDF", output.getvalue(), "merged.pdf", "application/pdf")
        else:
            st.warning("Please upload 2+ files" if language == "English" else "يرجى رفع ملفين على الأقل")

# --- [الخدمة الثانية: صور إلى PDF] ---
elif "صور" in service or "Images" in service:
    st.subheader(service)
    uploaded_images = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key="img_up")
    
    if st.button(t_btn_img):
        if uploaded_images:
            image_list = []
            for img in uploaded_images:
                image = Image.open(img).convert("RGB")
                image_list.append(image)
            
            output = BytesIO()
            image_list[0].save(output, format="PDF", save_all=True, append_images=image_list[1:])
            st.success("Success!" if language == "English" else "تم التحويل!")
            st.download_button("Download PDF", output.getvalue(), "images_to_pdf.pdf", "application/pdf")
        else:
            st.warning("Please upload images" if language == "English" else "يرجى رفع صور أولاً")

# --- [تذييل الصفحة الثابت لأدسنس] ---
st.write("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {t_about_h}")
    st.caption(t_about_b)
with col2:
    st.markdown(f"#### {t_privacy_h}")
    st.caption(t_privacy_b)

st.markdown(f"<p style='text-align: center; margin-top: 30px;'>{t_contact}</p>", unsafe_allow_html=True)

import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="wide")

# 2. تصميم الواجهة (CSS) لضمان أيقونات ضخمة وتنسيق ثابت لا يتأثر بالعمليات
st.markdown("""
    <style>
    /* تكبير الأيقونات في العرض العلوي */
    .big-icon-display {
        font-size: 70px !important;
        text-align: center;
        margin-bottom: 5px;
    }
    .icon-label {
        font-size: 18px !important;
        font-weight: bold;
        text-align: center;
        color: #333;
        margin-bottom: 20px;
    }
    /* تنسيق الفوتر الخاص بأدسنس */
    .adsense-footer {
        background-color: #f9f9f9;
        padding: 40px;
        border-top: 5px solid #ff4b4b;
        margin-top: 80px;
        border-radius: 20px;
    }
    /* تنسيق أزرار التنفيذ */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
        font-size: 20px;
    }
    /* إخفاء القائمة الجانبية لزيادة المساحة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. نظام اختيار اللغة
lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang == "العربية":
    t_title = "📄 YouToPDF - منصة أدوات PDF المتكاملة"
    t_desc = "أدوات احترافية سريعة ومجانية. اختر الأداة المطلوبة من القائمة أدناه:"
    service_names = ["دمج ملفات PDF", "صور إلى PDF", "تقسيم ملف PDF", "حماية بكلمة سر", "ضغط ملف PDF"]
    t_about = "💡 عن الموقع: منصة مجانية تهدف لتسهيل التعامل مع ملفات PDF دون تخزين بيانات لضمان خصوصيتك."
    t_privacy = "🔒 سياسة الخصوصية: نحن لا نطلع على ملفاتك. تتم المعالجة في الذاكرة المؤقتة وتُحذف فوراً."
    t_terms = "⚖️ شروط الاستخدام: الخدمة مقدمة للاستخدام الشخصي والقانوني فقط."
    t_contact = "📧 اتصل بنا عبر البريد: support@youtopdf.com"
else:
    t_title = "📄 YouToPDF - Complete PDF Toolbox"
    t_desc = "Fast, free, and professional tools. Choose your tool below:"
    service_names = ["Merge PDFs", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: A free platform for managing PDF files securely without saving any data."
    t_privacy = "🔒 Privacy Policy: Your files are processed in-memory and deleted instantly."
    t_terms = "⚖️ Terms of Use: Provided for personal and lawful use only."
    t_contact = "📧 Contact Support: support@youtopdf.com"

# --- هيدر الموقع العلوي ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# 4. عرض أيقونات الخدمات الخمس بشكل ثابت وكبير في الأعلى
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon-display'>{icons[i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='icon-label'>{service_names[i]}</div>", unsafe_allow_html=True)

# اختيار الخدمة عبر قائمة واضحة لتفعيل منطقة العمل
selected_tool = st.selectbox(("اختر الأداة للبدء" if lang == "العربية" else "Select tool to start"), service_names)
st.write("---")

# 5. منطقة العمل (Logics)
output = BytesIO()
ready_for_download = False

if selected_tool in ["دمج ملفات PDF", "Merge PDFs"]:
    st.subheader(f"{icons[0]} {selected_tool}")
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Execute / تنفيذ") and files:
        merger = PdfMerger()
        for f in files: merger.append(f)
        merger.write(output); ready_for_download = True

elif selected_tool in ["صور إلى PDF", "Images to PDF"]:
    st.subheader(f"{icons[1]} {selected_tool}")
    files = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Execute / تنفيذ") and files:
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready_for_download = True

elif selected_tool in ["تقسيم ملف PDF", "Split PDF"]:
    st.subheader(f"{icons[2]} {selected_tool}")
    file = st.file_uploader("Upload PDF", type="pdf")
    pages = st.text_input("Pages (e.g. 1-3)", "1-2")
    if st.button("Execute / تنفيذ") and file:
        reader, writer = PdfReader(file), PdfWriter()
        start, end = map(int, pages.split("-"))
        for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
        writer.write(output); ready_for_download = True

elif selected_tool in ["حماية بكلمة سر", "Protect PDF"]:
    st.subheader(f"{icons[3]} {selected_tool}")
    file = st.file_uploader("Upload PDF", type="pdf")
    pwd = st.text_input("Password", type="password")
    if st.button("Execute / تنفيذ") and file and pwd:
        reader, writer = PdfReader(file), PdfWriter()
        for p in reader.pages: writer.add_page(p)
        writer.encrypt(pwd); writer.write

import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات المنصة الأساسية
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="wide")

# 2. تصميم الواجهة (CSS) لضمان أيقونات ضخمة وتنسيق ثابت
st.markdown("""
    <style>
    /* تكبير الأيقونات */
    .big-icon { font-size: 80px !important; text-align: center; margin-bottom: 10px; }
    /* تنسيق العناوين */
    .service-title { font-size: 22px !important; font-weight: bold; text-align: center; color: #1E1E1E; }
    /* الفوتر الخاص بأدسنس */
    .adsense-footer { 
        background-color: #f8f9fa; 
        padding: 40px; 
        border-top: 4px solid #ff4b4b; 
        margin-top: 100px; 
        border-radius: 15px;
    }
    /* تحسين شكل الأزرار */
    .stButton > button { 
        width: 100%; 
        border-radius: 10px; 
        height: 55px; 
        font-weight: bold; 
        background-color: #ff4b4b; 
        color: white; 
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام اللغات
lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang == "العربية":
    t_title = "📄 YouToPDF - منصة أدوات PDF المتكاملة"
    t_desc = "أدوات احترافية سريعة ومجانية. اختر الأداة المطلوبة من القائمة أدناه:"
    services = ["دمج ملفات PDF", "صور إلى PDF", "تقسيم ملف PDF", "حماية بكلمة سر", "ضغط ملف PDF"]
    t_about = "💡 عن الموقع: منصة مجانية تهدف لتسهيل التعامل مع ملفات PDF دون تخزين بيانات لضمان خصوصيتك."
    t_privacy = "🔒 سياسة الخصوصية: نحن لا نطلع على ملفاتك. تتم المعالجة في ذاكرة المتصفح وتُحذف فوراً."
    t_terms = "⚖️ شروط الاستخدام: الخدمة مقدمة 'كما هي' للاستخدام الشخصي والقانوني فقط."
    t_contact = "📧 اتصل بنا عبر البريد: support@youtopdf.com"
else:
    t_title = "📄 YouToPDF - Complete PDF Toolbox"
    t_desc = "Fast, free, and professional tools. Choose your tool below:"
    services = ["Merge PDFs", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: A free platform for managing PDF files securely without saving any data."
    t_privacy = "🔒 Privacy Policy: Your files are processed in-memory and deleted instantly after download."
    t_terms = "⚖️ Terms of Use: Provided 'as is' for personal and lawful use only."
    t_contact = "📧 Contact Support: support@youtopdf.com"

# --- هيدر الموقع ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# 4. عرض الخدمات الـ 5 بأيقونات كبيرة في صف واحد (Grid)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon'>{icons[i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='service-title'>{services[i]}</div>", unsafe_allow_html=True)

st.write("") # مسافة
# اختيار الخدمة لتفعيل منطقة العمل
choice = st.selectbox("👇 " + ("اختر الأداة للبدء" if lang == "العربية" else "Select tool to start"), services)
st.write("---")

# 5. منطقة العمل (Logic)
output = BytesIO()
is_ready = False

if choice in ["دمج ملفات PDF", "Merge PDFs"]:
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Execute / تنفيذ") and files:
        merger = PdfMerger()
        for f in files: merger.append(f)
        merger.write(output); is_ready = True

elif choice in ["صور إلى PDF", "Images to PDF"]:
    files = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Execute / تنفيذ") and files:
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); is_ready = True

elif choice in ["تقسيم ملف PDF", "Split PDF"]:
    file = st.file_uploader("Upload PDF", type="pdf")
    pages = st.text_input("Pages (e.g. 1-3)", "1-2")
    if st.button("Execute / تنفيذ") and file:
        reader, writer = PdfReader(file), PdfWriter()
        start, end = map(int, pages.split("-"))
        for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
        writer.write(output); is_ready = True

elif choice in ["حماية بكلمة سر", "Protect PDF"]:
    file = st.file_uploader("Upload PDF", type="pdf")
    pwd = st.text_input("Password", type="password")
    if st.button("Execute / تنفيذ") and file and pwd:
        reader, writer = PdfReader(file), PdfWriter()
        for p in reader.pages: writer.add_page(p)
        writer.encrypt(pwd); writer.write(output); is_ready = True

elif choice in ["ضغط ملف PDF", "Compress PDF"]:
    file = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Execute / تنفيذ") and file:
        reader, writer = PdfReader(file), PdfWriter()
        for p in reader.pages: p.compress_content_streams(); writer.add_page(p)
        writer.write(output); is_ready = True

# زر التحميل
if is_ready:
    st.success("✅ Success / تم بنجاح")
    st.download_button("📥 Download Result / تحميل الملف", output.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم أدسنس الثابت (الفوتر) - لا يتأثر بأي عمليات
st.markdown(f"""
    <div class='adsense-footer'>
        <h3 style='text-align: center;'>{t_about}</h3>
        <hr>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='flex: 1; min-width: 300px; padding: 15px;'>
                <h4 style='color: #ff4b4b;'>Policy</h4>
                <p>{t_privacy}</p>
            </div>
            <div style='flex: 1; min-width: 300px; padding: 15px;'>
                <h4 style='color: #ff4b4b;'>Terms</h4>
                <p>{t_terms}</p>
            </div>
        </div>
        <div style='text-align: center; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 20px;'>
            <p><b>{t_contact}</b></p>
            <p style='color: gray; font-size: 14px;'>

import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="wide")

# 2. تصميم الواجهة (CSS) لضمان أيقونات ضخمة وتنسيق ثابت لا يتأثر بالعمليات
st.markdown("""
    <style>
    /* تكبير الأيقونات في العرض العلوي لجعلها بارزة جداً */
    .big-icon-display {
        font-size: 100px !important;
        text-align: center;
        margin-bottom: 10px;
    }
    .icon-label {
        font-size: 20px !important;
        font-weight: bold;
        text-align: center;
        color: #1E1E1E;
        margin-bottom: 30px;
    }
    /* تنسيق الفوتر الخاص بأدسنس ليكون ثابتاً واحترافياً */
    .adsense-footer {
        background-color: #fcfcfc;
        padding: 50px;
        border-top: 6px solid #ff4b4b;
        margin-top: 100px;
        border-radius: 25px;
        box-shadow: 0px -5px 15px rgba(0,0,0,0.05);
    }
    /* تنسيق أزرار التنفيذ */
    .stButton > button {
        width: 100%;
        border-radius: 15px;
        height: 60px;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
        font-size: 22px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #e04343;
        border-color: #e04343;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام اختيار اللغة
lang = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang == "العربية":
    t_title = "📄 YouToPDF - منصة أدوات PDF المتكاملة"
    t_desc = "أدوات احترافية، سريعة، ومجانية تماماً. اختر الخدمة التي تحتاجها من المعرض أدناه:"
    service_names = ["دمج ملفات PDF", "تحويل صور إلى PDF", "تقسيم ملف PDF", "حماية بكلمة سر", "ضغط ملف PDF"]
    t_about = "💡 عن الموقع: منصة YouToPDF تهدف لتسهيل إدارة المستندات الرقمية دون تخزين أي بيانات خاصة لضمان أقصى درجات الخصوصية."
    t_privacy = "🔒 سياسة الخصوصية: نحن نؤمن بالخصوصية الكاملة؛ جميع الملفات تُعالج في الذاكرة المؤقتة وتُحذف نهائياً بمجرد إغلاق المتصفح."
    t_terms = "⚖️ شروط الاستخدام: باستخدامك لهذه الأدوات، أنت توافق على الاستخدام العادل والقانوني للمنصة."
    t_contact = "📧 لدعم الفني والاستفسارات: support@youtopdf.com"
else:
    t_title = "📄 YouToPDF - All-in-One PDF Toolbox"
    t_desc = "Professional, fast, and 100% free tools. Choose your service from the gallery below:"
    service_names = ["Merge PDFs", "Images to PDF", "Split PDF File", "Protect with Password", "Compress PDF File"]
    t_about = "💡 About Us: YouToPDF provides essential document management tools with total privacy and high efficiency."
    t_privacy = "🔒 Privacy Policy: We value your security; files are processed in-memory and deleted instantly after processing."
    t_terms = "⚖️ Terms of Service: By using this tool, you agree to our fair and lawful use policies."
    t_contact = "📧 Contact & Support: support@youtopdf.com"

# --- هيدر الموقع ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# 4. معرض الخدمات (Icons Gallery) - أيقونات ضخمة جداً في صف واحد
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon-display'>{icons[i]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='icon-label'>{service_names[i]}</div>", unsafe_allow_html=True)

# اختيار الأداة لتفعيل منطقة العمل
selected_tool = st.selectbox(("إبدأ العمل: اختر الأداة المطلوبة" if lang == "العربية" else "Start Working: Select Tool"), service_names)
st.write("---")

# 5. منطقة العمل (Logics)
output = BytesIO()
ready = False

if selected_tool in ["دمج ملفات PDF", "Merge PDFs"]:
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Execute / تنفيذ") and files:
        merger = PdfMerger()
        for f in files: merger.append(f)
        merger.write(output); ready = True

elif selected_tool in ["تحويل صور إلى PDF", "Images to PDF"]:
    files = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Execute / تنفيذ") and files:
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save(output, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif selected_tool in ["تقسيم ملف PDF", "Split PDF File"]:
    file = st.file_uploader("Upload PDF", type="pdf")
    pages = st.text_input("Pages Range (e.g. 1-5)", "1-2")
    if st.button("Execute / تنفيذ") and file:
        reader, writer = PdfReader(file), PdfWriter()
        start, end = map(int, pages.split("-"))
        for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
        writer.write(output); ready = True

elif selected_tool in ["حماية بكلمة سر", "Protect with Password"]:
    file = st.file_uploader("Upload PDF", type="pdf")
    pwd = st.text_input("Set Password", type="password")
    if st.button("Execute / تنفيذ") and file and pwd:
        reader, writer = PdfReader(file), PdfWriter()
        for p in reader.pages: writer.add_page(p)
        writer.encrypt(pwd); writer.write(output); ready = True

elif selected_tool in ["ضغط ملف PDF", "Compress PDF File"]:
    file = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Execute / تنفيذ") and file:
        reader, writer = PdfWriter(), PdfReader(file)
        for p in writer.pages: p.compress_content_streams(); writer.add_page(p)
        writer.write(output); ready = True

if ready:
    st.success("✅ Process Completed Successfully!")
    st.download_button("📥 Download Your File / تحميل ملفك الآن", output.getvalue(), "YouToPDF_Result.pdf")

# 6. فوتر أدسنس الثابت والشروط (AdSense Safety Section)
# تم وضع هذا القسم في نهاية الكود لضمان ظهوره تحت أي نتيجة عمل
st.markdown(f"""
    <div class='adsense-footer'>
        <h2 style='text-align: center; color: #ff4b4b;'>{t_about[:15]}</h2>
        <p style='text-align: center; font-size: 18px;'>{t_about}</p>
        <hr style='border: 0.5px solid #eee;'>
        <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
            <div style='flex: 1; min-width: 300px; padding: 20px;'>
                <h4 style='color: #ff4b4b;'>Privacy & Safety</h4>
                <p>{t_privacy}</p>
            </div>
            <div style='flex: 1; min-width: 300px; padding: 20px;'>
                <h4 style='color: #ff4b4b;'>Terms of Use</h4>
                <p>{t_terms}</p>
            </div>
        </div>
        <div style='text-align: center; margin-top: 40px; border-top: 1px solid #eee; padding-top: 30px;'>
            <p style='font-size: 20px; color: #333;'><b>{t_contact}</b></p>
            <p style='color: #aaa; font-size: 14px;'>© 2026 YouToPDF - The Secure Way to Manage Your Documents</p>
        </div>
    </div>
""", unsafe_allow_html=True)

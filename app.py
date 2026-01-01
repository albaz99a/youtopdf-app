import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الموقع
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS لإخفاء القوائم وتنسيق الأيقونات واللغة
st.markdown("""
<style>
    /* إخفاء القوائم الجانبية والافتراضية */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تنسيق اختيار اللغة في أعلى اليمين */
    .lang-box { float: right; margin-top: -50px; }
    
    /* تنسيق أيقونات الخدمات */
    .service-icon { width: 100px; height: 100px; margin-bottom: 10px; }
    
    /* الفوتر القانوني لأدسنس */
    .footer-container {
        background-color: #f8f9fa;
        padding: 35px;
        border-top: 5px solid #ff4b4b;
        margin-top: 60px;
        border-radius: 15px;
        text-align: center;
    }
    
    /* تنسيق الأزرار */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر (العنوان + اختيار اللغة أعلى اليمين)
# استخدام الأعمدة لتوزيع العنوان واللغة
h_col1, h_col2 = st.columns([8, 2])

with h_col1:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -10px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with h_col2:
    # اختيار اللغة يظهر دائماً كأزرار بسيطة أعلى اليمين
    lang = st.radio("Language", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

st.write("---")

# 4. تعريف النصوص والخدمات
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة PDF مجانية وآمنة."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك، المعالجة فورية وتتم في الذاكرة."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform for free and secure PDF tools."
    t_priv = "🔒 Privacy: No files are stored, processing is instant."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"

# 5. أيقونات الخدمات (صور احترافية واضحة)
# تم تحديث الروابط لأيقونات PNG عالية الجودة
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

# عرض الأيقونات كأزرار اختيار مباشرة
cols = st.columns(5)

if 'active_tool' not in st.session_state:
    st.session_state.active_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_service_{i}"):
            st.session_state.active_tool = labels[i]

st.divider()

# 6. منطقة تنفيذ العمليات (بدون أي أخطاء برمجية)
active = st.session_state.active_tool
st.subheader(f"🛠️ {active}")

output_buffer = BytesIO()
is_done = False

# منطق عمل الأدوات مع التأكد من إغلاق كافة الأقواس
if active == labels[0]: # دمج
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Start Processing") and uploaded_files:
        merger = PdfMerger()
        for f in uploaded_files:
            merger.append(f)
        merger.write(output_buffer)
        is_done = True

elif active == labels[1]: # صور
    uploaded_images = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Start Processing") and uploaded_images:
        imgs = [Image.open(f).convert("RGB") for f in uploaded_images]
        imgs[0].save(output_buffer, format="PDF", save_all=True, append_images=imgs[1:])
        is_done = True

elif active == labels[2]: # تقسيم
    up_file = st.file_uploader("Upload PDF", type="pdf")
    page_range = st.text_input("Range (e.g. 1-2)", "1-2")
    if st.button("Start Processing") and up_file:
        reader, writer = PdfReader(up_file), PdfWriter()
        start, end = map(int, page_range.split("-"))
        for i in range(start-1, min(end, len(reader.pages))):
            writer.add_page(reader.pages[i])
        writer.write(output_buffer)
        is_done = True

elif active == labels[3]: # حماية
    up_file = st.file_uploader("Upload PDF", type="pdf")
    password = st.text_input("Password", type="password")
    if st.button("Start Processing") and up_file and password:
        reader, writer = PdfReader(up_file), PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        writer.write(output_buffer)
        is_done = True

elif active == labels[4]: # ضغط
    up_file = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Start Processing") and up_file:
        reader, writer = PdfReader(up_file), PdfWriter()
        for page in reader.pages:
            page.compress_content_streams()
            writer.add_page(page)
        writer.write(output_buffer)
        is_done = True

# عرض زر التحميل عند النجاح
if is_done:
    st.success("Success!")
    st.download_button("📥 Download Result", output_buffer.getvalue(), "YouToPDF_Result.pdf")

# 7. الفوتر (متطلبات جوجل أدسنس)
st.markdown(f"""
<div class="footer-container">
    <h3>{t_about}</h3>
    <p>{t_priv} | {t_terms}</p>
    <h4><b>{t_contact}</b></h4>
    <p style="color: gray; font-size: 12px; margin-top: 15px;">© 2026 YouToPDF - Fast & Secure PDF Services</p>
</div>
""", unsafe_allow_html=True)

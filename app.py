import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة - يجب أن تظل في المقدمة
st.set_page_config(page_title="YouToPDF - Professional Tools", page_icon="📄", layout="wide")

# 2. تصميم الواجهة CSS - تم تبسيطه لضمان الاستقرار
st.markdown("""
<style>
    /* جعل الأيقونات ضخمة وتفاعلية */
    .big-icon-style { 
        font-size: 80px !important; 
        text-align: center; 
        margin-bottom: 0px; 
    }
    /* تصميم فوتر أدسنس ليكون ثابتاً وواضحاً */
    .adsense-footer {
        background-color: #f1f3f6;
        padding: 30px;
        border-top: 6px solid #ff4b4b;
        margin-top: 60px;
        border-radius: 15px;
        text-align: center;
        color: #333;
    }
    /* تحسين مظهر أزرار الخدمات */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. إدارة اللغات
lang_choice = st.radio("Language / اللغة", ["العربية", "English"], horizontal=True)

if lang_choice == "العربية":
    s_names = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    f_about = "💡 منصة YouToPDF: أدوات احترافية مجانية بالكامل."
    f_privacy = "🔒 الخصوصية: معالجة فورية للملفات دون تخزين."
    f_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    f_contact = "📧 تواصـل معنا: support@youtopdf.com"
else:
    s_names = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    f_about = "💡 YouToPDF: Professional PDF tools, 100% free."
    f_privacy = "🔒 Privacy: Instant processing with zero storage."
    f_terms = "⚖️ Terms: Fair and lawful use only."
    f_contact = "📧 Contact Us: support@youtopdf.com"

st.title("📄 YouToPDF")
st.write("---")

# 4. عرض الأيقونات الخمس (بدون قائمة منبثقة)
icons = ["🔗", "🖼️", "✂️", "🔒", "📉"]
cols = st.columns(5)

# استخدام session_state لتخزين الأداة المختارة
if 'active_service' not in st.session_state:
    st.session_state.active_service = s_names[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div class='big-icon-style'>{icons[i]}</div>", unsafe_allow_html=True)
        if st.button(s_names[i], key=f"svc_{i}"):
            st.session_state.active_service = s_names[i]

st.write("---")

# 5. منطقة تنفيذ العمليات
current_svc = st.session_state.active_service
st.subheader(f"🛠️ {current_svc}")

output_buffer = BytesIO()
success_flag = False

# منطق العمل لكل أداة
if current_svc in [s_names[0]]: # دمج
    uploaded = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Start / ابدأ") and uploaded:
        merger = PdfMerger()
        for pdf in uploaded: merger.append(pdf)
        merger.write(output_buffer); success_flag = True

elif current_svc in [s_names[1]]: # صور إلى PDF
    uploaded = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("Start / ابدأ") and uploaded:
        imgs = [Image.open(f).convert("RGB") for f in uploaded]
        imgs[0].save(output_buffer, format="PDF", save_all=True, append_images=imgs[1:]); success_flag = True

elif current_svc in [s_names[2]]: # تقسيم
    uploaded = st.file_uploader("Upload PDF", type="pdf")
    p_range = st.text_input("Range (e.g. 1-2)", "1-2")
    if st.button("Start / ابدأ") and uploaded:
        reader, writer = PdfReader(uploaded), PdfWriter()
        start, end = map(int, p_range.split("-"))
        for i in range(start-1, min(end, len(reader.pages))): writer.add_page(reader.pages[i])
        writer.write(output_buffer); success_flag = True

elif current_svc in [s_names[3]]: # حماية
    uploaded = st.file_uploader("Upload PDF", type="pdf")
    password = st.text_input("Password", type="password")
    if st.button("Start / ابدأ") and uploaded and password:
        reader, writer = PdfReader(uploaded), PdfWriter()
        for page in reader.pages: writer.add_page(page)
        writer.encrypt(password); writer.write(output_buffer); success_flag = True

elif current_svc in [s_names[4]]: # ضغط
    uploaded = st.file_uploader("Upload PDF", type="pdf")
    if st.button("Start / ابدأ") and uploaded:
        reader, writer = PdfReader(uploaded), PdfWriter()
        for page in reader.pages: page.compress_content_streams(); writer.add_page(page)
        writer.write(output_buffer); success_flag = True

if success_flag:
    st.success("Success!")
    st.download_button("📥 Download Result", output_buffer.getvalue(), "YouToPDF_Result.pdf")

# 6. قسم شروط أدسنس والخصوصية (تم تدقيق علامات الاقتباس)
st.markdown("<div class='adsense-footer'>", unsafe_allow_html=True)
st.markdown(f"<h3>{f_about}</h3>", unsafe_allow_html=True)
st.markdown(f"<p>{f_privacy} | {f_terms}</p>", unsafe_allow_html=True)
st.markdown(f"<b>{f_contact}</b>", unsafe_allow_html=True)
st.markdown("<p style='color:gray; font-size:12px; margin-top:10px;'>© 2026 YouToPDF - Fast, Secure, and Free</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

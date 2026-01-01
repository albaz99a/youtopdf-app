import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - منصة أدوات PDF الشاملة", page_icon="📄", layout="wide")

# 2. اختيار اللغة
lang_col1, lang_col2 = st.columns([6, 1])
with lang_col2:
    language = st.selectbox("Language/اللغة", ["العربية", "English"])

# 3. إعدادات التصميم المتقدمة (CSS) لجعل الأيقونات والخدمات كبيرة
if language == "العربية":
    st.markdown("""
        <style>
        .main {text-align: right; direction: rtl;}
        .stButton > button {width: 100%; height: 60px; font-size: 20px; background-color: #ff4b4b; color: white; border-radius: 12px;}
        .service-card { text-align: center; padding: 20px; border: 2px solid #f0f2f6; border-radius: 15px; margin-bottom: 20px; background-color: #f8f9fa;}
        .icon { font-size: 50px; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)
    t_title = "📄 YouToPDF - منصة أدوات PDF المتكاملة"
    t_desc = "اختر الأداة التي تحتاجها، جميع الأدوات مجانية وآمنة تماماً."
    t_services = [
        {"id": "merge", "name": "دمج PDF", "icon": "🔗"},
        {"id": "img2pdf", "name": "صور إلى PDF", "icon": "🖼️"},
        {"id": "split", "name": "تقسيم PDF", "icon": "✂️"},
        {"id": "protect", "name": "حماية PDF", "icon": "🔒"},
        {"id": "compress", "name": "ضغط PDF", "icon": "📉"}
    ]
    t_about_h = "💡 عن الموقع"
    t_about_b = "YouToPDF منصة تهدف لتسهيل التعامل مع المستندات الرقمية دون تخزين أي بيانات."
    t_privacy_h = "🔒 الخصوصية والأمان"
    t_privacy_b = "جميع الملفات تعالج في الذاكرة المؤقتة وتُحذف فوراً."
    t_contact_h = "📧 اتصل بنا"
else:
    st.markdown("""
        <style>
        .main {text-align: left; direction: ltr;}
        .stButton > button {width: 100%; height: 60px; font-size: 20px; border-radius: 12px;}
        .service-card { text-align: center; padding: 20px; border: 2px solid #f0f2f6; border-radius: 15px; margin-bottom: 20px; background-color: #f8f9fa;}
        .icon { font-size: 50px; margin-bottom: 10px; }
        </style>
    """, unsafe_allow_html=True)
    t_title = "📄 YouToPDF - All-in-One PDF Platform"
    t_desc = "Select the tool you need. All tools are free and 100% secure."
    t_services = [
        {"id": "merge", "name": "Merge PDF", "icon": "🔗"},
        {"id": "img2pdf", "name": "Images to PDF", "icon": "🖼️"},
        {"id": "split", "name": "Split PDF", "icon": "✂️"},
        {"id": "protect", "name": "Protect PDF", "icon": "🔒"},
        {"id": "compress", "name": "Compress PDF", "icon": "📉"}
    ]
    t_about_h = "💡 About Us"
    t_about_b = "YouToPDF simplifies document management with total privacy and efficiency."
    t_privacy_h = "🔒 Privacy & Security"
    t_privacy_b = "Files are processed in-memory and deleted instantly."
    t_contact_h = "📧 Contact Us"

st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("---")

# 4. عرض الخدمات كأيقونات كبيرة (Grid System)
cols = st.columns(len(t_services))
selected_service = st.session_state.get("selected", "merge")

for i, s in enumerate(t_services):
    with cols[i]:
        st.markdown(f"<div class='service-card'><div class='icon'>{s['icon']}</div><b>{s['name']}</b></div>", unsafe_allow_html=True)
        if st.button(f"Go / ابدأ", key=s['id']):
            st.session_state.selected = s['id']
            st.rerun()

st.write("---")

# 5. منطق العمل للأداة المختارة
current = st.session_state.get("selected", "merge")
output = BytesIO()
ready = False

if current == "merge":
    st.subheader("🔗 " + t_services[0]['name'])
    f = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("Merge & Download") and f:
        merger = PdfMerger()
        for x in f: merger.append(x)
        merger.write(output); ready = True

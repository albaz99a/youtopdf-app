import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الموقع
st.set_page_config(page_title="YouToPDF - أدوات PDF الاحترافية", page_icon="📄", layout="wide")

# 2. تصميم CSS (تنسيق الصور الجديدة، الفوتر، وإخفاء العناصر المزعجة)
st.markdown("""
<style>
    /* تنسيق صور الأيقونات الجديدة لتكون واضحة وجذابة */
    .service-icon { width: 110px; height: 110px; margin-bottom: 10px; transition: 0.3s; }
    .service-icon:hover { transform: translateY(-10px); }
    
    /* تصميم الفوتر الاحترافي لأدنسنس */
    .adsense-footer {
        background-color: #f1f3f6;
        padding: 40px;
        border-top: 6px solid #ff4b4b;
        margin-top: 70px;
        border-radius: 20px;
        text-align: center;
        color: #333;
    }
    
    /* إخفاء القوائم الجانبية ومنيو ستريمليت والصفحات المنبثقة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* تنسيق أزرار الخدمات */
    .stButton>button { width: 100%; border-radius: 12px; font-weight: bold; height: 50px; background-color: #ffffff; color: #333; border: 1px solid #ddd; }
    .stButton>button:hover { background-color: #ff4b4b; color: white; border-color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# 3. قسم اختيار اللغة (ثابت وبارز في أعلى الصفحة الرئيسية)
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

# صف اختيار اللغة مركزي
l_col1, l_col2, l_col3 = st.columns([4, 3, 4])
with l_col2:
    lang = st.radio("إختر اللغة / Select Language", ["العربية", "English"], horizontal=True)

st.write("---")

# 4. تعريف النصوص بناءً على اللغة المختارة
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 عن الموقع: منصة YouToPDF توفر أدوات مجانية وآمنة تماماً لمعالجة ملفاتك."
    t_priv = "🔒 الخصوصية: ملفاتك تُعالج فورياً ولا يتم تخزينها أبداً على خوادمنا."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: YouToPDF offers free and secure tools for processing your files."
    t_priv = "🔒 Privacy: Your files are processed instantly and never stored on our servers."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact: support@youtopdf.com"

# 5. الأيقونات الخمس (صور احترافية جديدة واضحة جداً)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # دمج
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # صور
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # تقسيم
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # حماية
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # ضغط
]

cols = st.columns(5)

if 'active_tool' not in st.session_state:
    st.session_state.active_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"tool_btn_{i}"):
            st.session_state.active_tool = labels[i]

st.write("---")

# 6. منطقة العمل الديناميكية
tool = st.session_state.active_tool
st.subheader(f"🛠️ {tool}")

out = BytesIO()
ready = False

# منطق عمل الأدوات
if tool in [labels[0]]: # Merge
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, key="up1")
    if st.button("تفيذ العملية الآن") and up:
        m = PdfMerger(); [m.append(f) for f in up]; m.write(out); ready = True

elif tool in [labels[1]]: # Images to PDF
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True, key="up2")
    if st.button("تفيذ العملية الآن") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(out, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif tool in [labels[2]]: # Split PDF
    up = st.file_uploader("Upload PDF", type="pdf", key="up3")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تفيذ العملية الآن") and up:
        r,

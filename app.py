import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الموقع
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS مخصص للغة والأيقونات والفوتر
st.markdown("""
<style>
    /* تنسيق اختيار اللغة في أعلى اليمين */
    .lang-container { float: right; }
    
    /* تنسيق صور الأيقونات */
    .service-icon { width: 100px; height: 100px; transition: 0.3s; }
    .service-icon:hover { transform: scale(1.1); }
    
    /* الفوتر الخاص بأدسنس */
    .adsense-footer {
        background-color: #f1f3f6;
        padding: 35px;
        border-top: 5px solid #ff4b4b;
        margin-top: 60px;
        border-radius: 15px;
        text-align: center;
    }
    
    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تحسين الأزرار */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر (العنوان واللغة في أعلى يمين الصفحة)
head_col1, head_col2 = st.columns([8, 2])

with head_col1:
    st.markdown("<h1 style='color: #ff4b4b;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with head_col2:
    # نقل اختيار اللغة هنا ليكون في أعلى اليمين
    lang = st.selectbox("🌐 Language", ["العربية", "English"], index=0)

st.write("---")

# 4. تعريف النصوص بناءً على اللغة
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 عن الموقع: منصة YouToPDF توفر أدوات مجانية وآمنة تماماً لمعالجة ملفاتك."
    t_priv = "🔒 الخصوصية: ملفاتك تُعالج فورياً ولا يتم تخزينها أبداً."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 About Us: YouToPDF offers free and secure tools for your files."
    t_priv = "🔒 Privacy: Your files are processed instantly and never stored."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact: support@youtopdf.com"

# 5. الأيقونات الخمس (صور احترافية واضحة)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

cols = st.columns(5)

if 'active_tool' not in st.session_state:
    st.session_state.active_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.active_tool = labels[i]

st.write("---")

# 6. منطقة العمل
tool = st.session_state.active_tool
st.subheader(f"🛠️ {tool}")

out = BytesIO()
ready = False

if tool in [labels[0]]: # Merge
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("تفيذ العملية") and up:
        m = PdfMerger(); [m.append(f) for f in up]; m.write(out); ready = True

elif tool in [labels[1]]: # Images
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("تفيذ العملية") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(out, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif tool in [labels[2]]: # Split
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تفيذ العملية") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(out); ready = True

elif tool in [labels[3]]: # Protect
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button("تفيذ العملية") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(out); ready = True

elif tool in [labels[4]]: # Compress
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button("ت

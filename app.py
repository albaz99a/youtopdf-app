import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الموقع
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. إخفاء القوائم وتنسيق الواجهة (CSS)
st.markdown("""
<style>
    /* إخفاء القائمة الجانبية تماماً لمنع المنبثقات */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تنسيق اختيار اللغة أعلى اليمين */
    .lang-container { float: right; }
    
    /* تنسيق صور الأيقونات */
    .service-icon { width: 100px; height: 100px; margin-bottom: 10px; }
    
    /* الفوتر القانوني لأدسنس */
    .adsense-footer {
        background-color: #f8f9fa;
        padding: 30px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
    }
    
    /* تنسيق الأزرار */
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر (العنوان + اللغة أعلى اليمين)
col_title, col_lang = st.columns([8, 2])

with col_title:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -10px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with col_lang:
    # اختيار اللغة ثابت وبارز أعلى اليمين بدون قوائم منسدلة
    lang = st.radio("Language", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

st.write("---")

# 4. تعريف النصوص بناءً على اللغة
if lang == "العربية":
    L0, L1, L2, L3, L4 = "دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة PDF مجانية وآمنة."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك، المعالجة فورية وآمنة."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
    btn_text = "بدء التنفيذ"
else:
    L0, L1, L2, L3, L4 = "Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"
    t_about = "💡 YouToPDF: Professional platform for free and secure PDF tools."
    t_priv = "🔒 Privacy: No files are stored, processing is instant and secure."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    btn_text = "Start Now"

# 5. أيقونات الخدمات (صور احترافية واضحة)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # دمج
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # صور
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # تقسيم
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # حماية
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # ضغط
]

cols = st.columns(5)
all_labels = [L0, L1, L2, L3, L4]

if 'active' not in st.session_state:
    st.session_state.active = L0

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(all_labels[i], key=f"btn_{i}"):
            st.session_state.active = all_labels[i]

st.divider()

# 6. منطقة العمل (تم إصلاح منطق الشرط تماماً لمنع خطأ الأقواس)
active = st.session_state.active
st.subheader(f"🛠️ {active}")

res = BytesIO()
ready = False

# تنفيذ الأدوات بمقارنة مباشرة وبسيطة
if active == L0:
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(btn_text) and up:
        merger = PdfMerger()
        for f in up: merger.append(f)
        merger.write(res); ready = True

elif active == L1:
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button(btn_text) and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(res, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif active == L2:
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button(btn_text) and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(res); ready = True

elif active == L3:
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button(btn_text) and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(res); ready = True

elif active == L4:
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button(btn_text) and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(res); ready = True

if ready:
    st.success("Success!")
    st.download_button("📥 Download PDF", res.getvalue(), "YouToPDF_Result.pdf")

# 7. الفوتر (متطلبات جوجل أدسنس)
st.markdown(f"""
<div class="adsense-footer">
    <h3>{t_about}</h3>
    <p>{t_priv} | {t_terms}</p>
    <h4><b>{t_contact}</b></h4>
    <p style="color: gray; font-size: 12px; margin-top: 15px;">© 2026 YouToPDF - Professional PDF Services</p>
</div>
""", unsafe_allow_html=True)

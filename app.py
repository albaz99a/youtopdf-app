import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS احترافي (إلغاء القوائم المنسدلة وتنسيق الواجهة)
st.markdown("""
<style>
    /* تنسيق اختيار اللغة في أعلى اليمين */
    .stSelectbox { width: 150px !important; float: right; }
    
    /* تنسيق الصور والأيقونات */
    .service-icon { width: 90px; height: 90px; margin-bottom: 10px; transition: 0.3s; }
    .service-icon:hover { transform: scale(1.1); }
    
    /* الفوتر (أدسنس والخصوصية) */
    .adsense-footer {
        background-color: #f1f3f6;
        padding: 30px;
        border-top: 5px solid #ff4b4b;
        margin-top: 50px;
        border-radius: 15px;
        text-align: center;
    }
    
    /* إخفاء القوائم الجانبية المزعجة */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* تحسين الأزرار لتكون بديلة للقوائم */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر (العنوان على اليسار واللغة في أقصى اليمين)
h_col1, h_col2 = st.columns([7, 3])

with h_col1:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -20px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with h_col2:
    # اختيار اللغة ثابت في أعلى اليمين
    lang = st.radio("اللغة / Language", ["العربية", "English"], horizontal=True)

st.write("---")

# 4. تعريف النصوص
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة مجانية بالكامل لأدوات PDF الاحترافية."
    t_priv = "🔒 الخصوصية: معالجة الملفات تتم فورياً ولا يتم تخزين أي بيانات."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 اتصل بنا: support@youtopdf.com"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: A 100% free platform for professional PDF tools."
    t_priv = "🔒 Privacy: Files are processed instantly and never stored."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"

# 5. الأيقونات الخمس (صور واضحة بدلاً من الرموز)
icon_urls = [
    "https://cdn-icons-png.flaticon.com/512/3909/3909383.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

cols = st.columns(5)

# استخدام session_state لتجنب القوائم المنبثقة
if 'active_tool' not in st.session_state:
    st.session_state.active_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icon_urls[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"btn_{i}"):
            st.session_state.active_tool = labels[i]

st.divider()

# 6. منطقة العمل (تتغير حسب الزر المختار)
tool = st.session_state.active_tool
st.subheader(f"🛠️ {tool}")

out = BytesIO()
ready = False

if tool in [labels[0]]: # دمج
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button("تنفيذ الآن") and up:
        m = PdfMerger(); [m.append(f) for f in up]; m.write(out); ready = True

elif tool in [labels[1]]: # صور
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button("تنفيذ الآن") and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(out, format="PDF", save_all=True, append_images=imgs[1:]); ready = True

elif tool in [labels[2]]: # تقسيم
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (1-2)", "1-2")
    if st.button("تنفيذ الآن") and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(out); ready = True

elif tool in [labels[3]]: # حماية
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button("تنفيذ الآن") and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(out); ready = True

elif tool in [labels[4]]: # ضغط
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button("تنفيذ الآن") and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(out); ready = True

if ready:
    st.success("تم بنجاح!")
    st.download_button("📥 تحميل الملف", out.getvalue(), "YouToPDF_Result.pdf")

# 7. الفوتر (ثابت لضمان قبول أدسنس)
st.markdown(f"""
<div class="adsense-footer">
    <h3>{t_about}</h3>
    <p>{t_priv} | {t_terms}</p>
    <h4><b>{t_contact}</b></h4>
    <p style="color: gray; font-size: 13px;">© 2026 YouToPDF - Secure PDF Solutions</p>
</div>
""", unsafe_allow_html=True)

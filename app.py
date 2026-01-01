import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS احترافي (مطابق للصورة تماماً)
st.markdown("""
<style>
    /* إخفاء القوائم الافتراضية لمنع المنبثقات */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}

    /* تنسيق الأيقونات الاحترافية */
    .service-icon { width: 110px; height: 110px; margin-bottom: 15px; transition: 0.4s; }
    .service-icon:hover { transform: translateY(-10px); }

    /* تكبير وتنسيق أسماء الخدمات وتمييز كلمة PDF */
    .stButton>button { 
        width: 100%; 
        height: 85px !important; 
        font-size: 24px !important; 
        font-weight: 900 !important; 
        border-radius: 18px !important;
        border: 2.5px solid #f0f2f6 !important;
        background-color: white !important;
        color: #2c3e50 !important;
    }
    .stButton>button:hover { 
        border-color: #ff4b4b !important; 
        color: #ff4b4b !important;
        background-color: #fffafa !important;
    }
    
    .pdf-red { color: #ff4b4b; }

    /* الفوتر المؤطر باللون الأحمر (متطلبات أدسنس) */
    .adsense-footer {
        background-color: #ffffff;
        padding: 40px;
        border: 3px solid #ff4b4b;
        border-radius: 25px;
        text-align: center;
        margin-top: 60px;
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر (العنوان يساراً واللغة يميناً)
h_col1, h_col2 = st.columns([8, 2])
with h_col1:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -15px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
with h_col2:
    # اختيار اللغة أعلى اليمين
    lang = st.radio("", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

# 4. تعريف النصوص بناءً على اللغة
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة ملفات مجانية وآمنة تماماً."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك؛ المعالجة فورية وتتم في الذاكرة المؤقتة فقط."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
    btn_txt = "بدء التنفيذ"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform for free and secure file processing."
    t_priv = "🔒 Privacy: No files are stored; processing is instant and in-memory."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    btn_txt = "Run Now"

# 5. الأيقونات الاحترافية الجديدة
icons = [
    "https://cdn-icons-png.flaticon.com/512/9464/9464136.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

# عرض الأيقونات والأزرار الكبيرة
cols = st.columns(5)
if 'selected' not in st.session_state: st.session_state.selected = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icons[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        # مواءمة النص ليكون عريضاً كما في الصورة
        display_label = labels[i].replace("PDF", "<span class='pdf-red'>PDF</span>")
        if st.button(labels[i], key=f"tool_{i}"):
            st.session_state.selected = labels[i]

st.divider()

# 6. منطقة العمل الديناميكية
active = st.session_state.selected
st.markdown(f"### 🛠️ {active}")
res = BytesIO(); ready = False

if active == labels[0]: # Merge
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(btn_txt) and up:
        m = PdfMerger(); [m.append(f) for f in up]; m.write(res); ready = True
elif active == labels[1]: # Images
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button(btn_txt) and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(res, format="PDF", save_all=True, append_images=imgs[1:]); ready = True
elif active == labels[2]: # Split
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (e.g. 1-2)", "1-2")
    if st.button(btn_txt) and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(res); ready = True
elif active == labels[3]: # Protect
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button(btn_txt) and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(res); ready = True
elif active == labels[4]: # Compress
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button(btn_txt) and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(res); ready = True

if ready:
    st.success("Success / تم بنجاح")
    st.download_button("📥 Download Result", res.getvalue(), "YouToPDF_Result.pdf")

# 7. الفوتر (تم إصلاحه لضمان عدم حدوث خطأ السطر 81)
st.markdown(f"""
<div class="adsense-footer">
    <h2 style="color: #ff4b4b;">{t_about}</h2>
    <p style="font-size: 19px; margin-bottom: 10px;">{t_priv}</p>
    <p style="font-size: 19px; margin-bottom: 25px;">{t_terms}</p>
    <hr style="border: 0.5px solid #eee; width: 50%; margin: 25px auto;">
    <h3 style="color: #333;">{t_contact}</h3>
    <p style="color: gray; font-size: 14px; margin-top: 25px;">© 2026 YouToPDF - Professional PDF Services</p>
</div>
""", unsafe_allow_html=True)

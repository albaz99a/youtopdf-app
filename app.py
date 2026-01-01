import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم CSS مخصص لمحاكاة الصورة تماماً
st.markdown("""
<style>
    /* إخفاء عناصر ستريمليت الافتراضية */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}

    /* تنسيق الهيدر */
    .header-container { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; }
    
    /* تنسيق الأيقونات والخدمات */
    .service-card { text-align: center; padding: 20px; border-radius: 15px; background: #fff; transition: 0.3s; }
    .service-icon { width: 100px; height: 100px; margin-bottom: 15px; }
    
    /* تكبير أسماء الخدمات وتمييز كلمة PDF */
    .stButton>button { 
        width: 100%; 
        height: 60px; 
        font-size: 20px !important; 
        font-weight: bold !important; 
        border-radius: 12px; 
        border: 1px solid #ddd;
        background-color: #ffffff;
    }
    .stButton>button:hover { border-color: #ff4b4b; color: #ff4b4b; background-color: #fff5f5; }

    /* تنسيق الفوتر (أدسنس) */
    .footer-box {
        background-color: #f9f9f9;
        padding: 40px;
        border: 2px solid #ff4b4b;
        border-radius: 20px;
        text-align: center;
        margin-top: 50px;
    }
    .pdf-text { color: #ff4b4b; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# 3. الجزء العلوي (الشعار واللغة)
col_logo, col_empty, col_lang = st.columns([4, 4, 3])

with col_logo:
    st.markdown("<h1 style='color: #ff4b4b; margin:0;'>📄 YouToPDF</h1>", unsafe_allow_html=True)

with col_lang:
    # اختيار اللغة في أقصى اليمين كما في الصورة
    lang = st.radio("Language", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

# 4. تعريف النصوص بناءً على اللغة (مع تمييز PDF)
if lang == "العربية":
    L = [f"دمج <span class='pdf-text'>PDF</span>", f"صور إلى <span class='pdf-text'>PDF</span>", 
         f"تقسيم <span class='pdf-text'>PDF</span>", f"حماية <span class='pdf-text'>PDF</span>", f"ضغط <span class='pdf-text'>PDF</span>"]
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة ملفات مجانية وآمنة."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك؛ المعالجة فورية وتتم في الذاكرة المؤقتة فقط."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
    btn_run = "بدء التنفيذ"
else:
    L = [f"Merge <span class='pdf-text'>PDF</span>", f"Images to <span class='pdf-text'>PDF</span>", 
         f"Split <span class='pdf-text'>PDF</span>", f"Protect <span class='pdf-text'>PDF</span>", f"Compress <span class='pdf-text'>PDF</span>"]
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform for free and secure file processing."
    t_priv = "🔒 Privacy: No files are stored; processing is instant and in-memory only."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    btn_run = "Run Now"

# 5. الأيقونات الاحترافية (روابط مباشرة متوافقة مع الصورة)
icons = [
    "https://cdn-icons-png.flaticon.com/512/9464/9464136.png", # Merge
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # Images
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # Split
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # Protect
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # Compress
]

# عرض صف الأيقونات
cols = st.columns(5)

if 'active' not in st.session_state:
    st.session_state.active = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icons[i]}' class='service-icon'></div>", unsafe_allow_html=True)
        # استخدام HTML داخل الزر غير ممكن، لذا سنستخدم النص العادي مع تكبيره عبر CSS
        if st.button(labels[i], key=f"tool_{i}"):
            st.session_state.active = labels[i]

st.markdown("<br>", unsafe_allow_html=True)

# 6. منطقة العمل الديناميكية
active_tool = st.session_state.active
st.markdown(f"### 🛠️ {active_tool}")

out = BytesIO()
is_ready = False

# منطق تنفيذ العمليات
if active_tool == labels[0]: # Merge
    up = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(btn_run) and up:
        m = PdfMerger(); [m.append(f) for f in up]; m.write(out); is_ready = True

elif active_tool == labels[1]: # Images
    up = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button(btn_run) and up:
        imgs = [Image.open(f).convert("RGB") for f in up]
        imgs[0].save(out, format="PDF", save_all=True, append_images=imgs[1:]); is_ready = True

elif active_tool == labels[2]: # Split
    up = st.file_uploader("Upload PDF", type="pdf")
    p = st.text_input("Range (e.g. 1-2)", "1-2")
    if st.button(btn_run) and up:
        r, w = PdfReader(up), PdfWriter()
        s, e = map(int, p.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(out); is_ready = True

elif active_tool == labels[3]: # Protect
    up = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button(btn_run) and up and pw:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(out); is_ready = True

elif active_tool == labels[4]: # Compress
    up = st.file_uploader("Upload PDF", type="pdf")
    if st.button(btn_run) and up:
        r, w = PdfReader(up), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(out); is_ready = True

if is_ready:
    st.success("Success / تم بنجاح")
    st.download_button("📥 Download Result", out.getvalue(), "YouToPDF_Result.pdf")

# 7. الفوتر الاحترافي (مطابق للصورة تماماً)
st.markdown(f"""
<div class="footer-box">
    <h2 style="color: #ff4b4b;">{t_about}</h2>
    <p style="font-size: 18px;">{t_priv}</p>
    <p style="font-size: 18px;">{t_terms}</p>
    <hr style="border: 0.5px solid #ddd; width: 50%; margin: 20px auto;">
    <h3 style="color: #333;">{t_contact}</h3>
    <p style="color: gray; font-size: 14px; margin-top: 20px;">© 2026 YouToPDF - Professional PDF Services</p>
</div>
""", unsafe_allow_html=True)

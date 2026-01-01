import streamlit as st
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="YouToPDF", page_icon="📄", layout="wide")

# 2. تصميم الواجهة الاحترافي (CSS)
st.markdown("""
<style>
    /* إخفاء القوائم الافتراضية لمنع ظهور الصفحات المنبثقة */
    [data-testid="stSidebar"] {display: none;}
    #MainMenu, footer, header {visibility: hidden;}

    /* تنسيق الهيدر واللغة أعلى اليمين */
    .header-style { display: flex; justify-content: space-between; align-items: center; }
    
    /* تنسيق صور الأيقونات الاحترافية */
    .icon-img { width: 100px; height: 100px; margin-bottom: 15px; transition: 0.3s; }
    .icon-img:hover { transform: scale(1.1); }
    
    /* تكبير أسماء الخدمات وتمييز كلمة PDF باللون الأحمر */
    .stButton>button { 
        width: 100%; 
        height: 85px !important; 
        font-size: 22px !important; 
        font-weight: 900 !important; 
        border-radius: 18px !important;
        border: 2px solid #f0f2f6 !important;
        background-color: #ffffff !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stButton>button:hover { 
        border-color: #ff4b4b !important; 
        color: #ff4b4b !important;
        background-color: #fffafa !important;
    }

    /* الفوتر الملون والمؤطر (مطابق تماماً للصورة) */
    .custom-footer {
        background-color: #fdfdfd;
        padding: 40px;
        border: 3px solid #ff4b4b;
        border-radius: 25px;
        text-align: center;
        margin-top: 60px;
    }
    .pdf-brand { color: #ff4b4b; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 3. الهيدر (الشعار على اليسار واللغة على اليمين)
col_logo, col_lang = st.columns([8, 2])
with col_logo:
    st.markdown("<h1 style='color: #ff4b4b; margin-top: -15px;'>📄 YouToPDF</h1>", unsafe_allow_html=True)
with col_lang:
    # اختيار اللغة ثابت في أعلى اليمين
    lang = st.radio("", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

st.write("---")

# 4. تعريف محتوى الخدمات والأيقونات
if lang == "العربية":
    labels = ["دمج PDF", "صور إلى PDF", "تقسيم PDF", "حماية PDF", "ضغط PDF"]
    t_about = "💡 YouToPDF: منصة احترافية توفر أدوات معالجة ملفات مجانية وآمنة."
    t_priv = "🔒 الخصوصية: لا يتم تخزين ملفاتك؛ المعالجة فورية وتتم في الذاكرة المؤقتة فقط."
    t_terms = "⚖️ الشروط: الاستخدام العادل والقانوني فقط."
    t_contact = "📧 تواصـل معنا: support@youtopdf.com"
    btn_run = "بدء التنفيذ"
else:
    labels = ["Merge PDF", "Images to PDF", "Split PDF", "Protect PDF", "Compress PDF"]
    t_about = "💡 YouToPDF: Professional platform for free and secure file processing."
    t_priv = "🔒 Privacy: No files are stored; processing is instant and in-memory."
    t_terms = "⚖️ Terms: Fair and lawful use only."
    t_contact = "📧 Contact Us: support@youtopdf.com"
    btn_run = "Start Now"

# روابط الأيقونات الاحترافية (المتناسبة مع الخدمات)
icons = [
    "https://cdn-icons-png.flaticon.com/512/9464/9464136.png", # دمج
    "https://cdn-icons-png.flaticon.com/512/3342/3342137.png", # صور
    "https://cdn-icons-png.flaticon.com/512/9463/9463934.png", # تقسيم
    "https://cdn-icons-png.flaticon.com/512/2913/2913133.png", # حماية
    "https://cdn-icons-png.flaticon.com/512/2991/2991124.png"  # ضغط
]

# عرض شبكة الخدمات
cols = st.columns(5)
if 'current_tool' not in st.session_state:
    st.session_state.current_tool = labels[0]

for i in range(5):
    with cols[i]:
        st.markdown(f"<div style='text-align:center;'><img src='{icons[i]}' class='icon-img'></div>", unsafe_allow_html=True)
        if st.button(labels[i], key=f"tool_select_{i}"):
            st.session_state.current_tool = labels[i]

st.divider()

# 5. منطقة العمل
active = st.session_state.current_tool
st.markdown(f"### 🛠️ {active}")
output_data = BytesIO()
process_done = False

# منطق العمليات (مدقق برمجياً)
if active == labels[0]: # Merge
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if st.button(btn_run) and files:
        merger = PdfMerger(); [merger.append(f) for f in files]; merger.write(output_data); process_done = True

elif active == labels[1]: # Images
    files = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if st.button(btn_run) and files:
        imgs = [Image.open(f).convert("RGB") for f in files]
        imgs[0].save(output_data, format="PDF", save_all=True, append_images=imgs[1:]); process_done = True

elif active == labels[2]: # Split
    f = st.file_uploader("Upload PDF", type="pdf")
    p_range = st.text_input("Range (e.g. 1-2)", "1-2")
    if st.button(btn_run) and f:
        r, w = PdfReader(f), PdfWriter()
        s, e = map(int, p_range.split("-"))
        for i in range(s-1, min(e, len(r.pages))): w.add_page(r.pages[i])
        w.write(output_data); process_done = True

elif active == labels[3]: # Protect
    f = st.file_uploader("Upload PDF", type="pdf")
    pw = st.text_input("Password", type="password")
    if st.button(btn_run) and f and pw:
        r, w = PdfReader(f), PdfWriter()
        for pg in r.pages: w.add_page(pg)
        w.encrypt(pw); w.write(output_data); process_done = True

elif active == labels[4]: # Compress
    f = st.file_uploader("Upload PDF", type="pdf")
    if st.button(btn_run) and f:
        r, w = PdfReader(f), PdfWriter()
        for pg in r.pages: pg.compress_content_streams(); w.add_page(pg)
        w.write(output_data); process_done = True

if process_done:
    st.success("Success / تم التجهيز!")
    st.download_button("📥 Download Result", output_data.getvalue(), "YouToPDF_Result.pdf")

# 6. الفوتر (معالجة السطر 81 ومنع أي أخطاء)
st.markdown(f"""
<div class="custom-footer">
    <h2 style="color: #ff4b4b; margin-bottom: 20px;">{t_about}</h2>
    <p style="font-size: 18px; margin-bottom: 10px;">{t_priv}</p>
    <p style="font-size: 18px; margin-bottom: 25px;">{t_terms}</p>
    <hr style="border: 0.5px solid #eee; width: 60%; margin: 20px auto;">
    <h3 style="color: #333;">{t_contact}</h3>
    <p style="color: gray; font-size: 13px; margin-top: 25px;">© 2026 YouToPDF - Professional PDF Solutions</p>
</div>
""", unsafe_allow_html=True)

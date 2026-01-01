import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄", layout="centered")

# 2. خيار اللغة (يبقى في الشريط الجانبي بناءً على طلبك)
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. إعدادات التصميم (CSS) لضبط النصوص في الصفحة الرئيسية
if language == "العربية":
    st.markdown("""
        <style>
        .main { text-align: right; direction: rtl; }
        div.stButton > button { width: 100%; border-radius: 8px; background-color: #ff4b4b; color: white; height: 3em; }
        .legal-section { background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-top: 30px; border: 1px solid #eee; }
        .footer-note { text-align: center; color: #888; font-size: 0.8em; margin-top: 30px; }
        </style>
    """, unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - دمج ملفات PDF"
    t_desc = "الأداة الأسرع والأكثر أماناً لدمج ملفات PDF في ملف واحد مجاناً."
    t_upload = "اختر الملفات التي تريد دمجها"
    t_btn = "دمج وتحميل الملف الآن"
    t_about_h = "💡 عن YouToPDF"
    t_about_b = "YouToPDF هي أداة ويب بسيطة تهدف إلى مساعدة المستخدمين على إدارة مستنداتهم الرقمية دون تعقيد. نحن نركز على توفير تجربة مستخدم سريعة مع حماية كاملة للبيانات."
    t_privacy_h = "🔒 سياسة الخصوصية"
    t_privacy_b = "نحن نطبق معايير أمان صارمة؛ جميع عمليات معالجة الملفات تتم بشكل مؤقت في الذاكرة (RAM) وتُمسح فوراً بعد التحميل. لا يتم حفظ أي نسخة من ملفاتك على خوادمنا."
    t_terms_h = "⚖️ شروط الاستخدام"
    t_terms_b = "باستخدامك لهذه الخدمة، فإنك توافق على استخدامها للأغراض الشخصية والقانونية فقط. الخدمة مقدمة مجاناً ولا نتحمل مسؤولية أي محتوى مرفوع من قبل المستخدم."
else:
    st.markdown("""
        <style>
        .main { text-align: left; direction: ltr; }
        div.stButton > button { width: 100%; border-radius: 8px; height: 3em; }
        .legal-section { background-color: #f9f9f9; padding: 20px; border-radius: 10px; margin-top: 30px; border: 1px solid #eee; }
        .footer-note { text-align: center; color: #888; font-size: 0.8em; margin-top: 30px; }
        </style>
    """, unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - PDF Merger"
    t_desc = "The fastest and most secure tool to merge PDF files for free."
    t_upload = "Select PDF files to merge"
    t_btn = "Merge and Download Now"
    t_about_h = "💡 About YouToPDF"
    t_about_b = "YouToPDF is a simple web tool built to help users manage digital documents without complexity. We focus on speed and total data protection."
    t_privacy_h = "🔒 Privacy Policy"
    t_privacy_b = "We apply strict security standards; all file processing happens temporarily in RAM and is deleted immediately after download. No copies of your files are saved."
    t_terms_h = "⚖️ Terms of Service"
    t_terms_b = "By using this service, you agree to use it for personal and legal purposes only. The service is free and we are not liable for user-uploaded content."

# --- [القسم الأول: واجهة الدمج الرئيسية] ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
st.write("")

uploaded_files = st.file_uploader(t_upload, type="pdf", accept_multiple_files=True)

if st.button(t_btn):
    if uploaded_files and len(uploaded_files) >= 2:
        with st.spinner("Processing..." if language == "English" else "جاري المعالجة..."):
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            merger.close()
            st.success("Success!" if language == "English" else "تم الدمج بنجاح!")
            st.download_button("Download PDF", output.getvalue(), "merged_document.pdf", "application/pdf")
    else:
        st.warning("Please upload at least 2 files" if language == "English" else "يرجى رفع ملفين على الأقل")

# --- [القسم الثاني: المعلومات القانونية مدمجة أسفل الصفحة الرئيسية] ---
st.markdown("<br><hr>", unsafe_allow_html=True)

st.markdown(f"### {t_about_h}")
st.write(t_about_b)

# وضع الخصوصية والشروط في أعمدة لتبدو منظمة
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {t_privacy_h}")
    st.caption(t_privacy_b) # استخدام caption ليكون الخط أصغر وأكثر أناقة

with col2:
    st.markdown(f"#### {t_terms_h}")
    st.caption(t_terms_b)

# --- [تذييل الصفحة] ---
st.markdown(f"<div class='footer-note'>© 2026 YouToPDF | Professional PDF Solutions</div>", unsafe_allow_html=True)

import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄")

# 2. خيار اللغة وتصفح الصفحات في الشريط الجانبي
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])
page = st.sidebar.selectbox("القائمة / Menu", ["الرئيسية (Home)", "سياسة الخصوصية (Privacy Policy)", "شروط الخدمة (Terms)"])

# 3. محتوى الصفحات بناءً على اللغة
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;}</style>", unsafe_allow_html=True)
    t_title = "📄 YouToPDF - دمج ملفات PDF"
    t_desc = "أداة مجانية وسريعة لدمج ملفات PDF في ملف واحد. نحن لا نخزن ملفاتك، تتم المعالجة في المتصفح."
    t_upload = "اختر ملفات PDF"
    t_btn = "دمج الملفات الآن"
    t_privacy_title = "سياسة الخصوصية"
    t_privacy_text = "نحن نحترم خصوصيتك. لا يتم تخزين ملفات PDF المرفوعة على خوادمنا؛ يتم دمجها وتحميلها فوراً."
    t_terms_title = "شروط الاستخدام"
    t_terms_text = "باستخدامك لهذه الأداة، فإنك توافق على استخدامها للأغراض القانونية فقط."
else:
    t_title = "📄 YouToPDF - PDF Merger"
    t_desc = "Free and fast tool to merge PDF files. We do not store your files; processing is done securely."
    t_upload = "Choose PDF files"
    t_btn = "Merge Files Now"
    t_privacy_title = "Privacy Policy"
    t_privacy_text = "We value your privacy. Uploaded PDF files are not stored on our servers; they are processed and cleared."
    t_privacy_title = "Terms of Service"
    t_terms_text = "By using this tool, you agree to use it for lawful purposes only."

# --- التنقل بين الصفحات ---

if "الرئيسية" in page:
    st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(t_upload, type="pdf", accept_multiple_files=True)
    
    if st.button(t_btn):
        if uploaded_files and len(uploaded_files) >= 2:
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            output = BytesIO()
            merger.write(output)
            st.success("Success!")
            st.download_button("Download", output.getvalue(), "merged.pdf", "application/pdf")
        else:
            st.warning("Please upload 2+ files")

elif "سياسة الخصوصية" in page:
    st.title(t_privacy_title)
    st.write(t_privacy_text)

elif "شروط" in page:
    st.title(t_terms_title)
    st.write(t_terms_text)

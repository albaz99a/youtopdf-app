import streamlit as st
from PyPDF2 import PdfMerger
from io import BytesIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="YouToPDF - Merge PDF", page_icon="📄", layout="centered")

# 2. خيار اللغة في الشريط الجانبي
language = st.sidebar.radio("Choose Language / اختر اللغة", ["العربية", "English"])

# 3. النصوص الاحترافية لسياسة الخصوصية والشروط
if language == "العربية":
    st.markdown("<style>.main {text-align: right; direction: rtl;} div.stButton > button {width: 100%; background-color: #ff4b4b; color: white;}</style>", unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - دمج ملفات PDF"
    t_desc = "الأداة الأسرع والأكثر أماناً لدمج ملفات PDF مجاناً."
    t_btn = "دمج وتحميل الملف الآن"
    
    t_about_h = "💡 عن YouToPDF"
    t_about_b = "YouToPDF هي أداة ويب بسيطة تهدف إلى مساعدة المستخدمين على إدارة مستنداتهم الرقمية دون تعقيد. نحن نركز على توفير تجربة مستخدم سريعة مع حماية كاملة للبيانات."
    
    t_privacy_h = "🔒 سياسة الخصوصية"
    t_privacy_b = "في YouToPDF، نضع خصوصية المستخدم على رأس أولوياتنا. نحن نلتزم بسياسة 'عدم الاحتفاظ بالبيانات'؛ حيث يتم دمج ملفات PDF المرفوعة ومعالجتها لحظياً داخل ذاكرة النظام المؤقتة (RAM). بمجرد إغلاق المتصفح، يتم مسح كافة البيانات نهائياً. نحن لا نطلع على محتوى ملفاتك، ولا نشارك بياناتك مع أي أطراف ثالثة."
    
    t_terms_h = "⚖️ شروط الخدمة"
    t_terms_b = "الأداة مقدمة مجاناً للاستخدام الشخصي والتجاري المشروعة فقط. يمنع منعاً باتاً استخدام الأداة لمعالجة ملفات تنتهك حقوق الملكية الفكرية. لا يتحمل الموقع أي مسؤولية عن فقدان البيانات الناتج عن أخطاء تقنية، واستخدام الأداة يتم على مسؤوليتك الشخصية."
    
    t_contact = "📧 اتصل بنا: support@youtopdf.com" # يمكنك تغيير البريد لإيميلك الحقيقي
else:
    st.markdown("<style>.main {text-align: left; direction: ltr;} div.stButton > button {width: 100%;}</style>", unsafe_allow_html=True)
    
    t_title = "📄 YouToPDF - PDF Merger"
    t_desc = "The fastest and most secure tool to merge PDF files for free."
    t_btn = "Merge and Download Now"
    
    t_about_h = "💡 About YouToPDF"
    t_about_b = "YouToPDF is a simple web tool built to help users manage digital documents without complexity. We focus on speed and total data protection."
    
    t_privacy_h = "🔒 Privacy Policy"
    t_privacy_b = "At YouToPDF, user privacy is our top priority. We adhere to a strict 'No-Data Retention' policy. All uploaded PDF files are processed in real-time within the system memory (RAM). Once the session ends, all data is permanently wiped. We do not access your file content nor share any data with third parties."
    
    t_terms_h = "⚖️ Terms of Service"
    t_terms_b = "This tool is provided free of charge for lawful personal and commercial use only. Use of this tool for content that violates intellectual property rights is prohibited. YouToPDF is not liable for any data loss due to technical errors."
    
    t_contact = "📧 Contact Us: support@youtopdf.com"

# --- عرض المحتوى ---
st.markdown(f"<h1 style='text-align: center;'>{t_title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>{t_desc}</p>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed")

if st.button(t_btn):
    if uploaded_files and len(uploaded_files) >= 2:
        merger = PdfMerger()
        for pdf in uploaded_files:
            merger.append(pdf)
        output = BytesIO()
        merger.write(output)
        st.success("Success!" if language == "English" else "تم الدمج!")
        st.download_button("Download", output.getvalue(), "merged.pdf", "application/pdf")

st.write("---")

# أقسام أدسنس القانونية
st.markdown(f"### {t_about_h}")
st.write(t_about_b)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"#### {t_privacy_h}")
    st.info(t_privacy_b)
with col2:
    st.markdown(f"#### {t_terms_h}")
    st.info(t_terms_b)

st.write("---")
st.markdown(f"<p style='text-align: center;'>{t_contact}</p>", unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="YouToPDF App", layout="wide")

# نضع كود الـ HTML والـ CSS الذي صممناه سابقاً داخل متغير نصي
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <style>
        /* أضف كود الـ CSS هنا */
        body { background-color: #f7f9fc; font-family: sans-serif; }
        .header { color: #e74c3c; font-weight: bold; font-size: 24px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; width: 150px; display: inline-block; margin: 10px; }
        .red-box { border: 2px solid #e74c3c; border-radius: 20px; padding: 20px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="header">YouToPDF</div>
    
    <div class="card">
        <h3>Merge PDF</h3>
        <p style="background:red; color:white; border-radius:4px;">Som PDF</p>
    </div>

    <div class="red-box">
        <h3>Footer container</h3>
        <p>About YouTDF: Professional PDF tools.</p>
    </div>
</body>
</html>
"""

# عرض كود HTML داخل تطبيق Streamlit
components.html(html_code, height=800, scrolling=True)

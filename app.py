import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتأخذ العرض الكامل
st.set_page_config(layout="wide")

# كود الواجهة (HTML + CSS)
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body { font-family: Arial, sans-serif; background-color: #f7f9fc; margin: 0; padding: 20px; }
        .logo { font-size: 24px; font-weight: bold; color: #444; margin-bottom: 20px; }
        .logo span { color: #e74c3c; }
        
        .grid-container { display: flex; gap: 15px; justify-content: center; margin-bottom: 30px; }
        .card { background: white; padding: 20px; border-radius: 10px; text-align: center; width: 150px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .card i { font-size: 40px; color: #555; margin-bottom: 10px; }
        .badge { background: #e74c3c; color: white; font-size: 12px; padding: 3px 10px; border-radius: 4px; }
        
        .main-form { background: white; padding: 30px; border-radius: 15px; max-width: 800px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .footer-box { border: 2px solid #e74c3c; border-radius: 20px; padding: 20px; max-width: 800px; margin: 20px auto; }
        .red-text { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <div class="logo"><i class="far fa-file-pdf" style="color:#e74c3c"></i> YouToPDF</div>
    
    <div class="grid-container">
        <div class="card"><i class="fas fa-file-import"></i><p>Merge PDF</p><span class="badge">Som PDF</span></div>
        <div class="card"><i class="fas fa-images"></i><p>Images to PDF</p><span class="badge" style="background:#e67e22">Split 19F</span></div>
        <div class="card"><i class="fas fa-project-diagram"></i><p>Tapsipño PDF</p><span class="badge">Slin PDF</span></div>
        <div class="card"><i class="fas fa-lock"></i><p>Protect PDF</p><span class="badge">Stn PDF</span></div>
        <div class="card"><i class="fas fa-stopwatch"></i><p>Compress PDF</p><span class="badge" style="background:#c0392b">Btn PDit</span></div>
    </div>

    <div class="main-form">
        <p><strong>active f "sactive</strong></p>
        <p style="color:#666; font-size:14px;">Upload PDF: Professional platform for accept multiple fitles Tute</p>
        <hr>
        <p>Upload PDF: <span style="background:#eee; padding:5px; border-radius:4px;">Range (e. al. 1-2)</span></p>
        <p>Passs word: <span style="background:#eee; padding:5px; border-radius:4px;">Range (e. 1-2)</span></p>
    </div>

    <div class="footer-box">
        <h3>"" Footer container</h3>
        <p><i class="fas fa-map-marker-alt"></i> <b>About</b> YouTDF: ... <span class="red-text">==s=pdff PDF"</span></p>
        <p><i class="fas fa-lock"></i> <b>Privacy:</b> No yetn tepuilt und lawhfuil osly.</p>
        <hr>
        <p style="font-size:12px; color:#999;">Footer container background colurtitfor, font size 122", margm natt, moto 15"</p>
    </div>
</body>
</html>
"""

# تنفيذ الكود وعرضه في التطبيق
components.html(html_content, height=1000, scrolling=True)

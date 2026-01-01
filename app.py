from flask import Flask, render_template_string

app = Flask(__name__)

# دمج تصميم HTML و CSS في متغير نصي واحد
html_template = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>YouToPDF - Professional Tools</title>
    <style>
        :root { --primary-red: #e74c3c; }
        body { font-family: sans-serif; background-color: #f1f3f5; margin: 0; padding: 40px; }
        .wrapper { max-width: 950px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 5px 25px rgba(0,0,0,0.05); }
        
        header { text-align: center; margin-bottom: 30px; }
        .logo { color: var(--primary-red); font-size: 38px; font-weight: bold; }
        
        .tools-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin: 30px 0; }
        .tool-card { border: 1px solid #eee; border-radius: 10px; padding: 20px; text-align: center; }
        .tool-btn { background: var(--primary-red); color: white; border: none; padding: 6px 15px; border-radius: 5px; font-size: 11px; cursor: pointer; }

        .action-box { border: 1px solid #ddd; border-radius: 15px; padding: 30px; margin: 30px 0; }
        .form-row { display: flex; align-items: center; margin-bottom: 15px; }
        .form-row label { width: 120px; font-size: 14px; }
        .form-row input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px; }
        
        .dl-btn { background: #2ecc71; color: white; border: none; padding: 12px 30px; border-radius: 6px; display: block; margin: 20px auto 0; font-weight: bold; cursor: pointer; }

        .footer-red { border: 2.5px solid var(--primary-red); border-radius: 25px; padding: 25px; margin-top: 50px; }
        .bottom-line { text-align: center; font-size: 11px; color: #aaa; margin-top: 30px; }
    </style>
</head>
<body>
<div class="wrapper">
    <header>
        <div class="logo">📄 YouToPDF</div>
        <p>"YouToPDF": Professional tools for secure PDF processing.</p>
    </header>

    <div class="tools-grid">
        <div class="tool-card"><h3>Merge PDF</h3><button class="tool-btn">Som PDF</button></div>
        <div class="tool-card"><h3>Images to PDF</h3><button class="tool-btn">Split 19F</button></div>
        <div class="tool-card"><h3>Extract PDF</h3><button class="tool-btn">Slm PDF</button></div>
        <div class="tool-card"><h3>Protect PDF</h3><button class="tool-btn">Stn PDF</button></div>
        <div class="tool-card"><h3>Compress PDF</h3><button class="tool-btn">Btn PDlt</button></div>
    </div>

    <div class="action-box">
        <h2>🛠 active function</h2>
        <div class="form-row">
            <label>Upload PDF</label>
            <input type="text" placeholder="Range (e.g. 1-2)">
        </div>
        <div class="form-row">
            <label>Password</label>
            <input type="password" placeholder="Enter password">
        </div>
        <button class="dl-btn">📤 Download Result</button>
    </div>

    <div class="footer-red">
        <p>📍 <strong>About:</strong> YouToPDF: Professional secure PDF tools.</p>
        <p>🔒 <strong>Privacy:</strong> All files are processed locally.</p>
        <p>✉️ <strong>Terms:</strong> support@youtopdf.com</p>
    </div>

    <div class="bottom-line">© 2026 Google AdSense</div>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    # استخدام render_template_string لعرض الكود المدمج
    return render_template_string(html_template)

if __name__ == '__main__':
    # تشغيل السيرفر
    app.run(debug=True)

body {
    font-family: Arial, sans-serif;
    background-color: #f7f9fc;
    color: #333;
    margin: 0;
    padding: 20px;
}

header {
    max-width: 900px;
    margin: 0 auto;
}

.header-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    color: #444;
}

.lang-btn {
    border: 1px solid #ddd;
    background: white;
    padding: 5px 15px;
    border-radius: 4px;
    cursor: pointer;
}

.active-lang {
    background: #fdeaea;
    color: #e74c3c;
    border-color: #fdeaea;
}

.sub-header {
    margin-top: 20px;
    display: flex;
    gap: 10px;
}

.style-tag {
    background: #e1ecf4;
    color: #39739d;
    padding: 2px 8px;
    border-radius: 4px;
}

.intro-text {
    font-size: 14px;
    color: #555;
    margin-top: 15px;
}

.grid-container {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 30px;
    flex-wrap: wrap;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    text-align: center;
    width: 140px;
}

.card h3 {
    font-size: 14px;
    margin: 15px 0;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 4px;
    color: white;
    font-size: 12px;
}

.red { background-color: #e74c3c; }
.orange { background-color: #e67e22; }
.dark-red { background-color: #c0392b; }

.dots {
    text-align: center;
    font-size: 24px;
    color: #ccc;
    margin: 20px 0;
}

.active-section {
    background: white;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.form-group, .form-group-btn {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    border-bottom: 1px solid #eee;
    padding-bottom: 5px;
}

.form-group label, .form-group-btn label {
    width: 100px;
    font-size: 14px;
}

.form-group input {
    border: none;
    background: #f1f3f4;
    padding: 8px;
    width: 100%;
    border-radius: 4px;
}

.download-btn {
    background: #f1f3f4;
    border: 1px solid #ccc;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
}

.footer-container {
    border: 2px solid #e74c3c;
    border-radius: 20px;
    margin: 30px auto;
    max-width: 800px;
    padding: 20px;
}

.footer-container ul {
    list-style: none;
    padding: 0;
}

.footer-container li {
    margin-bottom: 10px;
    font-size: 14px;
}

.highlight-red {
    color: #e74c3c;
    font-weight: bold;
}

footer {
    text-align: center;
    font-size: 12px;
    color: #888;
    margin-top: 40px;
}


<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Clone</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <nav class="github-nav">
        <div class="nav-left">
            <i class="fab fa-github fa-2x"></i>
            <div class="search-container">
                <input type="text" placeholder="البحث أو الانتقال إلى...">
                <span class="search-slash">/</span>
            </div>
            <ul class="nav-links">
                <li>Pull requests</li>
                <li>Issues</li>
                <li>Marketplace</li>
                <li>Explore</li>
            </ul>
        </div>
        <div class="nav-right">
            <i class="far fa-bell"></i>
            <i class="fas fa-plus"></i>
            <img src="https://via.placeholder.com/20" alt="Avatar" class="avatar">
        </div>
    </nav>

    <main class="container">
        <div class="repo-list">
            <div class="repo-header">
                <h2>المستودعات الأخيرة</h2>
                <button class="btn-new">جديد</button>
            </div>
            
            <div class="repo-item">
                <a href="#" class="repo-name">my-awesome-project</a>
                <span class="status">Public</span>
                <p class="repo-desc">هذا وصف لمشروع برمجي يحاكي واجهة جيت هاب.</p>
                <div class="repo-meta">
                    <span><i class="fas fa-circle" style="color: #f1e05a;"></i> JavaScript</span>
                    <span><i class="far fa-star"></i> 124</span>
                </div>
            </div>

            <div class="repo-item">
                <a href="#" class="repo-name">portfolio-design</a>
                <span class="status">Public</span>
                <div class="repo-meta">
                    <span><i class="fas fa-circle" style="color: #e34c26;"></i> HTML</span>
                    <span><i class="far fa-star"></i> 45</span>
                </div>
            </div>
        </div>
    </main>

</body>
</html>

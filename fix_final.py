import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the Logout button on Ban screen
old_btn = '<button onclick="localStorage.clear(); location.reload();" style="margin-top:20px;padding:10px 20px;background:#ff4d4d;border:none;border-radius:10px;color:#fff;font-weight:bold;">Logout</button>'
new_btn = '<button onclick="auth.signOut(); location.reload();" style="margin-top:20px;padding:10px 20px;background:#ff4d4d;border:none;border-radius:10px;color:#fff;font-weight:bold;">Logout</button>'
html = html.replace(old_btn, new_btn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Logout button fixed!")

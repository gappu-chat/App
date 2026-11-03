import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the Auth (Login) page HTML
old_auth = re.search(r'<div class="w" id="auth">.*?<div class="msg" id="authMsg"></div>\s*</div>', html, re.DOTALL)
if old_auth:
    new_auth = """<div class="w" id="auth" style="display:flex; flex-direction:column; justify-content:center; min-height:80vh;">
  <div style="text-align:center; margin-bottom:30px;">
    <div style="font-size:4rem; line-height:1; margin-bottom:10px;">💬</div>
    <h1 style="font-size:2.5rem; margin:0; color:var(--acc);">Gappu Chat</h1>
    <p style="color:var(--dim); font-size:1.1rem; margin-top:8px;">Baatein karo, Game khelo, Dost banao</p>
  </div>
  
  <div class="tabs" style="background:var(--card); padding:5px; border-radius:16px; border:1px solid var(--line);">
    <button id="tabLogin" class="on" style="margin:0; border-radius:12px;">Login</button>
    <button id="tabSignup" style="margin:0; border-radius:12px;">Naya Account</button>
  </div>

  <div style="background:var(--card); padding:20px; border-radius:20px; border:1px solid var(--line); margin-top:15px;">
    <input id="email" type="email" placeholder="Email Address" autocomplete="email" style="background:var(--bg); border:1px solid var(--line);">
    <input id="pass" type="password" placeholder="Password" autocomplete="current-password" style="background:var(--bg); border:1px solid var(--line); margin-bottom:20px;">
    <button id="go" style="border-radius:12px; padding:14px; font-size:1.1rem;">Login karo</button>
    <div class="msg" id="authMsg" style="margin-bottom:0;"></div>
  </div>

  <div style="display:flex; align-items:center; margin:20px 0;">
    <hr style="flex:1; border:0; border-top:1px solid var(--line);">
    <span style="padding:0 10px; color:var(--dim); font-size:0.9rem;">YA FIR</span>
    <hr style="flex:1; border:0; border-top:1px solid var(--line);">
  </div>

  <button id="guestBtn" class="alt" style="border-radius:12px; padding:14px; border-color:var(--dim); color:var(--ink); display:flex; align-items:center; justify-content:center; gap:8px;">
    <span>👤</span> Guest ban ke khelo
  </button>
</div>"""
    html = html.replace(old_auth.group(0), new_auth)

# 2. Update the Chat list empty state (remove test IDs)
html = html.replace("nochat:'Abhi koi chat nahi. Upar dost ki ID search karo.',hint:'Test IDs: aman_demo, priya_demo, rohan_demo'", "nochat:'Abhi koi chat nahi hai. Upar search karke dost se baat karo.',hint:''")
html = html.replace("nochat:'No chats yet.',hint:'Demo IDs: aman_demo, priya_demo, rohan_demo'", "nochat:'No chats yet. Search a friend above.',hint:''")

# 3. Hide the hint element if empty
html = html.replace("box.appendChild(el('div', 'empty', t('hint')));", "if(t('hint')) box.appendChild(el('div', 'empty', t('hint')));")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Design updated successfully!")

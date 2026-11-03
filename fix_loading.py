import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Loading Screen HTML just after <body>
loading_html = """
<div id="loadingScreen" style="position:fixed; inset:0; z-index:9999; background:var(--bg); display:flex; flex-direction:column; align-items:center; justify-content:center; color:var(--acc);">
  <div style="font-size:4rem; margin-bottom:20px; animation:pulse 1.5s infinite;">💬</div>
  <h2 style="color:var(--acc); margin:0;">Gappu Chat</h2>
  <p style="color:var(--dim); margin-top:10px;">Loading...</p>
</div>
<style>
@keyframes pulse { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.1); opacity: 0.7; } 100% { transform: scale(1); opacity: 1; } }
</style>
"""
html = html.replace('<body>', '<body>\n' + loading_html)

# 2. Hide auth and app screens initially
html = html.replace('<div class="w" id="auth">', '<div class="w hidden" id="auth">')
# Remove hidden from app if it's there, we will control it via JS
html = html.replace('<div class="w hidden" id="app">', '<div class="w hidden" id="app">')

# 3. Update onAuthStateChanged to hide loading screen
old_auth_state = """auth.onAuthStateChanged(async user => {
  [listRef, blkRef, presenceRef, mref, typingRef, presenceListenRef, seenListenRef].forEach(r => r && r.off()); 
  listRef = blkRef = presenceRef = mref = typingRef = presenceListenRef = seenListenRef = null;
  closeChat(); closeSheet();
  me = user; prof = null; chats = {}; blocked = {};
  if (!user) { screen('auth'); return; }"""

new_auth_state = """auth.onAuthStateChanged(async user => {
  [listRef, blkRef, presenceRef, mref, typingRef, presenceListenRef, seenListenRef].forEach(r => r && r.off()); 
  listRef = blkRef = presenceRef = mref = typingRef = presenceListenRef = seenListenRef = null;
  closeChat(); closeSheet();
  me = user; prof = null; chats = {}; blocked = {};
  
  // Hide loading screen after auth check
  setTimeout(() => {
      const ls = document.getElementById('loadingScreen');
      if (ls) ls.style.display = 'none';
  }, 800);

  if (!user) { screen('auth'); return; }"""

html = html.replace(old_auth_state, new_auth_state)

# 4. Make sure screen() function handles everything correctly
old_screen = """function screen(id) { ['auth','claim','app'].forEach(x => $(x).classList.toggle('hidden', x !== id)); $('chat').classList.add('hidden'); }"""
new_screen = """function screen(id) { 
  ['auth','claim','app'].forEach(x => $(x).classList.toggle('hidden', x !== id)); 
  $('chat').classList.add('hidden'); 
}"""
html = html.replace(old_screen, new_screen)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Redirect bug fixed with Loading Screen!")

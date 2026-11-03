import re

# --- 1. Update index.html for Chat Ban ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Ban check in enterApp
old_enter = """function enterApp() {
  screen('app'); applyTheme(); applyI18n(); showTab('Chats'); renderMe(); renderGames();
  if(!notifReqDone) { requestNotifPermission(); notifReqDone = true; }"""

new_enter = """function enterApp() {
  // BAN CHECK
  if (prof.banned) {
     if (prof.banType === '7days' && prof.banUntil && Date.now() > prof.banUntil) {
         // Temporary ban expired, auto-unban
         db.ref('profiles/' + me.uid).update({ banned: null, banType: null, banUntil: null });
         prof.banned = null;
     } else if (prof.banType !== 'game') {
         // Permanent or active temporary ban
         const banScreen = document.createElement('div');
         banScreen.style.cssText = 'position:fixed;inset:0;background:#1a0000;color:#ff4d4d;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px;';
         banScreen.innerHTML = '<h1 style="font-size:3rem;">⛔</h1><h2>Account Banned</h2><p>Aapko rule todne ke liye ban kar diya gaya hai.</p><p style="font-size:0.8rem;opacity:0.7;">Contact Admin for help.</p><button onclick="localStorage.clear(); location.reload();" style="margin-top:20px;padding:10px 20px;background:#ff4d4d;border:none;border-radius:10px;color:#fff;font-weight:bold;">Logout</button>';
         document.body.appendChild(banScreen);
         return;
     }
  }

  screen('app'); applyTheme(); applyI18n(); showTab('Chats'); renderMe(); renderGames();
  if(!notifReqDone) { requestNotifPermission(); notifReqDone = true; }"""
html = html.replace(old_enter, new_enter)

# Add Game Ban check in renderGames
html = html.replace("""function renderGames() {
  const b = $('gameBox'); b.innerHTML = '';""", """function renderGames() {
  const b = $('gameBox'); b.innerHTML = '';
  
  if (prof.banType === 'game') {
      b.innerHTML = '<div style="text-align:center; color:var(--danger); margin-top:50px;"><h2>🎮 Game Banned</h2><p>Aapko games khelne se ban kar diya gaya hai.</p></div>';
      return;
  }""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# --- 2. Update Games for Game Ban (Backend Security) ---
for filename in ['snake_ladder.html', 'quiz.html', 'ludo.html', 'match.html']:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            g_html = f.read()
            
        # Add ban check right after profile fetch
        old_auth = """  const s = await db.ref('profiles/' + me.uid).once('value');
  if (s.exists()) {"""
        new_auth = """  const s = await db.ref('profiles/' + me.uid).once('value');
  if (s.exists()) {
      const checkProf = s.val();
      if (checkProf.banned && checkProf.banType === 'game') {
          document.body.innerHTML = '<div style="text-align:center; color:#e74c3c; margin-top:50px; font-family:sans-serif;"><h1>⛔ BANNED</h1><p>Aapko games khelne se ban kar diya gaya hai.</p><a href="index.html" style="color:#e0b04a;">← Wapas jao</a></div>';
          return;
      }
      if (checkProf.banned && (checkProf.banType === 'permanent' || (checkProf.banType === '7days' && Date.now() < checkProf.banUntil))) {
          window.location.href = 'index.html'; // Redirect to main to show ban screen
          return;
      }"""
        
        g_html = g_html.replace(old_auth, new_auth)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(g_html)
    except FileNotFoundError:
        pass

print("Strict Ban System added to Chat and all Games!")

import re

# --- 1. Fix Welcome Bonus (300 Coins) in index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Claim (Signup) logic to give 300 coins
html = html.replace("prof = { name, username: un, city, coins: 0, gamesWon: 0, guest: me.isAnonymous };", "prof = { name, username: un, city, coins: 300, gamesWon: 0, guest: me.isAnonymous };")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# --- 2. Fix Game Ban and Coins in Ludo (ludo.html) ---
with open('ludo.html', 'r', encoding='utf-8') as f:
    ludo = f.read()

# Add 300 Coins Check and Game Ban Check in Ludo
old_ludo_auth = """auth.onAuthStateChanged(async user => {
  if(!user) { window.location.href='index.html'; return; }
  me = user;
  const s = await db.ref('profiles/'+me.uid).once('value');
  if(s.exists()) { prof = s.val(); initGame(); }
});"""

new_ludo_auth = """auth.onAuthStateChanged(async user => {
  if(!user) { window.location.href='index.html'; return; }
  me = user;
  const s = await db.ref('profiles/'+me.uid).once('value');
  if(s.exists()) { 
      prof = s.val(); 
      if(prof.banned && prof.banType === 'game') {
          document.body.innerHTML = '<div style="text-align:center; color:#e74c3c; margin-top:50px; font-family:sans-serif;"><h1>⛔ BANNED</h1><p>Aapko games khelne se ban kar diya gaya hai.</p><a href="index.html" style="color:#e0b04a;">← Wapas jao</a></div>';
          return;
      }
      if((prof.coins || 0) < 50) {
          alert('Game khelne ke liye kam se kam 50 Coins chahiye!');
          window.location.href='index.html'; return;
      }
      initGame(); 
  }
});"""
ludo = ludo.replace(old_ludo_auth, new_ludo_auth)

# Deduct 50 Coins on Ludo Start and Save History
old_ludo_start = """  if(!snap.exists()) {
     await gameRef.set({
        status: 'waiting', admin: me.uid, turn: null, turnStart: Date.now(),
        players: { [me.uid]: { name: prof.name, color: 'red', tokens: [0,0,0,0] } }
     });
  } else {"""
new_ludo_start = """  if(!snap.exists()) {
     await gameRef.set({
        status: 'waiting', admin: me.uid, turn: null, turnStart: Date.now(),
        players: { [me.uid]: { name: prof.name, color: 'red', tokens: [0,0,0,0] } }
     });
     // Deduct entry fee for admin
     db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(-50));
  } else {"""
ludo = ludo.replace(old_ludo_start, new_ludo_start)

# Save Ludo History on start
ludo = ludo.replace("gameRef = db.ref('ludo_new_games/' + curGid);", "gameRef = db.ref('ludo_new_games/' + curGid);\n  db.ref('ludo_history').push({ gid: curGid, ts: Date.now() });")

with open('ludo.html', 'w', encoding='utf-8') as f:
    f.write(ludo)

# --- 3. Fix Admin Panel Live Games and Ludo Search ---
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Add Ludo to Live Games
old_live = """  // Fetch Quiz Games
  const qzSnap = await db.ref('quiz_games').orderByChild('status').equalTo('playing').once('value');
  qzSnap.forEach(c => liveGames.push({ type: 'Quiz', gid: c.key, ...c.val() }));"""
new_live = """  // Fetch Quiz Games
  const qzSnap = await db.ref('quiz_games').orderByChild('status').equalTo('playing').once('value');
  qzSnap.forEach(c => liveGames.push({ type: 'Quiz', gid: c.key, ...c.val() }));

  // Fetch Ludo Games
  const luSnap = await db.ref('ludo_new_games').orderByChild('status').equalTo('playing').once('value');
  luSnap.forEach(c => liveGames.push({ type: 'Ludo', gid: c.key, ...c.val() }));"""
admin = admin.replace(old_live, new_live)

# Add Ludo to Game Search
old_search = """  if(!s.exists()) {
      s = await db.ref('ludo_new_games/' + gid).once('value');
      gameType = 'Ludo';
  }"""
if old_search not in admin:
    # If it was already added previously, just ensure it's there
    admin = admin.replace("let s = await db.ref('sl_games/' + gid).once('value');", "let s = await db.ref('sl_games/' + gid).once('value');")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("Welcome Bonus, Ludo Start, and Admin Live Search fixed!")

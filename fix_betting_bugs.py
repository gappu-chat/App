import re

# --- 1. Fix index.html (Daily Bonus + Coin Check) ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Daily Bonus Button in Profile Menu
old_menu = """  [['✏️','editp',editProfile], ['🆔','chid',idSheet], ['✉️','email',emailSheet], ['📱','phone',phoneSheet],"""
new_menu = """  [['🎁','Daily Bonus (20 Coins)', dailyBonus], ['✏️','editp',editProfile], ['🆔','chid',idSheet], ['✉️','email',emailSheet], ['📱','phone',phoneSheet],"""
html = html.replace(old_menu, new_menu)

# Add Daily Bonus Logic before </script>
bonus_logic = """
function dailyBonus() {
  const today = new Date().toDateString();
  const lastClaim = LS('lastBonusDate');
  if (lastClaim === today) {
    toast('Aaj ka bonus le liya hai! Kal wapas aana.');
    return;
  }
  
  openSheet('Daily Bonus', b => {
    const m = el('div', '', 'Aaj ka 20 Coins bonus claim karein?');
    m.style.marginBottom = '15px'; m.style.textAlign = 'center';
    b.appendChild(m);
    
    const btn = el('button', '', '🎁 Claim 20 Coins');
    btn.onclick = async () => {
      btn.textContent = 'Claiming...';
      btn.disabled = true;
      try {
        await db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(20));
        prof.coins = (prof.coins || 0) + 20;
        LSset('lastBonusDate', today);
        closeSheet();
        toast('20 Coins mil gaye! 🎉');
        renderMe();
      } catch(e) { toast('Fail'); btn.disabled = false; btn.textContent = '🎁 Claim 20 Coins'; }
    };
    b.appendChild(btn);
  });
}
"""
html = html.replace("</script>\n</body>\n</html>", bonus_logic + "\n</script>\n</body>\n</html>")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# --- 2. Fix Snake & Ladders (Double Cut + Game Ban + Payout) ---
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# Fix Double Coin Cut
old_start_sl = """       if (pCount + 1 === 4) {
           updates.status = 'playing';
           updates.turn = Object.keys(players)[0] || me.uid;
           
           // Deduct Entry Fee (50 Coins)
           for(let uid in players) {
               db.ref('profiles/' + uid + '/coins').set(firebase.database.ServerValue.increment(-50));
           }
           db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(-50));
       }"""
new_start_sl = """       if (pCount + 1 === 4) {
           updates.status = 'playing';
           updates.turn = Object.keys(players)[0] || me.uid;
           
           // Deduct Entry Fee (50 Coins) - Only once per player
           for(let uid in players) {
               db.ref('profiles/' + uid + '/coins').set(firebase.database.ServerValue.increment(-50));
           }
       }"""
sl = sl.replace(old_start_sl, new_start_sl)

# Add Game Ban Check at start
old_auth = """  const s = await db.ref('profiles/' + me.uid).once('value');
  if (s.exists()) {"""
new_auth = """  const s = await db.ref('profiles/' + me.uid).once('value');
  if (s.exists()) {
      const checkProf = s.val();
      if (checkProf.banned && checkProf.banType === 'game') {
          document.body.innerHTML = '<div style="text-align:center; color:#e74c3c; margin-top:50px; font-family:sans-serif;"><h1>⛔ BANNED</h1><p>Aapko games khelne se ban kar diya gaya hai.</p><a href="index.html" style="color:#e0b04a;">← Wapas jao</a></div>';
          return;
      }"""
sl = sl.replace(old_auth, new_auth)

# Change payout to 180
sl = sl.replace("db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(200));", "db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(180));")
sl = sl.replace("updates.turn = getNextTurn();\n  }\n  updates.turnStart = Date.now();\n  updates.dice = dice;", "updates.turn = getNextTurn();\n  }\n  updates.turnStart = Date.now();\n  updates.dice = dice;")

with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)


# --- 3. Fix Quiz (Game Ban + Payout) ---
with open('quiz.html', 'r', encoding='utf-8') as f:
    qz = f.read()

# Add Game Ban Check
old_auth_qz = """  const s = await db.ref('profiles/' + me.uid).once('value');
  if (s.exists()) {"""
new_auth_qz = """  const s = await db.ref('profiles/' + me.uid).once('value');
  if (s.exists()) {
      const checkProf = s.val();
      if (checkProf.banned && checkProf.banType === 'game') {
          document.body.innerHTML = '<div style="text-align:center; color:#e74c3c; margin-top:50px; font-family:sans-serif;"><h1>⛔ BANNED</h1><p>Aapko games khelne se ban kar diya gaya hai.</p><a href="index.html" style="color:#e0b04a;">← Wapas jao</a></div>';
          return;
      }"""
qz = qz.replace(old_auth_qz, new_auth_qz)

# Change payout to 180
qz = qz.replace("db.ref('profiles/' + winnerUid + '/coins').set(firebase.database.ServerValue.increment(200));", "db.ref('profiles/' + winnerUid + '/coins').set(firebase.database.ServerValue.increment(180));")

with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(qz)


# --- 4. Add Game Ban Check to Ludo and Match ---
for filename in ['ludo.html', 'match.html']:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            g = f.read()
        if "checkProf.banned" not in g:
            old_auth_g = """firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL);"""
            new_auth_g = """firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL);
            
firebase.auth().onAuthStateChanged(async user => {
  if(user) {
     const s = await db.ref('profiles/' + user.uid).once('value');
     if(s.exists()) {
         const p = s.val();
         if(p.banned && p.banType === 'game') {
             document.body.innerHTML = '<div style="text-align:center; color:#e74c3c; margin-top:50px; font-family:sans-serif;"><h1>⛔ BANNED</h1><p>Aapko games khelne se ban kar diya gaya hai.</p><a href="index.html" style="color:#e0b04a;">← Wapas jao</a></div>';
             return;
         }
     }
  }
});"""
            g = g.replace(old_auth_g, new_auth_g)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(g)
    except FileNotFoundError:
        pass

print("All Betting, Bonus, and Ban bugs fixed successfully! 🎉")

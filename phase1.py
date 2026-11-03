import re

# --- 1. Update index.html ---
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add City input to claim screen
html = html.replace('<input id="cun" placeholder="User ID (a-z, 0-9, _ , 3 se 15)" maxlength="15" autocapitalize="none">', '<input id="cun" placeholder="User ID (a-z, 0-9, _ , 3 se 15)" maxlength="15" autocapitalize="none">\n  <input id="ccity" placeholder="Tumhara Shehar (City)" maxlength="20">')

# Update claim logic to save city and default coins/wins
html = html.replace("const name = $('cname').value.trim(), un = $('cun').value.trim().toLowerCase();", "const name = $('cname').value.trim(), un = $('cun').value.trim().toLowerCase(), city = $('ccity').value.trim() || 'Unknown';")
html = html.replace("prof = { name, username: un, guest: me.isAnonymous };", "prof = { name, username: un, city, coins: 0, gamesWon: 0, guest: me.isAnonymous };")

# Update Profile display to show City, Coins, Games Won
old_profile_card = """card.appendChild(av); card.appendChild(el('div', 'big', prof.name)); card.appendChild(el('div', 'dim', '@' + prof.username));
  b.appendChild(card);"""
new_profile_card = """card.appendChild(av); card.appendChild(el('div', 'big', prof.name)); card.appendChild(el('div', 'dim', '@' + prof.username));
  card.appendChild(el('div', 'dim', '📍 ' + (prof.city || 'City not set')));
  const stats = el('div', '', `🪙 ${prof.coins || 0} Coins  |  🏆 ${prof.gamesWon || 0} Wins`);
  stats.style.marginTop = '8px'; stats.style.color = 'var(--acc)'; stats.style.fontWeight = 'bold';
  card.appendChild(stats);
  b.appendChild(card);"""
html = html.replace(old_profile_card, new_profile_card)

# Add City edit in profile settings
html = html.replace("const n = inp(t('name'), prof.name); n.maxLength = 20; const m = el('div', 'msg');\n    b.appendChild(n);", "const n = inp(t('name'), prof.name); n.maxLength = 20; const c = inp('Shehar (City)', prof.city || ''); c.maxLength = 20; const m = el('div', 'msg');\n    b.appendChild(n); b.appendChild(c);")
html = html.replace("const v = n.value.trim(); if (!v) return;", "const v = n.value.trim(), city = c.value.trim(); if (!v) return;")
html = html.replace("await db.ref('profiles/' + me.uid + '/name').set(v); prof.name = v; renderMe(); m.textContent = t('done');", "await db.ref('profiles/' + me.uid).update({ name: v, city: city || 'Unknown' }); prof.name = v; prof.city = city; renderMe(); m.textContent = t('done');")

# Remove Tap Tycoon from Games list
html = re.sub(r"\[\'🍵\', \'Tap Tycoon\', \'g1\', true, \'linear-gradient.*?\],\n?", "", html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# --- 2. Update snake_ladder.html ---
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# Add coins and wins on victory
old_win_sl = """     updates.status = 'finished';
     updates.winner = me.uid;
     updates.finishedAt = Date.now();
     db.ref('sl_history').push({"""
new_win_sl = """     updates.status = 'finished';
     updates.winner = me.uid;
     updates.finishedAt = Date.now();
     
     // Give Rewards
     db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(100));
     db.ref('profiles/' + me.uid + '/gamesWon').set(firebase.database.ServerValue.increment(1));
     
     db.ref('sl_history').push({"""
sl = sl.replace(old_win_sl, new_win_sl)

with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)

# --- 3. Update quiz.html ---
with open('quiz.html', 'r', encoding='utf-8') as f:
    qz = f.read()

# Add coins and wins on victory in Quiz
old_win_qz = """   if (nextQ >= QUIZ_DATA.length) {
       await gameRef.update({ status: 'finished' });
       // Save history
       db.ref('quiz_history').push({"""
new_win_qz = """   if (nextQ >= QUIZ_DATA.length) {
       await gameRef.update({ status: 'finished' });
       
       // Find winner and give rewards
       let winnerUid = null;
       let maxScore = -1;
       for (const uid in gameData.players) {
           if (gameData.players[uid].score > maxScore) {
               maxScore = gameData.players[uid].score;
               winnerUid = uid;
           }
       }
       if (winnerUid) {
           db.ref('profiles/' + winnerUid + '/coins').set(firebase.database.ServerValue.increment(100));
           db.ref('profiles/' + winnerUid + '/gamesWon').set(firebase.database.ServerValue.increment(1));
       }
       
       // Save history
       db.ref('quiz_history').push({"""
qz = qz.replace(old_win_qz, new_win_qz)

with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(qz)

print("Phase 1 Complete! City, Coins, and Rewards system added. Tap Tycoon removed.")

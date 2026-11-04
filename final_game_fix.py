import re

# --- 1. Fix Snake & Ladders (Coins Add + New Game Button + History) ---
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# Fix Coin Addition Logic (using Transaction for safety)
old_win_sl = """     // Give Rewards (200 Coins for Winner)
     db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(200));"""
new_win_sl = """     // Give Rewards (180 Coins for Winner)
     db.ref('profiles/' + me.uid + '/coins').transaction(c => (c || 0) + 180);
     db.ref('profiles/' + me.uid + '/gamesWon').transaction(c => (c || 0) + 1);"""
sl = sl.replace(old_win_sl, new_win_sl)

# Add Game Over UI with Restart Button
old_winner_ui = """  if (winner) {
    $('turnTxt').textContent = "🏆 " + winner.name + " Jeet Gaya!";
    $('turnTxt').style.color = "#2ecc71";
    $('rollBtn').disabled = true;
    clearInterval(turnInterval);
    $('timerTxt').textContent = '';
    return;
  }"""
new_winner_ui = """  if (winner) {
    $('turnTxt').textContent = "🏆 " + winner.name + " Jeet Gaya!";
    $('turnTxt').style.color = "#2ecc71";
    $('rollBtn').disabled = true;
    clearInterval(turnInterval);
    $('timerTxt').textContent = '';
    
    // Show Restart Button
    if(!document.getElementById('restartBtn')) {
       const btn = document.createElement('button');
       btn.id = 'restartBtn';
       btn.className = 'alt';
       btn.textContent = '🔄 Naya Game Khelo';
       btn.style.marginTop = '10px';
       btn.style.width = '100%';
       btn.onclick = () => window.location.href = 'snake_ladder.html';
       $('msgs').parentElement.appendChild(btn);
    }
    return;
  }"""
sl = sl.replace(old_winner_ui, new_winner_ui)
with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)

# --- 2. Fix Quiz (Coins Add + New Game Button) ---
with open('quiz.html', 'r', encoding='utf-8') as f:
    qz = f.read()

# Fix Coin addition in Quiz
old_win_qz = """       if (winnerUid) {
           db.ref('profiles/' + winnerUid + '/coins').set(firebase.database.ServerValue.increment(100));"""
new_win_qz = """       if (winnerUid) {
           db.ref('profiles/' + winnerUid + '/coins').transaction(c => (c || 0) + 180);"""
qz = qz.replace(old_win_qz, new_win_qz)

# Add Restart Button in Quiz Game Over
old_quiz_over = """  } else if (status === 'finished') {
     $('timerTxt').textContent = '';
     const winner = Object.keys(gameData.players).reduce((a, b) => gameData.players[a].score > gameData.players[b].score ? a : b);
     $('questionText').textContent = "🏆 " + gameData.players[winner].name + " Jeeta!";
     $('optionsBox').innerHTML = '';
     $('hostControls').classList.add('hidden');
  }"""
new_quiz_over = """  } else if (status === 'finished') {
     $('timerTxt').textContent = '';
     const winner = Object.keys(gameData.players).reduce((a, b) => gameData.players[a].score > gameData.players[b].score ? a : b);
     $('questionText').textContent = "🏆 " + gameData.players[winner].name + " Jeeta!";
     $('optionsBox').innerHTML = '';
     $('hostControls').classList.add('hidden');
     
     if(!document.getElementById('restartBtn')) {
       const btn = document.createElement('button');
       btn.id = 'restartBtn';
       btn.className = 'alt';
       btn.textContent = '🔄 Naya Game Khelo';
       btn.style.marginTop = '20px';
       btn.onclick = () => window.location.href = 'quiz.html';
       $('optionsBox').appendChild(btn);
     }
  }"""
qz = qz.replace(old_quiz_over, new_quiz_over)
with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(qz)

# --- 3. Fix Admin Panel Live & Search for Ludo ---
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Add Ludo to live games fetch
if "ludo_new_games" not in admin:
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

# Fix Game Search to include Ludo
if "ludo_new_games" not in admin:
    old_search = """  const s = await db.ref('sl_games/' + gid).once('value');
  if(!s.exists()) { box.innerHTML = '<p class="dim">Game ID not found in Snakes & Ladders.</p>'; return; }"""
    new_search = """  let s = await db.ref('sl_games/' + gid).once('value');
  let gameType = 'Snake';
  if(!s.exists()) {
      s = await db.ref('quiz_games/' + gid).once('value');
      gameType = 'Quiz';
  }
  if(!s.exists()) {
      s = await db.ref('ludo_new_games/' + gid).once('value');
      gameType = 'Ludo';
  }
  if(!s.exists()) { box.innerHTML = '<p class="dim">Game ID not found.</p>'; return; }"""
    admin = admin.replace(old_search, new_search)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)

print("Fixed Coins, Restart Buttons, and Ludo Admin Search!")

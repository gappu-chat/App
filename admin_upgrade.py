import re

# --- 1. Update Admin Panel (Premium UI + Game History) ---
with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# Fix Tabs UI (Scrollable)
admin = admin.replace(".tabs{display:flex;gap:8px;margin-bottom:15px;overflow-x:auto;padding-bottom:5px}", ".tabs{display:flex;gap:8px;margin-bottom:15px;overflow-x:auto;white-space:nowrap;padding-bottom:5px}")
admin = admin.replace(".tabs button{margin:0;white-space:nowrap;width:auto;padding:8px 16px;font-size:0.9rem}", ".tabs button{margin:0;width:auto;padding:8px 16px;font-size:0.9rem;flex-shrink:0}")

# Add Game History Tab
admin = admin.replace('<button id="tabGames">🎮 Games</button>', '<button id="tabHistory">📜 History</button>\n    <button id="tabGames">🎮 Search Game</button>')

# Add Game History View
admin = admin.replace('<div id="vGames" class="hidden">', """<div id="vHistory" class="hidden">
    <div id="historyList"></div>
  </div>
  <div id="vGames" class="hidden">""")

# Update Tab Logic
admin = admin.replace("['Dash', 'Users', 'Reports', 'Games'].forEach", "['Dash', 'Users', 'Reports', 'History', 'Games'].forEach")
admin = admin.replace("$('tabGames').onclick = () => showTab('Games');", """$('tabHistory').onclick = () => { showTab('History'); loadGameHistory(); };
$('tabGames').onclick = () => showTab('Games');""")

# Add Game History Loader Logic
history_js = """
async function loadGameHistory() {
  const box = $('historyList'); box.innerHTML = 'Loading...';
  
  // Fetch recent 50 games from both SL and Quiz
  const slSnap = await db.ref('sl_history').limitToLast(50).once('value');
  const qzSnap = await db.ref('quiz_history').limitToLast(50).once('value');
  
  let games = [];
  slSnap.forEach(c => games.push({ type: 'Snake', ...c.val() }));
  qzSnap.forEach(c => games.push({ type: 'Quiz', ...c.val() }));
  
  // Sort by timestamp (newest first)
  games.sort((a, b) => (b.ts || 0) - (a.ts || 0));
  
  box.innerHTML = '';
  if(games.length === 0) { box.innerHTML = '<p class="dim">No games played yet.</p>'; return; }
  
  games.forEach(g => {
    const row = document.createElement('div');
    row.className = 'row';
    row.innerHTML = `
      <div>
        <b style="color:var(--acc);">${g.type} Game</b><br>
        <small class="dim">GID: ${g.gid}</small><br>
        <small class="dim">Winner: ${g.winner}</small><br>
        <small class="dim">Time: ${new Date(g.ts).toLocaleString()}</small>
      </div>
      <button class="sm" onclick="viewGameDetails('${g.type}', '${g.gid}')">View</button>
    `;
    box.appendChild(row);
  });
}

window.viewGameDetails = async (type, gid) => {
  const ref = type === 'Snake' ? 'sl_games/' + gid : 'quiz_games/' + gid;
  const snap = await db.ref(ref).once('value');
  if(!snap.exists()) return alert('Game data deleted from database!');
  
  const g = snap.val();
  let html = `<b>Game Type:</b> ${type}<br><b>Game ID:</b> ${gid}<br><b>Status:</b> ${g.status}<br><br><b>Players:</b><br>`;
  
  if(g.players) {
     for(const uid in g.players) {
       html += `- ${g.players[uid].name}`;
       if(type==='Quiz') html += ` (Score: ${g.players[uid].score})`;
       else html += ` (Pos: ${g.players[uid].pos})`;
       html += `<br>`;
     }
  }
  $('gameResult').innerHTML = `<div class="card">${html}</div>`;
  showTab('Games');
  $('searchGameId').value = gid;
};
"""
admin = admin.replace("// --- Game Search Logic ---", history_js + "\n// --- Game Search Logic ---")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)


# --- 2. Update snake_ladder.html to save unique GID correctly ---
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# We already have 'gid: currentGid' in sl_history. Let's ensure it's there.
if "gid: currentGid" not in sl:
    sl = sl.replace("db.ref('sl_history').push({", "db.ref('sl_history').push({\n        gid: currentGid,")
    
# Also generate 5 digit ID instead of 4 to avoid collisions
sl = sl.replace("Math.floor(1000 + Math.random() * 9000)", "Math.floor(10000 + Math.random() * 90000)")

with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)

# --- 3. Update quiz.html to save unique GID correctly ---
with open('quiz.html', 'r', encoding='utf-8') as f:
    qz = f.read()

# Add gid to quiz history
if "gid: currentGid" not in qz:
    qz = qz.replace("db.ref('quiz_history').push({", "db.ref('quiz_history').push({\n        gid: currentGid,")
    
# Generate 5 digit ID
qz = qz.replace("Math.floor(1000 + Math.random() * 9000)", "Math.floor(10000 + Math.random() * 90000)")

with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(qz)

print("Admin Panel UI Upgraded & Game History ID system fixed!")

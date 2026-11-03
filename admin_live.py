with open('admin.html', 'r', encoding='utf-8') as f:
    admin = f.read()

# 1. Add Live Tab
admin = admin.replace('<button id="tabHistory">📜 History</button>', '<button id="tabLive">🔴 Live Games</button>\n    <button id="tabHistory">📜 History</button>')

# 2. Add Live View
admin = admin.replace('<div id="vHistory" class="hidden">', """<div id="vLive" class="hidden">
    <div id="liveList"></div>
  </div>
  <div id="vHistory" class="hidden">""")

# 3. Update Tab Logic
admin = admin.replace("['Dash', 'Users', 'Reports', 'History', 'Games'].forEach", "['Dash', 'Users', 'Reports', 'Live', 'History', 'Games'].forEach")
admin = admin.replace("$('tabHistory').onclick = () => { showTab('History'); loadGameHistory(); };", """$('tabLive').onclick = () => { showTab('Live'); loadLiveGames(); };
$('tabHistory').onclick = () => { showTab('History'); loadGameHistory(); };""")

# 4. Add Live Games Logic
live_js = """
async function loadLiveGames() {
  const box = $('liveList'); box.innerHTML = 'Fetching live games...';
  box.innerHTML = '';
  
  let liveGames = [];
  
  // Fetch SL Games
  const slSnap = await db.ref('sl_games').orderByChild('status').equalTo('playing').once('value');
  slSnap.forEach(c => liveGames.push({ type: 'Snake', gid: c.key, ...c.val() }));
  
  // Fetch Quiz Games
  const qzSnap = await db.ref('quiz_games').orderByChild('status').equalTo('playing').once('value');
  qzSnap.forEach(c => liveGames.push({ type: 'Quiz', gid: c.key, ...c.val() }));

  if(liveGames.length === 0) {
    box.innerHTML = '<p class="dim" style="text-align:center; margin-top:20px;">Abhi koi live game nahi chal raha hai.</p>';
    return;
  }

  liveGames.forEach(g => {
    const row = document.createElement('div');
    row.className = 'row';
    row.innerHTML = `
      <div>
        <b style="color:var(--danger);">LIVE: ${g.type} Game</b><br>
        <small class="dim">GID: <b>${g.gid}</b></small><br>
        <small class="dim">Players: ${Object.keys(g.players || {}).length}/4</small>
      </div>
      <button class="sm warn" onclick="viewGameDetails('${g.type}', '${g.gid}')">Watch</button>
    `;
    box.appendChild(row);
  });
}
"""
admin = admin.replace("// --- Game Search Logic ---", live_js + "\n// --- Game Search Logic ---")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin)
print("Live Games tab added to Admin Panel!")

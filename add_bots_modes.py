import re

# --- 1. Update Snakes & Ladders ---
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# Add Game Mode selection to Lobby
old_lobby = """  <button id="globalBtn" style="background:#2ecc71; border-color:#2ecc71; color:#fff; font-size:1.1rem; padding:15px;">🌍 Play Global</button>"""
new_lobby = """  <button id="globalBtn" style="background:#2ecc71; border-color:#2ecc71; color:#fff; font-size:1.1rem; padding:15px;">🌍 Play Global</button>
  <div style="display:flex; gap:10px; width:100%; margin-top:10px;">
     <button id="btn1v1" style="flex:1; background:#3498db; border-color:#3498db; color:#fff;">👤 1v1 (Bot)</button>
     <button id="btn2v2" style="flex:1; background:#9b59b6; border-color:#9b59b6; color:#fff;">👥 2v2 (Bot)</button>
  </div>"""
sl = sl.replace(old_lobby, new_lobby)

# Add Bot Logic for 1v1
bot_js = """
$('btn1v1').onclick = async () => {
  // Create a room with 1 bot
  const gid = Math.floor(10000 + Math.random() * 90000).toString();
  await db.ref('sl_games/' + gid).set({
    status: 'playing',
    admin: me.uid,
    created: Date.now(),
    players: { 
      [me.uid]: { name: prof.name, pos: 0, color: 'p1' },
      'bot_1': { name: 'Bot Amit', pos: 0, color: 'p2' }
    },
    turn: me.uid,
    turnStart: Date.now(),
    dice: 0
  });
  joinRoom(gid);
};

$('btn2v2').onclick = async () => {
  // Create a room with 3 bots
  const gid = Math.floor(10000 + Math.random() * 90000).toString();
  await db.ref('sl_games/' + gid).set({
    status: 'playing',
    admin: me.uid,
    created: Date.now(),
    players: { 
      [me.uid]: { name: prof.name, pos: 0, color: 'p1' },
      'bot_1': { name: 'Bot Amit', pos: 0, color: 'p2' },
      'bot_2': { name: 'Bot Priya', pos: 0, color: 'p3' },
      'bot_3': { name: 'Bot Rohan', pos: 0, color: 'p4' }
    },
    turn: me.uid,
    turnStart: Date.now(),
    dice: 0
  });
  joinRoom(gid);
};

// Bot Turn Logic
function checkBotTurn() {
  if (!gameData || gameData.status !== 'playing') return;
  const turnUid = gameData.turn;
  
  if (turnUid && turnUid.startsWith('bot_')) {
     setTimeout(async () => {
         const dice = Math.floor(Math.random() * 6) + 1;
         const players = gameData.players;
         let newPos = players[turnUid].pos + dice;
         if (players[turnUid].pos === 0 && dice !== 6) newPos = 0; // Can't move without 6
         if (newPos > 100) newPos = 100;
         if (snakes[newPos]) newPos = snakes[newPos];
         if (ladders[newPos]) newPos = ladders[newPos];
         
         const updates = {};
         updates['players/' + turnUid + '/pos'] = newPos;
         updates.turn = getNextTurn();
         updates.turnStart = Date.now();
         updates.dice = dice;
         await gameRef.update(updates);
     }, 1500); // 1.5 sec delay for bot
  }
}
"""
sl = sl.replace("// --- Chat ---", bot_js + "\n// --- Chat ---")

# Call checkBotTurn inside updateTurn
sl = sl.replace("renderTopProfiles();\n}", "renderTopProfiles();\n  checkBotTurn();\n}")

with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)

print("Bots and Game Modes added to Snakes & Ladders!")

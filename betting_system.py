import re

# --- 1. Update Snake & Ladders ---
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# Add Entry Fee check when 4th player joins
old_start_sl = """       if (pCount + 1 === 4) {
           updates.status = 'playing';
           updates.turn = Object.keys(players)[0] || me.uid;
       }"""
new_start_sl = """       if (pCount + 1 === 4) {
           updates.status = 'playing';
           updates.turn = Object.keys(players)[0] || me.uid;
           
           // Deduct Entry Fee (50 Coins)
           for(let uid in players) {
               db.ref('profiles/' + uid + '/coins').set(firebase.database.ServerValue.increment(-50));
           }
           db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(-50));
       }"""
sl = sl.replace(old_start_sl, new_start_sl)

# Add Win Reward (200 Coins)
old_win_sl = """     // Give Rewards
     db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(100));"""
new_win_sl = """     // Give Rewards (200 Coins for Winner)
     db.ref('profiles/' + me.uid + '/coins').set(firebase.database.ServerValue.increment(200));"""
sl = sl.replace(old_win_sl, new_win_sl)

with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)

# --- 2. Update Quiz ---
with open('quiz.html', 'r', encoding='utf-8') as f:
    qz = f.read()

# Deduct 50 on Start Quiz (Admin starts it)
old_start_qz = """await gameRef.update({ status: 'playing', qIndex: 0, answers: {}, qStart: Date.now() });"""
new_start_qz = """await gameRef.update({ status: 'playing', qIndex: 0, answers: {}, qStart: Date.now() });
   // Deduct Entry Fee
   const players = gameData.players || {};
   for(let uid in players) {
       db.ref('profiles/' + uid + '/coins').set(firebase.database.ServerValue.increment(-50));
   }"""
qz = qz.replace(old_start_qz, new_start_qz)

# Give 200 to winner
old_win_qz = """       if (winnerUid) {
           db.ref('profiles/' + winnerUid + '/coins').set(firebase.database.ServerValue.increment(100));"""
new_win_qz = """       if (winnerUid) {
           db.ref('profiles/' + winnerUid + '/coins').set(firebase.database.ServerValue.increment(200));"""
qz = qz.replace(old_win_qz, new_win_qz)

with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(qz)

print("Betting system added! Entry: 50, Win: 200")

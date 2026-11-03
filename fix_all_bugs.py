import re

print("Fixing Chat App (index.html)...")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Image Size (128px, 0.5 quality) to save DB space
html = html.replace("c.width = c.height = 256;", "c.width = c.height = 128;")
html = html.replace("res(c.toDataURL('image/jpeg', .7));", "res(c.toDataURL('image/jpeg', .5));")
# 2. Fix Unread Badge logic
html = html.replace("if (!isGrp && chats[uid] && chats[uid].unread) { db.ref('userChats/'+me.uid+'/'+uid+'/unread').set(0); }", 
"if (!isGrp) { db.ref('userChats/'+me.uid+'/'+uid+'/unread').set(0); }")
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixing Snakes & Ladders (snake_ladder.html)...")
with open('snake_ladder.html', 'r', encoding='utf-8') as f:
    sl = f.read()

# 1. Add turnStart timestamp to game creation
sl = sl.replace("turn: me.uid,\n    dice: 0", "turn: me.uid,\n    turnStart: Date.now(),\n    dice: 0")
# 2. Add turnStart timestamp on updates
sl = sl.replace("updates.turn = getNextTurn(true);\n  updates.dice = 0;", "updates.turn = getNextTurn(true);\n  updates.turnStart = Date.now();\n  updates.dice = 0;")
sl = sl.replace("updates.turn = getNextTurn();\n  }\n  updates.dice = dice;", "updates.turn = getNextTurn();\n  }\n  updates.turnStart = Date.now();\n  updates.dice = dice;")
# 3. Auto-skip if time passes (works even if player disconnects)
old_turn_logic = """if (turnUid === me.uid) {
    $('turnTxt').textContent = "Tumhari baari!";
    $('turnTxt').style.color = "#2ecc71";
    $('rollBtn').disabled = false;
    startTimer();
  } else {
    $('turnTxt').textContent = (pInfo ? pInfo.name : 'Kisi aur') + " ki baari";
    $('turnTxt').style.color = "#e74c3c";
    $('rollBtn').disabled = true;
    clearInterval(turnInterval);
    $('timerTxt').textContent = ''; 
  }"""
new_turn_logic = """const turnStart = gameData.turnStart || Date.now();
  const timePassed = Date.now() - turnStart;

  if (timePassed > 12000) {
      // Auto skip if stuck for 12 seconds
      if (gameData.turn === me.uid) autoSkipTurn(); 
      $('turnTxt').textContent = "Skipping turn...";
      $('turnTxt').style.color = "#e0b04a";
      $('rollBtn').disabled = true;
      return;
  }

  if (turnUid === me.uid) {
    $('turnTxt').textContent = "Tumhari baari!";
    $('turnTxt').style.color = "#2ecc71";
    $('rollBtn').disabled = false;
    if(!turnInterval) startTimer(turnStart);
  } else {
    $('turnTxt').textContent = (pInfo ? pInfo.name : 'Kisi aur') + " ki baari";
    $('turnTxt').style.color = "#e74c3c";
    $('rollBtn').disabled = true;
    clearInterval(turnInterval); turnInterval = null;
    $('timerTxt').textContent = ''; 
  }"""
sl = sl.replace(old_turn_logic, new_turn_logic)
# 4. Update startTimer to use DB timestamp
old_start_timer = """function startTimer() {
  clearInterval(turnInterval);
  let timeLeft = 10;
  $('timerTxt').textContent = `(${timeLeft}s)`;
  turnInterval = setInterval(() => {
    timeLeft--;
    $('timerTxt').textContent = `(${timeLeft}s)`;
    if(timeLeft <= 0) {
      clearInterval(turnInterval);
      autoSkipTurn();
    }
  }, 1000);
}"""
new_start_timer = """function startTimer(startTime) {
  clearInterval(turnInterval);
  turnInterval = setInterval(() => {
    let timeLeft = 10 - Math.floor((Date.now() - startTime) / 1000);
    if(timeLeft <= 0) { $('timerTxt').textContent = `(0s)`; }
    else { $('timerTxt').textContent = `(${timeLeft}s)`; }
  }, 500);
}"""
sl = sl.replace(old_start_timer, new_start_timer)
with open('snake_ladder.html', 'w', encoding='utf-8') as f:
    f.write(sl)

print("Fixing Quiz Game (quiz.html)...")
with open('quiz.html', 'r', encoding='utf-8') as f:
    qz = f.read()

# 1. Add qStart timestamp
qz = qz.replace("await gameRef.update({ status: 'playing', qIndex: 0, answers: {} });", "await gameRef.update({ status: 'playing', qIndex: 0, answers: {}, qStart: Date.now() });")
qz = qz.replace("await gameRef.update({ qIndex: nextQ, answers: {} });", "await gameRef.update({ qIndex: nextQ, answers: {}, qStart: Date.now() });")

# 2. Sync Timer for everyone
old_quiz_timer = """if (status === 'playing') {
     const qData = QUIZ_DATA[qIndex];"""
new_quiz_timer = """if (status === 'playing') {
     const qStart = gameData.qStart || Date.now();
     const timePassed = Date.now() - qStart;
     if(timePassed > 15000 && me.uid === gameData.admin) {
         $('nextBtn').click(); // Auto next if 15s over
     }
     let tLeft = 15 - Math.floor(timePassed / 1000);
     $('timerTxt').textContent = tLeft > 0 ? `(${tLeft}s)` : `(0s)`;
     
     const qData = QUIZ_DATA[qIndex];"""
qz = qz.replace(old_quiz_timer, new_quiz_timer)

# 3. Remove old Admin-only timer to prevent clash
qz = qz.replace("if (me.uid === gameData.admin) { startAdminTimer(); }", "")
with open('quiz.html', 'w', encoding='utf-8') as f:
    f.write(qz)

print("All bugs fixed successfully! 🎉")

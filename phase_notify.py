import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Audio Notification Logic and Permission Request
notif_js = """
// --- Notification System ---
let notifyAudio = new Audio('data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU'+'9'.repeat(100)); // Silent placeholder for basic beep if needed

function requestNotifPermission() {
  if ('Notification' in window && Notification.permission !== 'granted') {
      Notification.requestPermission();
  }
}

function showLocalNotification(title, body) {
  // In-app popup (Toast)
  toast('💬 ' + title + ': ' + body);
  
  // System Notification (if allowed)
  if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, { body: body, icon: 'https://cdn-icons-png.flaticon.com/512/134/134914.png' });
  }
}

// Call permission request on login
let notifReqDone = false;
"""

# Insert this before the first auth.onAuthStateChanged
html = html.replace("auth.onAuthStateChanged(async user => {", notif_js + "\nauth.onAuthStateChanged(async user => {")

# 2. Call request in enterApp
html = html.replace("screen('app'); applyTheme(); applyI18n(); showTab('Chats'); renderMe(); renderGames();", 
"screen('app'); applyTheme(); applyI18n(); showTab('Chats'); renderMe(); renderGames();\n  if(!notifReqDone) { requestNotifPermission(); notifReqDone = true; }")

# 3. Add trigger for incoming messages in the DB listener
# Find the listRef listener
old_list = """listRef = db.ref('userChats/' + me.uid);
  listRef.on('value', s => { chats = s.val() || {}; renderList(); });"""
  
new_list = """listRef = db.ref('userChats/' + me.uid);
  let prevChats = {};
  listRef.on('value', s => { 
      const newChats = s.val() || {}; 
      
      // Notification Logic
      if(Object.keys(prevChats).length > 0) {
          for(const uid in newChats) {
              if(prevChats[uid] && newChats[uid].ts > prevChats[uid].ts && (!cur || cur.uid !== uid)) {
                  // New message came in a different chat
                  if(!cur || cur.uid !== uid) {
                     showLocalNotification(newChats[uid].name, newChats[uid].last);
                  }
              }
          }
      }
      
      prevChats = newChats;
      chats = newChats; 
      renderList(); 
  });"""
html = html.replace(old_list, new_list)

# 4. Also notify in the live chat if we are in a different chat
# Actually, the listRef logic handles most. But let's add for active chat too.
html = html.replace("mref.on('child_added', s => addMsg(s.val(), s.key));", 
"""mref.on('child_added', s => {
        const m = s.val();
        addMsg(m, s.key);
        if (m.from !== me.uid && Date.now() - (m.ts || 0) < 5000) {
           showLocalNotification(cur.name, m.text || '[Photo]');
        }
    });""")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Notification system added!")

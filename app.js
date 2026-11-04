const $ = id => document.getElementById(id);
const TS = firebase.database.ServerValue.TIMESTAMP;
let me = null, prof = null, chats = {}, cur = null, mref = null, listRef = null;
let replyTo = null;

// --- Login & Auth ---
let mode = 'login';
$('go').onclick = async () => {
  const email = $('email').value.trim();
  const pass = $('pass').value;
  if(!email || !pass) return alert('Email/Password dalo');
  try {
    if(mode === 'login') await auth.signInWithEmailAndPassword(email, pass);
    else await auth.createUserWithEmailAndPassword(email, pass);
  } catch(e) { alert(e.message); }
};

$('guestBtn').onclick = async () => {
  try { await auth.signInAnonymously(); } catch(e) { alert(e.message); }
};

auth.onAuthStateChanged(async user => {
  if(user) {
    me = user;
    $('auth').classList.add('hidden');
    $('app').classList.remove('hidden');
    
    // Check if user profile exists, else create
    const snap = await db.ref('profiles/' + user.uid).once('value');
    if(!snap.exists()) {
       await db.ref('profiles/' + user.uid).set({
          name: 'User_' + Math.floor(Math.random()*1000),
          username: 'user' + Math.floor(Math.random()*10000),
          city: 'Unknown',
          coins: 300,
          gamesWon: 0
       });
    }
    prof = (await db.ref('profiles/' + user.uid).once('value')).val();
    initChat();
  } else {
    $('auth').classList.remove('hidden');
    $('app').classList.add('hidden');
  }
});

// --- Navigation ---
function showTab(t) {
  ['Chats','Games','Me'].forEach(x => {
     $('v' + x).classList.toggle('hidden', x !== t);
     $('n' + x).classList.toggle('on', x === t);
  });
  if(t !== 'Chats') closeChat();
}
$('nChats').onclick = () => showTab('Chats');
$('nGames').onclick = () => showTab('Games');
$('nMe').onclick = () => showTab('Me');

// --- Chat System ---
function initChat() {
  listRef = db.ref('userChats/' + me.uid);
  listRef.on('value', s => {
     chats = s.val() || {};
     renderList();
  });
}

function renderList() {
  const box = $('list'); box.innerHTML = '';
  if(!me || $('q').value.trim()) return;
  const arr = Object.entries(chats).sort((a, b) => (b[1].ts || 0) - (a[1].ts || 0));
  
  if(!arr.length) {
     box.appendChild(el('div','empty','Abhi koi chat nahi hai. Upar search karo.'));
     return;
  }
  
  arr.forEach(([uid, c]) => {
     const r = el('div', 'row');
     const a = el('div', 'av'); a.textContent = c.name[0].toUpperCase();
     r.appendChild(a);
     const t = el('div', 't');
     t.appendChild(el('b','', c.name));
     t.appendChild(el('small','', c.last || ''));
     r.appendChild(t);
     r.onclick = () => openChat(uid, c.name);
     box.appendChild(r);
  });
}

let timer = null;
$('q').oninput = () => { clearTimeout(timer); timer = setTimeout(search, 300); };
async function search() {
  const q = $('q').value.trim().toLowerCase().replace(/^@/, '');
  const box = $('results'); box.innerHTML = '';
  if(!q) { $('list').classList.remove('hidden'); renderList(); return; }
  $('list').classList.add('hidden');
  
  try {
     const s = await db.ref('usernames').orderByKey().startAt(q).endAt(q + '\uf8ff').limitToFirst(10).once('value');
     let found = 0;
     for (const [un, uid] of Object.entries(s.val() || {})) {
        if(uid === me.uid) continue;
        const p = (await db.ref('profiles/' + uid).once('value')).val();
        if(p) {
           const r = el('div', 'row');
           const a = el('div', 'av'); a.textContent = p.name[0].toUpperCase(); r.appendChild(a);
           const t = el('div', 't'); t.appendChild(el('b','', p.name)); t.appendChild(el('small','', '@' + un)); r.appendChild(t);
           r.onclick = () => openChat(uid, p.name);
           box.appendChild(r); found++;
        }
     }
     if(!found) box.appendChild(el('div','empty','User nahi mila.'));
  } catch(e) {}
}

// --- Active Chat Logic ---
function openChat(uid, name) {
  cur = { uid, name };
  $('chName').textContent = name;
  $('chAv').textContent = name[0].toUpperCase();
  $('msgs').innerHTML = '';
  $('chat').classList.remove('hidden');
  
  const cid = [me.uid, uid].sort().join('_');
  mref = db.ref('chats/' + cid + '/messages').limitToLast(50);
  mref.on('child_added', s => addMsg(s.val(), s.key));
}

function closeChat() {
  if(mref) { mref.off(); mref = null; }
  cur = null;
  $('chat').classList.add('hidden');
  $('q').value = ''; $('results').innerHTML = '';
  $('list').classList.remove('hidden');
}
$('back').onclick = closeChat;

function addMsg(m) {
  if(!m) return;
  const isMe = m.from === me.uid;
  const b = el('div', 'b ' + (isMe ? 'me' : 'th'), m.text);
  const tm = new Date(m.ts).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'});
  b.appendChild(el('small','', tm));
  $('msgs').appendChild(b);
  $('msgs').scrollTop = $('msgs').scrollHeight;
}

$('send').onclick = () => {
  const text = $('txt').value.trim();
  if(!text || !cur) return;
  $('txt').value = '';
  const cid = [me.uid, cur.uid].sort().join('_');
  const key = db.ref('chats/' + cid + '/messages').push().key;
  const u = {};
  u['chats/' + cid + '/messages/' + key] = { from: me.uid, text, ts: TS };
  u['userChats/' + me.uid + '/' + cur.uid] = { name: cur.name, last: text.slice(0,30), ts: TS };
  u['userChats/' + cur.uid + '/' + me.uid] = { name: prof.name, last: text.slice(0,30), ts: TS };
  db.ref().update(u);
};

// --- Utility ---
function el(tag, cls, text) {
  const e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text) e.textContent = text;
  return e;
}

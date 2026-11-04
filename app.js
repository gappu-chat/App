const $ = id => document.getElementById(id);
const TS = firebase.database.ServerValue.TIMESTAMP;

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
    $('auth').classList.add('hidden');
    $('app').classList.remove('hidden');
    
    // Check if user profile exists
    const snap = await db.ref('profiles/' + user.uid).once('value');
    if(!snap.exists()) {
       // Create dummy profile for new users (Claim ID system can be added later)
       await db.ref('profiles/' + user.uid).set({
          name: 'User_' + Math.floor(Math.random()*1000),
          username: 'user' + Math.floor(Math.random()*10000),
          city: 'Unknown',
          coins: 300, // Welcome Bonus
          gamesWon: 0
       });
    }
  } else {
    $('auth').classList.remove('hidden');
    $('app').classList.add('hidden');
  }
});

// --- Navigation ---
$('nChats').onclick = () => {
  $('nChats').classList.add('on');
  $('nGames').classList.remove('on');
  $('nMe').classList.remove('on');
  alert('Chats tab active (logic baad me)');
};
$('nGames').onclick = () => {
  $('nChats').classList.remove('on');
  $('nGames').classList.add('on');
  $('nMe').classList.remove('on');
  alert('Games tab active (logic baad me)');
};
$('nMe').onclick = () => {
  $('nChats').classList.remove('on');
  $('nGames').classList.remove('on');
  $('nMe').classList.add('on');
  alert('Profile tab active (logic baad me)');
};

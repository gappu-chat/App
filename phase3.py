import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Event Tab in Bottom Navigation
old_nav = """<button id="nMe"><i>👤</i><span data-i="me"></span></button>"""
new_nav = """<button id="nEvent"><i>🎁</i><span>Event</span></button>
    <button id="nMe"><i>👤</i><span data-i="me"></span></button>"""
html = html.replace(old_nav, new_nav)

# 2. Add Event View Container
old_views = """<div id="vMe" class="hidden"><div id="meBox"></div></div>"""
new_views = """<div id="vEvent" class="hidden">
    <h2 style="color:#e0b04a; text-align:center;">🎁 Event & Shop</h2>
    <p style="text-align:center; color:var(--dim); font-size:0.9rem;">Apne coins se premium cheezein kharido!</p>
    <div id="eventBox"></div>
  </div>
  <div id="vMe" class="hidden"><div id="meBox"></div></div>"""
html = html.replace(old_views, new_views)

# 3. Update Tab Switching Logic
old_tabs = """$('nChats').onclick = () => showTab('Chats');
$('nGames').onclick = () => showTab('Games');
$('nMe').onclick = () => showTab('Me');"""
new_tabs = """$('nChats').onclick = () => showTab('Chats');
$('nGames').onclick = () => showTab('Games');
$('nEvent').onclick = () => { showTab('Event'); renderEvent(); };
$('nMe').onclick = () => showTab('Me');"""
html = html.replace(old_tabs, new_tabs)

# 4. Update showTab array to include Event
html = html.replace("['Chats','Games','Me'].forEach", "['Chats','Games','Event','Me'].forEach")

# 5. Add Event Rendering Logic before </script>
event_logic = """
// --- Event & Shop Logic ---
const SHOP_ITEMS = [
  { id: 'gold_theme', name: 'Golden Theme', price: 500, icon: '👑', desc: 'Ek premium golden theme', type: 'theme' },
  { id: 'vip_badge', name: 'VIP Badge', price: 1000, icon: '💎', desc: 'Profile aur leaderboard par VIP tag', type: 'badge' },
  { id: 'red_name', name: 'Red Name', price: 200, icon: '🔴', desc: 'Chat me naam red color ka', type: 'color' }
];

function renderEvent() {
  const box = $('eventBox'); box.innerHTML = '';
  
  // Show current coins
  const coinCard = el('div', 'card pc');
  coinCard.style.background = 'linear-gradient(135deg, #f6b73c, #e4573d)';
  coinCard.style.color = '#fff';
  coinCard.appendChild(el('div', '', 'Tumhare Paas Hai'));
  coinCard.appendChild(el('div', 'big', '🪙 ' + (prof.coins || 0) + ' Coins'));
  coinCard.style.fontWeight = 'bold';
  box.appendChild(coinCard);
  
  SHOP_ITEMS.forEach(item => {
    const row = el('div', 'row');
    row.style.flexDirection = 'column';
    row.style.alignItems = 'flex-start';
    row.style.cursor = 'default';
    
    const top = el('div');
    top.style.display = 'flex'; top.style.width = '100%'; top.style.alignItems = 'center'; top.style.gap = '10px';
    top.appendChild(el('div', '', item.icon)).style.fontSize = '2rem';
    
    const info = el('div'); info.style.flex = '1';
    info.appendChild(el('b', '', item.name));
    info.appendChild(el('div', '', item.desc)).style.fontSize = '0.8rem';
    info.lastChild.style.color = 'var(--dim)';
    
    const btn = el('button', '', '🪙 ' + item.price);
    btn.style.width = 'auto'; btn.style.margin = '0'; btn.style.padding = '8px 12px';
    
    // Check if already purchased
    const owned = prof.inventory && prof.inventory[item.id];
    if (owned) {
      btn.textContent = '✅ Owned';
      btn.disabled = true;
      btn.style.background = '#2ecc71'; btn.style.borderColor = '#2ecc71'; btn.style.color = '#fff';
    } else {
      btn.onclick = () => buyItem(item);
    }
    
    top.appendChild(info);
    top.appendChild(btn);
    row.appendChild(top);
    
    // Apply theme logic if owned
    if (owned && item.type === 'theme') applyThemeFromShop(item.id);
    
    box.appendChild(row);
  });
}

async function buyItem(item) {
  if ((prof.coins || 0) < item.price) {
    toast('Tumhare paas itne coins nahi hain! Game khel kar jeeto.');
    return;
  }
  
  try {
    const updates = {};
    updates['profiles/' + me.uid + '/coins'] = firebase.database.ServerValue.increment(-item.price);
    updates['profiles/' + me.uid + '/inventory/' + item.id] = true;
    await db.ref().update(updates);
    
    prof.coins = (prof.coins || 0) - item.price;
    if (!prof.inventory) prof.inventory = {};
    prof.inventory[item.id] = true;
    
    toast('Kharid liya! ' + item.name);
    renderEvent();
    renderMe();
  } catch(e) { toast('Purchase failed!'); }
}

function applyThemeFromShop(id) {
  if (id === 'gold_theme') {
    document.documentElement.dataset.theme = 'gold';
    // Add gold theme CSS dynamically if not exists
    if (!document.getElementById('goldTheme')) {
       const style = document.createElement('style');
       style.id = 'goldTheme';
       style.textContent = `[data-theme=gold]{--bg:#1a1500;--bg2:#ffd700;--card:#2b2500;--acc:#ffd700;--ink:#fff;--dim:#aaa;--bar:#110e00;--on:#000;--line:#665500}`;
       document.head.appendChild(style);
    }
    theme = 'gold';
  }
}
"""
html = html.replace("</script>\n</body>\n</html>", event_logic + "\n</script>\n</body>\n</html>")

# 6. Update Leaderboard to show Badge & Name Color
old_rank = """info.appendChild(el('b', '', u.name));"""
new_rank = """const nameEl = el('b', '', u.name);
        if (u.inventory && u.inventory['vip_badge']) nameEl.textContent += ' 💎';
        if (u.inventory && u.inventory['red_name']) nameEl.style.color = '#e74c3c';
        info.appendChild(nameEl);"""
html = html.replace(old_rank, new_rank)

# 7. Update Profile to show Badge
old_prof_name = """card.appendChild(el('div', 'big', prof.name));"""
new_prof_name = """const pName = el('div', 'big', prof.name);
  if (prof.inventory && prof.inventory['vip_badge']) pName.textContent += ' 💎';
  if (prof.inventory && prof.inventory['red_name']) pName.style.color = '#e74c3c';
  card.appendChild(pName);"""
html = html.replace(old_prof_name, new_prof_name)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Phase 3 Complete! Event Shop added.")

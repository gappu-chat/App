import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace Event View with Countdown Design
old_view = """<div id="vEvent" class="hidden">
    <h2 style="color:#e0b04a; text-align:center;">🎁 Event & Shop</h2>
    <p style="text-align:center; color:var(--dim); font-size:0.9rem;">Apne coins se premium cheezein kharido!</p>
    <div id="eventBox"></div>
  </div>"""
new_view = """<div id="vEvent" class="hidden" style="display:flex; flex-direction:column; align-items:center; text-align:center;">
    <h2 style="color:var(--acc); margin-bottom:5px;">🎉 Big Event Coming!</h2>
    <p style="color:var(--dim); font-size:0.9rem; margin-top:0;">Taiyari karo, kuch bada aane wala hai.</p>
    
    <div style="background:var(--card); border:2px solid var(--line); border-radius:16px; padding:20px; width:100%; margin-top:15px; box-sizing:border-box;">
      <h3 style="margin:0; color:#e74c3c; font-size:1.5rem;">1 December 2026</h3>
      <p style="font-size:0.9rem; opacity:0.8;">Event Start Hone Me Baki:</p>
      
      <div id="countdown" style="display:flex; justify-content:center; gap:10px; margin-top:15px; font-size:1.2rem; font-weight:bold; color:var(--acc);">
         <div><span id="cd-days">00</span><br><span style="font-size:0.6rem; color:var(--dim)">DAYS</span></div> :
         <div><span id="cd-hours">00</span><br><span style="font-size:0.6rem; color:var(--dim)">HRS</span></div> :
         <div><span id="cd-mins">00</span><br><span style="font-size:0.6rem; color:var(--dim)">MIN</span></div> :
         <div><span id="cd-secs">00</span><br><span style="font-size:0.6rem; color:var(--dim)">SEC</span></div>
      </div>
    </div>

    <div style="text-align:left; width:100%; margin-top:20px;">
      <h3 style="color:var(--acc); margin-bottom:10px;">Event Me Kya Milega?</h3>
      <div class="row" style="opacity:0.6;">
         <div class="ri">👑</div> <b>Exclusive Themes</b>
      </div>
      <div class="row" style="opacity:0.6;">
         <div class="ri">💎</div> <b>VIP Badges & Titles</b>
      </div>
      <div class="row" style="opacity:0.6;">
         <div class="ri">💰</div> <b>Real Money Gifts & Coins</b>
      </div>
    </div>
    <div style="margin-top:20px; font-size:0.8rem; color:#e74c3c; font-weight:bold; padding:10px; background:#7a2a2a44; border-radius:10px; border:1px solid #7a2a2a;">
      🔒 Kharidari abhi band hai. Event start hote hi unlock ho jayega!
    </div>
  </div>"""
html = html.replace(old_view, new_view)

# 2. Replace the old renderEvent function with the Countdown logic
old_render = """function renderEvent() {
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
}"""

new_render = """let eventTimer = null;

function renderEvent() {
  clearInterval(eventTimer);
  const targetDate = new Date("2026-12-01T00:00:00").getTime();
  
  eventTimer = setInterval(() => {
    const now = new Date().getTime();
    const distance = targetDate - now;
    
    if (distance < 0) {
      clearInterval(eventTimer);
      $('countdown').innerHTML = "<h2 style='color:#2ecc71;'>Event LIVE! 🎉</h2>";
      return;
    }
    
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);
    
    $('cd-days').textContent = days < 10 ? '0'+days : days;
    $('cd-hours').textContent = hours < 10 ? '0'+hours : hours;
    $('cd-mins').textContent = minutes < 10 ? '0'+minutes : minutes;
    $('cd-secs').textContent = seconds < 10 ? '0'+seconds : seconds;
  }, 1000);
}"""
html = html.replace(old_render, new_render)

# 3. Fix tab switching to trigger the timer
html = html.replace("$('nEvent').onclick = () => { showTab('Event'); renderEvent(); };", "$('nEvent').onclick = () => { showTab('Event'); renderEvent(); };\n$('nMe').onclick = () => { showTab('Me'); clearInterval(eventTimer); };\n$('nChats').onclick = () => { showTab('Chats'); clearInterval(eventTimer); };\n$('nGames').onclick = () => { showTab('Games'); clearInterval(eventTimer); };")
# Remove old duplicate onclick listeners
html = html.replace("$('nChats').onclick = () => showTab('Chats');\n$('nGames').onclick = () => showTab('Games');\n$('nMe').onclick = () => showTab('Me');", "")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Event Section with Countdown added successfully!")

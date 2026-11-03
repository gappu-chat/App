import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Ranking Button to Chats Header
old_header = """<h2 style="margin:0" data-i="chats"></h2>
      <button id="newGroupBtn" class="sm" style="width:auto; padding:8px 12px; font-size:0.9rem;">➕ Group</button>"""
new_header = """<h2 style="margin:0" data-i="chats"></h2>
      <div style="display:flex; gap:8px;">
        <button id="rankingBtn" class="sm" style="width:auto; padding:8px 12px; font-size:0.9rem; background:#3498db; border-color:#3498db; color:#fff;">🏆 Ranking</button>
        <button id="newGroupBtn" class="sm" style="width:auto; padding:8px 12px; font-size:0.9rem;">➕ Group</button>
      </div>"""
html = html.replace(old_header, new_header)

# 2. Add Ranking Modal HTML
modal_html = """
<div id="rankModal" class="hidden" style="position:fixed;top:0;left:0;right:0;bottom:0;background:var(--bg);z-index:50;display:flex;flex-direction:column;">
  <div style="padding:15px; border-bottom:2px solid var(--acc); display:flex; justify-content:space-between; align-items:center; background:var(--bar);">
    <h2 style="margin:0; color:var(--acc);">🏆 Leaderboard</h2>
    <button id="closeRankBtn" class="ic alt" style="border:none;">✕</button>
  </div>
  <div style="display:flex; padding:10px; gap:10px; background:var(--card);">
    <button id="tabGlobal" class="on" style="margin:0; flex:1;">Global</button>
    <button id="tabIndia" style="margin:0; flex:1;">India</button>
  </div>
  <div id="rankList" style="flex:1; overflow-y:auto; padding:15px; display:flex; flex-direction:column; gap:10px;"></div>
</div>
"""
html = html.replace('<div id="sheet" class="hidden">', modal_html + '\n<div id="sheet" class="hidden">')

# 3. Add Ranking JS Logic before </script>
rank_js = """
// --- Ranking Logic ---
let allUsers = [];
let currentRankTab = 'global';

$('rankingBtn').onclick = async () => {
    $('rankModal').classList.remove('hidden');
    $('rankList').innerHTML = '<div style="text-align:center; color:var(--dim); margin-top:20px;">Loading Ranking...</div>';
    
    // Fetch top 100 users based on coins
    const snap = await db.ref('profiles').orderByChild('coins').limitToLast(100).once('value');
    allUsers = [];
    snap.forEach(child => {
        allUsers.push({ uid: child.key, ...child.val() });
    });
    allUsers.reverse(); // Highest first
    
    renderRanking();
};

function renderRanking() {
    const box = $('rankList'); box.innerHTML = '';
    
    let filtered = allUsers;
    if (currentRankTab === 'india') {
        filtered = allUsers.filter(u => {
            const c = (u.city || '').toLowerCase();
            // Simple check for Indian cities, you can add more
            return c.includes('india') || c.includes('delhi') || c.includes('mumbai') || c.includes('kolkata') || c.includes('chennai') || c.includes('bangalore') || c.includes('pune') || c.includes('hyderabad') || c.includes('jaipur') || c.includes('patna') || c.includes('lucknow') || c.includes('bihar') || c.includes('up');
        });
    }

    if (filtered.length === 0) {
        box.innerHTML = '<div style="text-align:center; color:var(--dim); margin-top:20px;">Abhi koi player nahi hai is list me.</div>';
        return;
    }

    filtered.forEach((u, i) => {
        const row = el('div', 'row');
        row.style.background = 'var(--card)';
        row.style.cursor = 'default';
        
        // Rank number or medal
        let rankTxt = (i+1) + '.';
        let rankColor = 'var(--dim)';
        if(i === 0) { rankTxt = '🥇'; rankColor = '#f1c40f'; }
        else if(i === 1) { rankTxt = '🥈'; rankColor = '#bdc3c7'; }
        else if(i === 2) { rankTxt = '🥉'; rankColor = '#cd7f32'; }
        
        const rankEl = el('div', '', rankTxt);
        rankEl.style.fontSize = '1.2rem';
        rankEl.style.fontWeight = 'bold';
        rankEl.style.width = '35px';
        rankEl.style.textAlign = 'center';
        rankEl.style.color = rankColor;
        
        const av = el('div', 'av');
        av.style.width = '40px'; av.style.height = '40px'; av.style.fontSize = '1rem';
        setAv(av, u.uid, u.name);
        
        const info = el('div', 't');
        info.appendChild(el('b', '', u.name));
        info.appendChild(el('small', '', '📍 ' + (u.city || 'Unknown')));
        
        const coins = el('div', '', '🪙 ' + (u.coins || 0));
        coins.style.fontWeight = 'bold';
        coins.style.color = 'var(--acc)';
        
        row.appendChild(rankEl);
        row.appendChild(av);
        row.appendChild(info);
        row.appendChild(coins);
        box.appendChild(row);
    });
}

$('tabGlobal').onclick = () => {
    currentRankTab = 'global';
    $('tabGlobal').classList.add('on');
    $('tabIndia').classList.remove('on');
    renderRanking();
};
$('tabIndia').onclick = () => {
    currentRankTab = 'india';
    $('tabIndia').classList.add('on');
    $('tabGlobal').classList.remove('on');
    renderRanking();
};
$('closeRankBtn').onclick = () => $('rankModal').classList.add('hidden');
"""
html = html.replace("</script>\n</body>\n</html>", rank_js + "\n</script>\n</body>\n</html>")

# 4. Fix existing users who might not have coins or city in database
old_edit_prof = "await db.ref('profiles/' + me.uid).update({ name: v, city: city || 'Unknown' });"
new_edit_prof = "await db.ref('profiles/' + me.uid).update({ name: v, city: city || 'Unknown', coins: prof.coins || 0, gamesWon: prof.gamesWon || 0 });"
html = html.replace(old_edit_prof, new_edit_prof)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Phase 2 Complete! Ranking system added.")

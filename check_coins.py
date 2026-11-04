with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check coins before opening Games tab
old_games_tab = """$('nGames').onclick = () => { showTab('Games'); clearInterval(eventTimer); };"""
new_games_tab = """$('nGames').onclick = () => { 
  if((prof.coins || 0) < 50) {
     toast('Game khelne ke liye kam se kam 50 Coins chahiye. Pehle jeeto ya kharido!');
     return;
  }
  showTab('Games'); clearInterval(eventTimer); 
};"""
html = html.replace(old_games_tab, new_games_tab)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Minimum coins check added!")

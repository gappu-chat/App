import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_search_end = """  if (!n && q !== prof.username) box.appendChild(el('div', 'empty', t('nouser')));
}"""
new_search_end = """  if (!n && q !== prof.username) box.appendChild(el('div', 'empty', t('nouser')));
  
  const urlParams = new URLSearchParams(window.location.search);
  const targetChat = urlParams.get('chat');
  if (targetChat && q === targetChat) {
      const firstRow = box.querySelector('.row');
      if (firstRow) {
          firstRow.click();
          window.history.replaceState({}, document.title, window.location.pathname);
          document.getElementById('q').value = ''; document.getElementById('results').innerHTML = '';
          renderList();
      }
  }
}"""

html = html.replace(old_search_end, new_search_end)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Chat link system ready!")

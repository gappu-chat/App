import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix the URL param logic to run AFTER app enters
old_logic = """  const urlParams = new URLSearchParams(window.location.search);
  const targetChat = urlParams.get('chat');
  if (targetChat && q === targetChat) {
      const firstRow = box.querySelector('.row');
      if (firstRow) {
          firstRow.click();
          window.history.replaceState({}, document.title, window.location.pathname);
          document.getElementById('q').value = ''; document.getElementById('results').innerHTML = '';
          renderList();
      }
  }"""

new_logic = """  // URL chat logic moved to enterApp to catch it on load"""

if old_logic in html:
    html = html.replace(old_logic, new_logic)

# 2. Add URL check in enterApp (after everything is loaded)
old_enter = """  listRef = db.ref('userChats/' + me.uid);
  listRef.on('value', s => { chats = s.val() || {}; renderList(); });"""

new_enter = """  listRef = db.ref('userChats/' + me.uid);
  listRef.on('value', s => { chats = s.val() || {}; renderList(); });
  
  // Check if URL has ?chat=username
  const urlParams = new URLSearchParams(window.location.search);
  const targetChat = urlParams.get('chat');
  if (targetChat) {
      window.history.replaceState({}, document.title, window.location.pathname); // Clear URL
      // Set search query and trigger search
      document.getElementById('q').value = targetChat;
      search().then(() => {
          setTimeout(() => {
              const firstRow = document.getElementById('results').querySelector('.row');
              if (firstRow) firstRow.click();
              document.getElementById('q').value = ''; 
              document.getElementById('results').innerHTML = '';
              renderList();
          }, 500);
      });
  }"""

if old_enter in html:
    html = html.replace(old_enter, new_enter)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Chat link bug fixed!")

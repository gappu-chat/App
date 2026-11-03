import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Privacy Policy & Delete Account Buttons in Profile Settings menu
old_menu = """[['✏️','editp',editProfile], ['🆔','chid',idSheet], ['✉️','email',emailSheet], ['📱','phone',phoneSheet],
   ['🔑','preset',resetPass], ['🎨','theme',themeSheet], ['🌐','lang',langSheet], ['🛡️','privacy',privacySheet],
   ['🚫','blist',blockSheet]].forEach(([i,k,f]) => {"""
new_menu = """[['✏️','editp',editProfile], ['🆔','chid',idSheet], ['✉️','email',emailSheet], ['📱','phone',phoneSheet],
   ['🔑','preset',resetPass], ['🎨','theme',themeSheet], ['🌐','lang',langSheet], ['🛡️','privacy',privacySheet],
   ['🚫','blist',blockSheet], ['📜','Privacy Policy', privacyPolicySheet], ['🗑️','Delete Account', deleteAccountSheet]].forEach(([i,k,f]) => {"""
html = html.replace(old_menu, new_menu)

# 2. Add Privacy Policy & Delete Logic before </script>
privacy_logic = """
// --- Privacy Policy & Delete Account ---
function privacyPolicySheet() {
  openSheet('Privacy Policy', b => {
    const content = el('div', '');
    content.style.fontSize = '0.9rem';
    content.style.lineHeight = '1.5';
    content.innerHTML = `
      <p><b>Gappu Chat Privacy Policy</b></p>
      <p>Hum aapka data kaise use karte hain:</p>
      <ul style="padding-left:20px;">
        <li><b>Email:</b> Sirf login karne ke liye use hota hai.</li>
        <li><b>Naam, City, Profile Photo:</b> Taaki dost aapko pehchan sake.</li>
        <li><b>Chats:</b> Aapke messages secure Firebase database me save hote hain.</li>
        <li><b>Security:</b> Hum aapka data kisi third-party ko nahi bechte.</li>
      </ul>
      <p>Aap kabhi bhi apna account delete kar sakte hain.</p>
    `;
    b.appendChild(content);
  });
}

function deleteAccountSheet() {
  openSheet('Delete Account', b => {
    const m = el('div', '', 'Kya aap sach me apna account delete karna chahte hain? Ye action wapas nahi ho sakta. Aapke saare messages, games aur coins hamesha ke liye chale jayenge.');
    m.style.color = 'var(--danger)';
    m.style.marginBottom = '15px';
    b.appendChild(m);
    
    const btn = el('button', '', 'Haan, Account Delete Karo');
    btn.style.background = 'var(--danger)';
    btn.style.borderColor = 'var(--danger)';
    btn.style.color = '#fff';
    btn.onclick = async () => {
      btn.textContent = 'Deleting...';
      btn.disabled = true;
      
      try {
        // 1. Delete profile data
        await db.ref('profiles/' + me.uid).remove();
        // 2. Delete presence
        await db.ref('presence/' + me.uid).remove();
        // 3. Delete from usernames
        if (prof.username) await db.ref('usernames/' + prof.username).remove();
        
        // 4. Delete Auth Account
        await me.delete();
        
        // 5. Clear local storage and redirect
        localStorage.clear();
        window.location.reload();
      } catch(e) {
        if (e.code === 'auth/requires-recent-login') {
           toast('Security ke liye, pehle logout karke dobara login karein aur fir delete karein.');
        } else {
           toast('Delete failed: ' + e.message);
        }
        btn.textContent = 'Haan, Account Delete Karo';
        btn.disabled = false;
      }
    };
    b.appendChild(btn);
  });
}
"""
html = html.replace("</script>\n</body>\n</html>", privacy_logic + "\n</script>\n</body>\n</html>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Privacy Policy and Account Deletion added!")

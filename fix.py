import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Jo galat script galti se add hui hai, use hatao
bad_script = r'<script>\s*document\.getElementById\("imgBtn"\)[\s\S]*?<\/script>'
html = re.sub(bad_script, '', html)

# 2. addMsg function me Photo dikhane ka logic add karo
old_addMsg = """  const textNode = document.createTextNode(m.text);
  b.appendChild(textNode);"""
    
new_addMsg = """  if (m.img) {
    const img = document.createElement('img');
    img.src = m.img;
    img.style.maxWidth = '100%';
    img.style.borderRadius = '8px';
    img.style.marginBottom = '4px';
    b.appendChild(img);
  } else {
    const textNode = document.createTextNode(m.text);
    b.appendChild(textNode);
  }"""
    
if old_addMsg in html:
    html = html.replace(old_addMsg, new_addMsg)

# 3. Photo bhejne ka naya sahi logic file ke end me add karo
img_logic = """
// --- Image Upload Logic ---
document.getElementById("imgBtn").onclick = () => { document.getElementById("file").click(); };
document.getElementById("file").onchange = async (e) => {
  const f = e.target.files[0]; e.target.value = "";
  if (!f) return;
  if (!cur) { toast("Pehle chat kholo"); return; }
  try {
    const url = await shrink(f);
    const text = "[Photo]";
    if (cur.demo) {
      const m = { from: me.uid, text, img: url, ts: Date.now() };
      dstore(cur.uid, m, cur.name); addMsg(m);
      return;
    }
    const baseRef = cur.isGroup ? "groups/" + cur.uid : "chats/" + cur.cid;
    const key = db.ref(baseRef + "/messages").push().key;
    const u = {};
    u[baseRef + "/messages/" + key] = { from: me.uid, text, img: url, ts: TS };
    u["userChats/" + me.uid + "/" + cur.uid] = { name: cur.name, last: text, ts: TS };
    if(!cur.isGroup) {
       const otherUnread = (chats[cur.uid] && chats[cur.uid].unread) ? chats[cur.uid].unread : 0;
       u["userChats/" + cur.uid + "/" + me.uid] = { name: prof.name, last: text, ts: TS, unread: otherUnread + 1 };
    }
    db.ref().update(u).catch(() => { toast("Fail"); });
  } catch (x) { console.error(x); toast("Photo bhejne me error aaya"); }
};
// --------------------------
"""

# File ke end me add karo
parts = html.rsplit('</script>', 1)
if len(parts) == 2:
    html = parts[0] + img_logic + '</script>' + parts[1]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fix ho gaya! Ab browser me localhost:8000 kholo.")

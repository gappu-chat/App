import os, base64, re

# 1. Create manifest.json
manifest = """{
  "name": "Gappu Chat",
  "short_name": "Gappu",
  "start_url": "./index.html",
  "display": "standalone",
  "background_color": "#0d2b2a",
  "theme_color": "#0d2b2a",
  "description": "Free Chat, Games, aur bahut kuch!",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}"""
with open('manifest.json', 'w') as f:
    f.write(manifest)

# 2. Create sw.js (Service Worker)
sw = """const CACHE_NAME = 'gappu-chat-v1';
const urlsToCache = [
  './',
  './index.html',
  './game.html',
  './snake_ladder.html',
  './quiz.html',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});"""
with open('sw.js', 'w') as f:
    f.write(sw)

# 3. Create dummy icons (Base64 1x1 transparent PNG for now, user can replace later)
icon_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
with open('icon-192.png', 'wb') as f:
    f.write(icon_data)
with open('icon-512.png', 'wb') as f:
    f.write(icon_data)

# 4. Update index.html to include Manifest and Service Worker
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add manifest link in <head>
if 'manifest.json' not in html:
    html = html.replace('<meta name="google" content="notranslate">', '<meta name="google" content="notranslate">\n<link rel="manifest" href="manifest.json">\n<meta name="theme-color" content="#0d2b2a">')

# Add Service Worker registration in <script>
sw_reg = """
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').then(reg => {
      console.log('SW registered!', reg);
    }).catch(err => {
      console.log('SW registration failed!', err);
    });
  });
}
"""
if 'serviceWorker.register' not in html:
    html = html.replace("</script>\n</body>\n</html>", sw_reg + "\n</script>\n</body>\n</html>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("PWA Setup Complete! manifest.json, sw.js, and icons created.")

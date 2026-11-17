# Builds the standalone copies of the prototype:
#   OUT_DIR/          -> GitHub Pages (installable, offline)
#   STANDALONE.html   -> single file for /mnt/project-files
# usage: python3 build_site.py PROTOTYPE.html OUT_DIR STANDALONE.html
import sys,os
from PIL import Image, ImageDraw
proto,site,standalone_path=sys.argv[1:4]
src=open(proto,encoding='utf-8').read()
body=src.replace('<title>V60 Coffee Prototype</title>','')
base_head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0E1621">
<title>V60 Coffee</title>
'''
pwa_head='''<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="V60">
'''
sw_reg='''<script>
if('serviceWorker' in navigator){addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));}
</script>
'''
standalone=base_head+'</head>\n<body>\n'+body+'\n</body>\n</html>\n'
open(standalone_path,'w',encoding='utf-8').write(standalone)
os.makedirs(site,exist_ok=True)
page=base_head+pwa_head+'</head>\n<body>\n'+body+'\n'+sw_reg+'</body>\n</html>\n'
open(os.path.join(site,'index.html'),'w',encoding='utf-8').write(page)
open(os.path.join(site,'manifest.webmanifest'),'w').write('''{
  "name": "V60 Coffee",
  "short_name": "V60",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#0E1621",
  "theme_color": "#0E1621",
  "icons": [
    {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
''')
import hashlib
ver=hashlib.sha1(page.encode()).hexdigest()[:10]
open(os.path.join(site,'sw.js'),'w').write('''// Network first, so a new bean list shows as soon as you are online; cached copy when offline.
const CACHE='v60-%s';
const FILES=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(fetch(e.request).then(r=>{if(r.ok&&new URL(e.request.url).origin===location.origin){const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));}return r;}).catch(()=>caches.match(e.request,{ignoreSearch:true}).then(m=>m||caches.match('index.html'))));
});
'''%ver)
# icon: V60 cone dripping into a server, on the app background
def icon(n,path):
  S=4*n;im=Image.new('RGB',(S,S),(14,22,33));d=ImageDraw.Draw(im);u=S/100
  d.polygon([(22*u,24*u),(78*u,24*u),(58*u,58*u),(42*u,58*u)],outline=(234,242,248),width=int(4*u))
  d.polygon([(30*u,31*u),(70*u,31*u),(56*u,54*u),(44*u,54*u)],fill=(107,74,51))
  d.ellipse([47*u,62*u,53*u,68*u],fill=(210,155,108))
  d.polygon([(32*u,72*u),(68*u,72*u),(65*u,88*u),(35*u,88*u)],fill=(138,90,54),outline=(234,242,248),width=int(3*u))
  im.resize((n,n),Image.LANCZOS).save(path)
for n,f in [(192,'icon-192.png'),(512,'icon-512.png'),(180,'apple-touch-icon.png')]: icon(n,os.path.join(site,f))
print('built',ver)

// service-worker.js — gerado pelo Mini SK em 28/10/2026, 01:50:25
// Não precisa mexer: ele guarda sozinho o que o app usa.
const PREFIXO = 'sk-mini-sk-computador-27-10-b-1-';
const CACHE = PREFIXO + 'mvrmytwp';
// Lista feita automaticamente (para funcionar sem internet logo após instalar)
const GUARDAR = [
  "./",
  "./abrir.py",
  "./favicon.ico",
  "./ferramentas/aqui-ficam-o-python-e-o-node.txt",
  "./icons/apple-touch-icon.png",
  "./icons/icon-16.png",
  "./icons/icon-32.png",
  "./icons/icon-48.png",
  "./icons/icon-72.png",
  "./icons/icon-96.png",
  "./icons/icon-128.png",
  "./icons/icon-144.png",
  "./icons/icon-152.png",
  "./icons/icon-180.png",
  "./icons/icon-192.png",
  "./icons/icon-384.png",
  "./icons/icon-512.png",
  "./icons/icon.svg",
  "./icons/maskable-192.png",
  "./icons/maskable-512.png",
  "./icons/maskable.svg",
  "./index.html",
  "./INICIAR-MINI-SK.bat",
  "./LEIA-ME.txt",
  "./manifest.json",
  "./PLANO.md",
  "./RECEITA.md",
  "./www/css/app.css",
  "./www/favicon.ico",
  "./www/icons/apple-touch-icon.png",
  "./www/icons/icon-16.png",
  "./www/icons/icon-32.png",
  "./www/icons/icon-48.png",
  "./www/icons/icon-72.png",
  "./www/icons/icon-96.png",
  "./www/icons/icon-128.png",
  "./www/icons/icon-144.png",
  "./www/icons/icon-152.png",
  "./www/icons/icon-180.png",
  "./www/icons/icon-192.png",
  "./www/icons/icon-384.png",
  "./www/icons/icon-512.png",
  "./www/icons/icon.svg",
  "./www/icons/maskable-192.png",
  "./www/icons/maskable-512.png",
  "./www/icons/maskable.svg",
  "./www/index.html",
  "./www/js/00-core.js",
  "./www/js/04-conta.js",
  "./www/js/10-fs.js",
  "./www/js/20-zip.js",
  "./www/js/30-highlight.js",
  "./www/js/40-editor.js",
  "./www/js/50-tree.js",
  "./www/js/60-preview.js",
  "./www/js/61-tsx.js",
  "./www/js/70-search.js",
  "./www/js/80-ai.js",
  "./www/js/81-gasto.js",
  "./www/js/83-voz.js",
  "./www/js/84-ponte.js",
  "./www/js/85-checkpoints.js",
  "./www/js/86-terminal.js",
  "./www/js/86b-node.js",
  "./www/js/86c-termux.js",
  "./www/js/86e-atalhos.js",
  "./www/js/86f-pasta-viva.js",
  "./www/js/86g-largura.js",
  "./www/js/86h-node-extra.js",
  "./www/js/87-links.js",
  "./www/js/88-inventario.js",
  "./www/js/89-config.js",
  "./www/js/89b-cacador.js",
  "./www/js/90-github.js",
  "./www/js/91-acoes.js",
  "./www/js/91b-publicar.js",
  "./www/js/92-playground.js",
  "./www/js/92c-importar.js",
  "./www/js/93-conversa.js",
  "./www/js/94-fatiador.js",
  "./www/js/95-pwa.js",
  "./www/js/96-apk.js",
  "./www/js/96b-eas.js",
  "./www/js/96c-preparar.js",
  "./www/js/96d-exe-minisk.js",
  "./www/js/96e-exe-python.js",
  "./www/js/97-analise.js",
  "./www/js/97b-cacabug.js",
  "./www/js/97c-modularizar.js",
  "./www/js/98-api.js",
  "./www/js/99-app.js",
  "./www/js/lib/acorn.min.js",
  "./www/js/lib/expo-core.js",
  "./www/js/lib/jszip.min.js",
  "./www/js/lib/lab/30-analise.js",
  "./www/js/lib/lab/50-comparar.js",
  "./www/js/lib/nacl-fast.min.js",
  "./www/js/lib/picotador/00-base.js",
  "./www/js/lib/picotador/10-ler.js",
  "./www/js/lib/picotador/20-projetos.js",
  "./www/js/lib/picotador/30-mensagens.js",
  "./www/js/lib/plano-core.js",
  "./www/js/lib/ponte-termux.cjs.txt",
  "./www/js/lib/receita-core.js",
  "./www/js/lib/selar.js",
  "./www/LEIA-ME.md",
  "./www/manifest.json",
  "./www/service-worker.js",
  "./www/sw.js"
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => Promise.all(GUARDAR.map((u) => c.add(u).catch(() => null)))));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k.startsWith(PREFIXO) && k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// Primeiro a internet (sempre a versão nova); sem internet, a cópia guardada.
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(
    fetch(req).then((res) => {
      if (res.ok) { const copia = res.clone(); caches.open(CACHE).then((c) => c.put(req, copia)); }
      // Igual ao Workbox da Replit: página que não existe (rota do app) abre o index
      if (res.status === 404 && req.mode === 'navigate') return caches.match('./').then((r) => r || fetch('./'));
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then((r) => r || (req.mode === 'navigate' ? caches.match('./') : undefined)))
  );
});

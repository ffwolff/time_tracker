self.addEventListener('install', event => {
  console.log('[ServiceWorker] Instalado');
  event.waitUntil(
    caches.open('tracker-cache').then(cache => {
      return cache.addAll([
        '/',
        '/static/style.css',
        '/static/manifest.json'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});

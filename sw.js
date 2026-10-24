const CACHE_NAME = 'pwa-static-v22'; // Bump on every asset change so clients update
const ASSETS_TO_CACHE = [
  './',
  './normalize.css',
  './style.css',
  './manifest.json',
  './lula.webp',
  './flavio.webp',
  './favicon.ico',
  './apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png'
];

// 1. Install Event: Cache essential app shell files
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching app shell');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => self.skipWaiting())
  );
});

// 2. Activate Event: Clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Fetch Event: Cache-First for the app shell, everything else goes straight to the network
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // posts.json and externas.json are never cached: not calling respondWith lets the browser handle them untouched
  if (event.request.method !== 'GET' || url.pathname.endsWith('/posts.json') || url.pathname.endsWith('/externas.json')) return;

  event.respondWith(
    caches.match(event.request, { ignoreSearch: true })
      .then((cachedResponse) => cachedResponse || fetch(event.request))
  );
});

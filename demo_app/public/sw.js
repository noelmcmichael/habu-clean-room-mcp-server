// Disabled Service Worker - Forces fresh content
console.log('🚫 Service Worker disabled for cache refresh');

// Clear all caches and unregister
self.addEventListener('install', () => {
  console.log('🗑️ Clearing all caches...');
  caches.keys().then(cacheNames => {
    return Promise.all(
      cacheNames.map(cacheName => {
        console.log('Deleting cache:', cacheName);
        return caches.delete(cacheName);
      })
    );
  });
  self.skipWaiting();
});

self.addEventListener('activate', () => {
  console.log('✅ Cache clearing complete');
  self.clients.claim();
});

// Pass through all requests without caching
self.addEventListener('fetch', (event) => {
  event.respondWith(fetch(event.request));
});
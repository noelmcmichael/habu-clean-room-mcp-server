// Service Worker for Performance Optimization
// Implements intelligent caching strategy for faster loading

const CACHE_NAME = 'habu-app-v2.0-force-update';
const API_CACHE_NAME = 'habu-api-v2.0-force-update';

// Static assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/static/js/main.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico'
];

// API endpoints to cache with TTL
const CACHEABLE_APIS = [
  '/api/health',
  '/api/mcp/habu_enhanced_templates',
  '/api/mcp/habu_list_partners'
];

// Cache duration for different types of content
const CACHE_DURATION = {
  static: 24 * 60 * 60 * 1000,    // 24 hours
  api: 5 * 60 * 1000,             // 5 minutes
  templates: 10 * 60 * 1000,      // 10 minutes
  health: 2 * 60 * 1000           // 2 minutes
};

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker installing...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ Service Worker installed successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('❌ Service Worker installation failed:', error);
      })
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker activating...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
              console.log('🗑️ Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ Service Worker activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - implement caching strategy
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request));
    return;
  }
  
  // Handle static assets
  event.respondWith(handleStaticRequest(request));
});

// Handle API requests with cache-first strategy for specific endpoints
async function handleApiRequest(request) {
  const url = new URL(request.url);
  const pathname = url.pathname;
  
  // Check if this API is cacheable
  const isCacheable = CACHEABLE_APIS.some(api => pathname.includes(api));
  
  if (!isCacheable) {
    // For non-cacheable APIs (like chat), always go to network
    try {
      return await fetch(request);
    } catch (error) {
      console.error('❌ Network request failed:', error);
      return new Response(
        JSON.stringify({ error: 'Network error', offline: true }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }
  
  // For cacheable APIs, use cache-first with TTL
  try {
    const cache = await caches.open(API_CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      const cacheTime = cachedResponse.headers.get('sw-cache-time');
      if (cacheTime) {
        const age = Date.now() - parseInt(cacheTime);
        const maxAge = getCacheMaxAge(pathname);
        
        if (age < maxAge) {
          console.log('📱 Serving from cache:', pathname);
          return cachedResponse;
        }
      }
    }
    
    // Cache miss or expired - fetch from network
    console.log('🌐 Fetching from network:', pathname);
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Clone response and add cache timestamp
      const responseToCache = networkResponse.clone();
      const headers = new Headers(responseToCache.headers);
      headers.set('sw-cache-time', Date.now().toString());
      
      const cachedResponseInit = {
        status: responseToCache.status,
        statusText: responseToCache.statusText,
        headers: headers
      };
      
      const body = await responseToCache.arrayBuffer();
      const cachedResponse = new Response(body, cachedResponseInit);
      
      // Cache the response
      await cache.put(request, cachedResponse.clone());
      console.log('💾 Cached API response:', pathname);
      
      return cachedResponse;
    }
    
    return networkResponse;
    
  } catch (error) {
    console.error('❌ API request failed:', error);
    
    // Try to serve stale cache as fallback
    const cache = await caches.open(API_CACHE_NAME);
    const staleResponse = await cache.match(request);
    
    if (staleResponse) {
      console.log('📦 Serving stale cache as fallback:', pathname);
      return staleResponse;
    }
    
    return new Response(
      JSON.stringify({ error: 'Service unavailable', offline: true }),
      { status: 503, headers: { 'Content-Type': 'application/json' } }
    );
  }
}

// Handle static requests with cache-first strategy
async function handleStaticRequest(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      console.log('📦 Serving static asset from cache:', request.url);
      return cachedResponse;
    }
    
    // Not in cache - fetch and cache
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      await cache.put(request, networkResponse.clone());
      console.log('💾 Cached static asset:', request.url);
    }
    
    return networkResponse;
    
  } catch (error) {
    console.error('❌ Static request failed:', error);
    
    // For navigation requests, return a basic offline page
    if (request.mode === 'navigate') {
      return new Response(
        `<!DOCTYPE html>
         <html><head><title>Offline</title></head>
         <body><h1>You're offline</h1><p>Please check your connection.</p></body>
         </html>`,
        { headers: { 'Content-Type': 'text/html' } }
      );
    }
    
    return new Response('Offline', { status: 503 });
  }
}

// Get cache duration based on endpoint
function getCacheMaxAge(pathname) {
  if (pathname.includes('health')) {
    return CACHE_DURATION.health;
  } else if (pathname.includes('templates')) {
    return CACHE_DURATION.templates;
  } else if (pathname.startsWith('/api/')) {
    return CACHE_DURATION.api;
  }
  return CACHE_DURATION.static;
}

// Message handling for cache management
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            console.log('🗑️ Clearing cache:', cacheName);
            return caches.delete(cacheName);
          })
        );
      }).then(() => {
        event.ports[0].postMessage({ success: true });
      }).catch((error) => {
        console.error('❌ Cache clear failed:', error);
        event.ports[0].postMessage({ success: false, error: error.message });
      })
    );
  }
});
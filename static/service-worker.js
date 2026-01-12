/**
 * VEO AUTOMATOR - Service Worker
 * Permite funcionamento offline (PWA)
 */

const CACHE_NAME = 'veo-automator-v1';
const urlsToCache = [
  '/',
  '/static/style.css',
  '/static/script.js',
  '/static/manifest.json'
];

// Instalação - cachear arquivos
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache aberto');
        return cache.addAll(urlsToCache);
      })
  );
});

// Ativação - limpar cache antigo
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Removendo cache antigo:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch - servir do cache quando offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Retorna do cache se encontrado
        if (response) {
          return response;
        }
        // Senão, busca da rede
        return fetch(event.request);
      })
  );
});

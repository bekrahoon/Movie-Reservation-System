{% load static %}
/* Cinema 4D service worker.
   Served from "/service-worker.js" (see config/urls.py) so its scope is "/". */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/7.1.0/workbox-sw.js");

const CACHE_VERSION = "v1";
workbox.core.setCacheNameDetails({ prefix: "cinema4d", suffix: CACHE_VERSION });
workbox.core.clientsClaim();

// ---------------------------------------------------------------------
// 1. Precache the app shell (CSS/JS used on every page + offline page +
//    icons referenced by the manifest).
// ---------------------------------------------------------------------
workbox.precaching.precacheAndRoute([
    { url: "{% static 'style.css' %}", revision: "{{ CACHE_VERSION }}" },
    { url: "{% static 'css/auth.css' %}", revision: "{{ CACHE_VERSION }}" },
    { url: "{% static 'img/icons/icon-192x192.png' %}", revision: "{{ CACHE_VERSION }}" },
    { url: "{% static 'img/icons/icon-512x512.png' %}", revision: "{{ CACHE_VERSION }}" },
    { url: "/offline/", revision: "{{ CACHE_VERSION }}" },
]);

self.addEventListener("install", () => self.skipWaiting());

// ---------------------------------------------------------------------
// 2. Static assets (CSS/JS/fonts/images served from /static/) ->
//    Stale-While-Revalidate: instant from cache, refreshed in background.
// ---------------------------------------------------------------------
workbox.routing.registerRoute(
    ({ url }) => url.pathname.startsWith("/static/"),
    new workbox.strategies.StaleWhileRevalidate({
        cacheName: "static-resources",
        plugins: [
            new workbox.expiration.ExpirationPlugin({
                maxEntries: 200,
                maxAgeSeconds: 30 * 24 * 60 * 60, // 30 days
            }),
        ],
    })
);

// ---------------------------------------------------------------------
// 3. Movie posters / media uploads -> Cache-First (rarely change once
//    uploaded), with an entry/size limit so the cache doesn't grow forever.
// ---------------------------------------------------------------------
workbox.routing.registerRoute(
    ({ url }) => url.pathname.startsWith("/media/"),
    new workbox.strategies.CacheFirst({
        cacheName: "media-posters",
        plugins: [
            new workbox.expiration.ExpirationPlugin({
                maxEntries: 100,
                maxAgeSeconds: 14 * 24 * 60 * 60, // 14 days
                purgeOnQuotaError: true,
            }),
        ],
    })
);

// ---------------------------------------------------------------------
// 4. Read-only "browse" pages (home, movie detail, genres, search) ->
//    Network-First so logged-in users always see fresh showtimes/seat
//    availability, but a cached copy is shown when offline.
// ---------------------------------------------------------------------
const browsePageMatcher = ({ request, url }) =>
    request.mode === "navigate" &&
    (url.pathname === "/" ||
        url.pathname.startsWith("/movies/") ||
        url.pathname.startsWith("/movies_genre/") ||
        url.pathname.startsWith("/movies_search/") ||
        url.pathname.startsWith("/genres/") ||
        url.pathname.startsWith("/about_us/"));

workbox.routing.registerRoute(
    browsePageMatcher,
    new workbox.strategies.NetworkFirst({
        cacheName: "pages",
        networkTimeoutSeconds: 4,
        plugins: [
            new workbox.expiration.ExpirationPlugin({
                maxEntries: 50,
                maxAgeSeconds: 24 * 60 * 60, // 1 day
            }),
        ],
    })
);

// ---------------------------------------------------------------------
// 5. Everything else that mutates state or is user/account specific
//    (cart, bookings, checkout, login/register, admin, API writes)
//    bypasses the service worker entirely -> always network.
// ---------------------------------------------------------------------
const noCacheMatcher = ({ url }) =>
    url.pathname.startsWith("/cart") ||
    url.pathname.startsWith("/bookings") ||
    url.pathname.startsWith("/admin") ||
    url.pathname.startsWith("/api/") ||
    url.pathname.startsWith("/accounts") ||
    url.pathname.startsWith("/login") ||
    url.pathname.startsWith("/register") ||
    url.pathname.startsWith("/logout");

workbox.routing.registerRoute(noCacheMatcher, new workbox.strategies.NetworkOnly());

// ---------------------------------------------------------------------
// 6. Offline fallback for navigations that fail completely (no cache hit
//    and no network), e.g. a booking page opened for the first time
//    while offline.
// ---------------------------------------------------------------------
workbox.routing.setCatchHandler(async ({ event }) => {
    if (event.request.mode === "navigate") {
        return caches.match("/offline/");
    }
    return Response.error();
});

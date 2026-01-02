// Intercept fetch calls to return embedded data
(function() {
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
        if (url.includes('config.json')) {
            return Promise.resolve({
                ok: true,
                json: () => Promise.resolve(window.ACTIVE_CONFIG)
            });
        }
        if (url.includes('events.json')) {
            return Promise.resolve({
                ok: true,
                json: () => Promise.resolve({events: window.ACTIVE_EVENTS})
            });
        }
        if (url.includes('content.json')) {
            const content = url.includes('.de.') ? window.EMBEDDED_CONTENT_DE : window.EMBEDDED_CONTENT_EN;
            return Promise.resolve({
                ok: true,
                json: () => Promise.resolve(content)
            });
        }
        return originalFetch.apply(this, arguments);
    };
})();

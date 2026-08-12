(function () {
    "use strict";

    const telegram = window.Telegram?.WebApp;

    if (!telegram) {
        console.warn("Telegram WebApp mavjud emas.");
        return;
    }

    telegram.ready();
    telegram.expand();

    const initData = telegram.initData;

    if (!initData) {
        console.warn("Telegram WebApp initData mavjud emas.");
        return;
    }

    window.NovaHubTelegram = {
        initData: initData,

        headers() {
            return {
                "X-Telegram-Init-Data": initData,
                "Content-Type": "application/json",
            };
        },

        async fetch(url, options = {}) {
            const headers = {
                ...this.headers(),
                ...(options.headers || {}),
            };

            return window.fetch(url, {
                ...options,
                headers,
            });
        },
    };
})();

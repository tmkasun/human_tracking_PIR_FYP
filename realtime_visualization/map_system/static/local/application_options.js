var ApplicationOptions = {
    constance: {
        WEB_SOCKET_SERVER: 'localhost',
        WEB_SOCKET_PORT: 8001,

        /* Django Static Url */
        STATIC_URL: '/static/',

        NOTIFY_INFO_TIMEOUT: 3000,
        NOTIFY_SUCCESS_TIMEOUT: 4000,
        NOTIFY_WARNING_TIMEOUT: 3000,
        NOTIFY_DANGER_TIMEOUT: 9000
    },
    messages: {
        app: {}
    },
    locale: {
        type: 'sin',
        sin: {
            websocket: {
                errors: {
                    'connection': 'වෙබ් සොකට් සම්බන්ධතාවය විසන්ඳිවී ඇත කරුණාකර ඔබගේ අන්තර්ජාල සබදතාවය පරීක්ශාකර බලන්න  '
                }
            }
        },
        eng: {
            websockt: {
                errors: {
                    'connection': 'Something went wrong when trying to connect to WebSocket </br> <b>Please check your internet or Network connection<b/>'
                }
            }

        }
    }
};
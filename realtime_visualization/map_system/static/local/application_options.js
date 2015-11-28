var ApplicationOptions = {
    colors: {
        states: {
            NORMAL: 'blue',
            WARNING: 'orange',
            OFFLINE: 'grey',
            ALERTED: 'red',
            UNKNOWN: 'black' // TODO: previous color #19FFFF , change this if black is not user friendly ;)
        },
        application: {
            header: 'grey'
        }
    },
    constance:{
        WEB_SOCKET_SERVER: 'aws4.knnect.com',
        WEB_SOCKET_PORT: 9764,
        CEP_WEB_SOCKET_OUTPUT_ADAPTOR_NAME: 'DefaultWebsocketOutputAdaptor',
        CEP_WEB_SOCKET_BUILDER_TOPIC: 'geoDataEndPoint',

        /* Django Static Url */
        STATIC_URL: '/static/',

        SPEED_HISTORY_COUNT: 20,
        NOTIFY_INFO_TIMEOUT: 3000,
        NOTIFY_SUCCESS_TIMEOUT: 4000,
        NOTIFY_WARNING_TIMEOUT: 3000,
        NOTIFY_DANGER_TIMEOUT: 9000
    },
    messages:{
        app:{

        }
    },
    leaflet: {
        iconUrls: {
            normalIcon: '/static/images/markers/arrow_normal.png',
            alertedIcon: '/static/images/markers/arrow_alerted.png',
            offlineIcon: '/static/images/markers/arrow_offline.png',
            warningIcon: '/static/images/markers/arrow_warning.png',
            defaultIcon: '/static/images/markers/default_icons/marker-icon.png',
            resizeIcon: '/static/images/markers/resize.png'

        }
    },
    locale: {
        type: 'sin',
        sin: {
            websocket:{
                errors:{
                    'connection': 'වෙබ් සොකට් සම්බන්ධතාවය විසන්ඳිවී ඇත කරුණාකර ඔබගේ අන්තර්ජාල සබදතාවය පරීක්ශාකර බලන්න  '
                }
            }
        },
        eng: {
            websockt: {
                errors:{
                    'connection': 'Something went wrong when trying to connect to WebSocket </br> <b>Please check your internet or Network connection<b/>'
                }
            }

        }
    }
};
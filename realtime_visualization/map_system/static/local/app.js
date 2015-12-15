/*Application configurations*/

/**
 * Initialize leaflet map object
 * Set offcanvas menu hide when click on map layer by using 'map.on(click)' event tracer
 */

var defaultOSM = L.tileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 22,
    attribution: 'Map data © OpenStreetMap contributors <a href="http://openstreetmap.org/" target="_blank">Openstreetmap</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">. Map data (c) <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> contributors, CC-BY-SA.'
});

var baseLayers = {
    "Open Street Maps": defaultOSM
};
function initializeMap() {
    if (typeof(map) !== 'undefined') {
        map.remove();
    }
    map = L.map("map", {
        zoom: 20,
        center: [7.07094249382,79.96429187961],
        layers: [defaultOSM],
        zoomControl: false,
        attributionControl: false,
        maxZoom: 29,
        maxNativeZoom: 19,
        worldCopyJump: true
    });

    map.on('click', function (e) {
        $.UIkit.offcanvas.hide();//[force = false] no animation
    });
}

/**
 * Set view port to current browser location , if user allowed to share location
 * @param {float[]} position
 */
function success(position) {
    var browserLatitude = position.coords.latitude;
    var browserLongitude = position.coords.longitude;
    //map.setView([browserLatitude, browserLongitude]);
    //map.setZoom(20);


    $.UIkit.notify({
        message: "Map view set to browser's location",
        status: 'info',
        timeout: ApplicationOptions.constance.NOTIFY_INFO_TIMEOUT,
        pos: 'top-center'
    });
};

/**
 * Show error message if unable to get browser location
 */
function error() {
    $.UIkit.notify({
        message: "Unable to find browser location!",
        status: 'warning',
        timeout: ApplicationOptions.constance.NOTIFY_WARNING_TIMEOUT,
        pos: 'top-center'
    });
};

/**
 * Change map attribution text, Attribution link is in Bottom Right corner
 * @param e
 */
function updateAttribution(e) {
    $.each(map._layers, function (index, layer) {
        if (layer.getAttribution) {
            $("#attribution").html((layer.getAttribution()));
        }
    });
}

/**
 *
 * @param objectId - Spatial object id , received from websocket
 * @returns {boolean}
 *
 * TODO: when click on a notification alert ? "Uncaught ReferenceError: KM is not defined "
 */
var toggled = false;
function focusOnSpatialObject(objectId) {

    var spatialObject = currentSpatialObjects[objectId];// (local)
    if (!spatialObject) {
        $.UIkit.notify({
            message: "Spatial Object <span style='color:red'>" + objectId + "</span> not in the Map!!",
            status: 'warning',
            timeout: ApplicationOptions.constance.NOTIFY_WARNING_TIMEOUT,
            pos: 'top-center'
        });
        return false;
    }
    clearFocus(); // Clear current focus if any
    selectedSpatialObject = objectId; // (global) Why not use 'var' other than implicit declaration http://stackoverflow.com/questions/1470488/what-is-the-function-of-the-var-keyword-and-when-to-use-it-or-omit-it#answer-1471738

    map.setView(spatialObject.marker.getLatLng(), 17, {animate: true}); // TODO: check the map._layersMaxZoom and set the zoom level accordingly

    $('#objectInfo').find('#objectInfoId').html(selectedSpatialObject);
    spatialObject.marker.openPopup();
    if (!toggled) {
        $('#objectInfo').animate({width: 'toggle'}, 100);
        toggled = true;
    }
    getAlertsHistory(objectId);
    spatialObject.drawPath();
    setTimeout(function () {
        createChart();
        chart.load({columns: [spatialObject.speedHistory.getArray()]});
    }, 100);
}

/**
 * Unfocused on current searched spatial object, Remove drawn history path, close opened popup and set selectedSpatialObject to null
 */
function clearFocus() {
    if (selectedSpatialObject) {
        spatialObject = currentSpatialObjects[selectedSpatialObject];
        spatialObject.removePath();
        spatialObject.marker.closePopup();
        selectedSpatialObject = null;
    }
}

/**
 * Close all opened modal(s) and hide offcanvas
 */
function closeAll() {
    $('.modal').modal('hide');
    setTimeout(function () {
        $.UIkit.offcanvas.hide()
    }, 100);
}

/**
 * Create C3 chart for display speed variations, in last (20) received events
 */
var chart;
function createChart() {
    chart = c3.generate({
        bindto: '#chart_div',
        data: {
            columns: [
                ['speed']
            ]
        },
        subchart: {
            show: true
        },
        axis: {
            y: {
                label: {
                    text: 'Speed',
                    position: 'outer-middle'
                }
            }
        },
        legend: {
            show: false
        }
    });
}

/**
 * Notify a message when an AJAX call is made to back end
 * @param message {String} - message need to be displayed
 */
function notifyAlert(message, status) {
    if (typeof status === 'undefined') {
        status = 'warning';
    }
    return $.UIkit.notify({
        message: "Alert: " + message,
        status: status,
        timeout: 600, // Show infinitely until close otherwise
        pos: 'bottom-left'
    });
}

/**
 *
 * @param message {String} - Message need to be displaying
 * @param status {String} - $.Notify Status code { info, success ,warning ,danger }
 *
 */
var ajaxNotifySettings = null;
// TODO: Make an prototype and give available options list rather than hard typing them , who know what are there?
function setAjaxNotify(message, status) {
    if (typeof status === 'undefined') {
        status = 'warning';
    }
    ajaxNotifySettings = {
        'message': message,
        'status': status
    };
}

var ajaxNotifyObject;
$(document).on({
    ajaxStart: function () {
        if (!ajaxNotifySettings) return;

        ajaxNotifyObject = notifyAlert(ajaxNotifySettings['message'], ajaxNotifySettings['status']);

    },
    ajaxStop: function () {
        if (!ajaxNotifyObject) return;

        ajaxNotifyObject.status(ajaxNotifySettings['status']);
        ajaxNotifyObject.content(ajaxNotifySettings['message']);
        setTimeout(function () {
            ajaxNotifyObject.close();
            ajaxNotifyObject = null;
            ajaxNotifySettings = null;
        }, ApplicationOptions.constance.NOTIFY_INFO_TIMEOUT);
    }
});

var map;
initializeMap();



///static/local/faculty.json

    $.getJSON("/static/local/home.json", function (geoJSON) {
        //return false;
        var indoorLayer = new L.Indoor(geoJSON, {
            getLevel: function (feature) {
                return 0;
                //if (feature.properties.relations.length === 0)
                //    return null;

                //return feature.properties.relations[0].reltags.level;
            },
            onEachFeature: function (feature, layer) {
                //layer.bindPopup(JSON.stringify(feature.properties, null, 4));
            },
            style: function (feature) {
                var fill = 'white';
                //console.log(feature.properties.tags["building:part"]);
                if (feature.properties.tags["building:part"] === 'corridor') {
                    fill = '#169EC6';
                } else if (feature.properties.tags["building:part"] === 'room') {
                    fill = 'blue';
                }
                return {
                    fillColor: fill,
                    weight: 1,
                    color: '#666',
                    fillOpacity: 1
                };
            }
        });

        indoorLayer.setLevel("0");

        indoorLayer.addTo(map);

        var levelControl = new L.Control.Level({
            level: "0",
            levels: indoorLayer.getLevels()
        });

        // Connect the level control to the indoor layer
        levelControl.addEventListener("levelchange", indoorLayer.setLevel, indoorLayer);

        levelControl.addTo(map);
    });





var attributionControl = L.control({
    position: "bottomright"
});

attributionControl.onAdd = function (map) {
    var div = L.DomUtil.create("div", "leaflet-control-attribution");
    div.innerHTML = "<a href='#' onclick='$(\"#attributionModal\").modal(\"show\"); return false;'>Attribution</a>";
    return div;
};

map.on("layeradd", updateAttribution);
map.on("layerremove", updateAttribution);

$("#loading").hide();

navigator.geolocation.getCurrentPosition(success, error);
map.addControl(attributionControl);

/**
 * Add full screen plugin to map
 */
L.control.fullscreen({
    position: 'bottomright'
}).addTo(map);
L.control.zoom({
    position: "bottomright"
}).addTo(map);


var groupedOverlays = {
    "Web Map Service layers": {}
};

var layerControl = L.control.groupedLayers(baseLayers, groupedOverlays, {
    collapsed: true
}).addTo(map);

var setupWizard;
// wizard with it's cards initialization.
$(function () {
    var options = {submitUrl: "controllers/setup_dashboard.jag"};
    setupWizard = $("#setup_dashboard").wizard(options);
});


$(".modal").draggable({
    handle: ".modal-header"
});

//Clear modal content for reuse the wrapper by other functions
$('body').on('hidden.bs.modal', '.modal', function (modal) {
    $(this).removeData('bs.modal');
});


/* TypeAhead search functionality */

/* Highlight search box text on click */
$("#searchbox").click(function () {
    $(this).select();
});

var substringMatcher = function () {
    return function findMatches(q, cb) {
        var matches, substrRegex;
        matches = [];
        substrRegex = new RegExp(q, 'i');
        $.each(currentSpatialObjects, function (i, str) {
            if (substrRegex.test(i)) {
                matches.push({value: i});
            }
        });

        cb(matches);
    };
};

$('#searchbox').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'speed',
        displayKey: 'value',
        source: substringMatcher()
    }).on('typeahead:selected', function ($e, datum) {
        objectId = datum['value'];
        focusOnSpatialObject(objectId)
    });


// TODO: Remove tile server and web map service import calls if not in use
//getTileServers();
//getWms();

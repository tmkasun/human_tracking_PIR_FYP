/* All the remote calls to backend server*/

/* close all opened modals and side pane */

function addTileUrl() {
    /* TODO: add validation, check for empty url and names*/
    var tileUrl = $('#tileUrl').val();
    var urlName = $('#tileName').val();
    var maxzoom = $('#maxzoom').val();
    subdomains = $('#sub_domains').val();
    var attribution = $('#data_attribution').val();
    /* Add to base layers*/
    var newTileLayer = L.tileLayer(tileUrl, {
        maxZoom: parseInt(maxzoom),
        subdomains: subdomains.split(','),
        attribution: attribution
    });
    layerControl.addBaseLayer(newTileLayer, urlName);

    inputs = layerControl._form.getElementsByTagName('input');
    inputsLen = inputs.length;
    for (i = 0; i < inputsLen; i++) {
        input = inputs[i];
        obj = layerControl._layers[input.layerId];
        if (layerControl._map.hasLayer(obj.layer)) {
            map.removeLayer(obj.layer);
        }
    }
    map.addLayer(newTileLayer);

    /* Do ajax save */
    var data = {
        url: tileUrl,
        'name': urlName,
        'attribution': attribution,
        'maxzoom': maxzoom,
        'subdomains': subdomains
    };
    var serverUrl = "controllers/tile_servers.jag";
    // TODO: If failure happens notify user about the error message
    $.post(serverUrl, data, function (response) {
        $.UIkit.notify({
            message: '<span style="color: dodgerblue">' + response + '</span>',
            status: 'success',
            timeout: ApplicationOptions.constance.NOTIFY_SUCCESS_TIMEOUT,
            pos: 'top-center'
        });
        closeAll();
    });

// TODO: Show a preview of newly added tileserver map
//    var mapPreview = L.map('mapPreview', {
//        zoom: 10,
//        center: [6.934846, 79.851980],
//    });
//    L.tileLayer(tileUrl).addTo(mapPreview);

}

function addWmsEndPoint() {
    serviceName = $('#serviceName').val();
    layers = $('#layers').val();
    wmsVersion = $('#wmsVersion').val();
    serviceEndPoint = $('#serviceEndPoint').val();
    outputFormat = $('#outputFormat').val();

    wmsLayer = L.tileLayer.wms(serviceEndPoint, {
        layers: layers.split(','),
        format: outputFormat ? outputFormat : 'image/png',
//        version: wmsVersion,
        transparent: true,
        opacity: 0.4
    });

    layerControl.addOverlay(wmsLayer, serviceName, "Web Map Service layers");
    map.addLayer(wmsLayer);
    var data = {
        'serviceName': serviceName,
        'layers': layers,
        'wmsVersion': wmsVersion,
        'serviceEndPoint': serviceEndPoint,
        'outputFormat': outputFormat
    };
    var serverUrl = "controllers/wms_endpoints.jag";
    // TODO: If failure happens notify user about the error message
    $.post(serverUrl, data, function (response) {
        $.UIkit.notify({
            message: '<span style="color: dodgerblue">' + response + '</span>',
            status: 'success',
            timeout: ApplicationOptions.constance.NOTIFY_SUCCESS_TIMEOUT,
            pos: 'top-center'
        });
        closeAll();
    });
}
/**
 * Send new speed limit global value to back-end via post
 * CSRF has been used to prevvent man of the middle type of attacks , see `map_service/views.py#proximity_alert` for more infomation
 */
function setSpeedAlert() {
    var speedAlertValue = $("#speedAlertValue").val();
    data = { // TODO: change content type to app/json
        'speedAlertValue': speedAlertValue
        //'parseData': JSON.stringify({'speedAlertValue': speedAlertValue}), // parseKey : parseValue pair , this key pair is replace with the key in the template file
        //'executionPlan': 'speed',
        //'customName': null,
        //'cepAction': 'edit' // TODO: what if setting speed alert for the first time ?? that should be a deployment ? try 'edit' if fails 'deploy' , need to handle at the jaggery back end
    };
    setAjaxNotify("Setting new speed alert...");
    $.post('/map_service/set_speed_alert', data, function (response) {
        setAjaxNotify("Successfully set new speed limit", 'success');

    }, 'json');
}

/**
 * Send GeoJson of the selected area by the user to the back-end server
 * */
function setWithinAlert(leafletId) {
    /*
     * TODO: replace double quote to single quote because of a conflict when deploying execution plan in CEP
     * this is against JSON standards so has been re-replaced when getting the data from governance registry
     * (look in get_alerts for .replace() method)
     * */
    var selectedAreaGeoJson = JSON.stringify(map._layers[leafletId].toGeoJSON().geometry).replace(/"/g, "'");
    var queryName = $("#queryName").val();
    var areaName = $("#areaName").val();
    var data = {
        'geoFenceGeoJSON': selectedAreaGeoJson,
        'areaName': areaName, // TODO: fix , When template copies there can be two queryName and areaName id elements in the DOM
        'queryName': queryName
    };
    console.log('DEBUG: Reached this point');
    setAjaxNotify("Applying new geo-fence area...");
    $.post('/map_service/set_geofence', data, function (response) {
        setAjaxNotify("New geo-fence added to the system successfully...",'success');
        closeTools(leafletId);
    }, 'json');
}

function setStationeryAlert(leafletId) {
    /*
     * TODO: replace double quote to single quote because of a conflict when deploying execution plan in CEP
     * this is against JSON standards so has been re-replaced when getting the data from governance registry
     * (look in get_alerts for .replace() method)
     * */
    var selectedAreaGeoJson = map._layers[leafletId].toGeoJSON().geometry;

    //if a circle is drawn adding radius for the object
    if (selectedAreaGeoJson.type == "Point") {

        var radius = map._layers[leafletId]._mRadius;
        selectedAreaGeoJson["radius"] = radius;
    }

    var selectedProcessedAreaGeoJson = JSON.stringify(selectedAreaGeoJson).replace(/"/g, "'");

    var queryName = $("#queryName").val();
    var stationeryName = $("#areaName").val();
    var time = $("#time").val();
    var data = {
        'parseData': JSON.stringify({
            'geoFenceGeoJSON': selectedProcessedAreaGeoJson,
            'executionPlanName': _createExecutionPlanName(queryName, "Stationery"),
            'stationeryName': stationeryName,
            'stationeryTime': time
        }),
        'executionPlan': 'stationery',
        'customName': stationeryName, // TODO: fix , When template copies there can be two queryName and areaName id elements in the DOM
        'queryName': queryName,
        'cepAction': 'deploy'
    };
    $.post('controllers/set_alerts.jag', data, function (response) {
        $.UIkit.notify({
            message: '<span style="color: dodgerblue">' + response.status + '</span><br>' + response.message,
            status: (response.status == 'success' ? 'success' : 'danger'),
            timeout: 3000,
            pos: 'top-center'
        });
        closeAll();
        closeTools(leafletId);
    }, 'json');
}

function removeGeoFence(geoFenceElement, id) {
    var queryName = $(geoFenceElement).attr('data-queryName');
    var areaName = $(geoFenceElement).attr('data-areaName');

    data = {
        'executionPlanName': _createExecutionPlanName(queryName, id),
        'queryName': queryName,
        'cepAction': 'undeploy',
        'alertType': id

    };
    $.post('controllers/remove_alerts.jag', data, function (response) {
        $.UIkit.notify({
            message: '<span style="color: dodgerblue">' + response.status + '</span><br>' + response.message,
            status: (response.status == 'success' ? 'success' : 'danger'),
            timeout: 3000,
            pos: 'top-center'
        });
        closeAll();
    }, 'json');
}

function getAlertsHistory(objectId) {
    $.getJSON("controllers/get_alerts_history.jag?objectId=" + objectId, function (data) {
        var alertsContainer = $('#showAlertsArea').empty();
        $.each(data, function (key, val) {
            var alertDOMElement = document.createElement('a'); // Reason for using document.createElement (performance issue) http://stackoverflow.com/questions/268490/jquery-document-createelement-equivalent
            // TODO: define central state definition if needed to cahnge then it would be only one place change, same state switch has been used in websocket , spatialObject prototype
            switch (val.state) {
                case "NORMAL":
//                    $(alertDOMElement).addClass("list-group-item list-group-item-info");
                    return;
                case "WARNING":
                    $(alertDOMElement).addClass("list-group-item list-group-item-warning");
                    break;
                case "ALERTED":
                    $(alertDOMElement).addClass("list-group-item list-group-item-danger");
                    break;
                case "OFFLINE":
                    $(alertDOMElement).addClass("list-group-item list-group-item-success");
                    break;
            }
            $(alertDOMElement).html(val.information);
            $(alertDOMElement).css({marginTop: "5px"});
            $(alertDOMElement).attr('onClick', 'showAlertInMap(this)');

            // Set HTML5 data attributes for later use
            $(alertDOMElement).attr('data-id', val.id);
            $(alertDOMElement).attr('data-latitude', val.latitude);
            $(alertDOMElement).attr('data-longitude', val.longitude);
            $(alertDOMElement).attr('data-state', val.state);
            $(alertDOMElement).attr('data-information', val.information);

            alertsContainer.append(alertDOMElement);
        });
    });
}

/**
 * Send new proximity function arguments to backend
 */
function setProximityAlert() {
    var proximityDistance = $("#proximityDistance").val();
    var proximityTime = $("#proximityTime").val();
    var data = {
        /*
         TODO: Remove if nolonger needed, Stringify is not nessasay, Current architecture(V 1.1) do not requires execution plan parameter
         'parseData': JSON.stringify({'proximityTime': proximityTime,'proximityDistance': proximityDistance}),
         'executionPlan': 'proximity',
         'customName': null,
         'cepAction': 'edit',
         */
        'proximityTime': proximityTime,
        'proximityDistance': proximityDistance
    };
    setAjaxNotify("Setting new Proximity alert...");
    // TODO: Use django composer
    $.post('/map_service/set_proximity_alert', data, function (response) {
        setAjaxNotify("Successfully set new Proximity limit", 'success');
    }, 'json');
}

function _createExecutionPlanName(queryName, id) {

    if (id == "WithIn") {
        return 'geo_within' + (queryName ? '_' + queryName : '') + '_alert'; // TODO: value of the `queryName` can't be empty, because it will cause name conflicts in CEP, have to do validation(check not empty String)
    }
    else if (id == "Stationery") {
        return 'geo_stationery' + (queryName ? '_' + queryName : '') + '_alert'; // TODO: value of the `queryName` can't be empty, because it will cause name conflicts in CEP, have to do validation(check not empty String)
    }

}

// TODO: DEPRECATED method
function getTileServers() {
    //For reference: returning JSON from server
    // {"serverId" : 44, "url" : "ffsafsa", "name" : "sadsa", "subdomains" : "asfasfsa", "attribution" : "dsfdsfdsf", "maxzoom" : 12}
    $.getJSON("controllers/tile_servers.jag?serverId=all", function (data) {
        $.each(data, function (key, val) {
            $.UIkit.notify({
                message: 'Loading... <span style="color: #ccfcff">' + val.name + '</span>' +
                ' URL: <span style="color: #00ff00">' + val.url + '</span>',
                status: 'info',
                timeout: ApplicationOptions.constance.NOTIFY_INFO_TIMEOUT,
                pos: 'bottom-left'
            });
            //baseLayers[val.name]
            var newTileLayer = L.tileLayer(
                val.url, {
                    maxZoom: val.maxzoom, // TODO: if no maxzoom level do not set this attribute
                    subdomains: val.subdomains.split(','), // TODO: if no subdomains do not set this attribute
                    attribution: val.attribution
                }
            );
            layerControl.addBaseLayer(newTileLayer, val.name); // TODO: implement single method for #20  and this and do validation
        });
    });

}

// TODO: DEPRECATED method
function getWms() {
    // For refference {"wmsServerId" : 1, "serviceUrl" : "http://{s}.somedomain.com/blabla/{z}/{x}/{y}.png", "name" : "Sample server URL", "layers" : "asdsad,sd,adasd,asd", "version" : "1.0.2", "format" : "sadasda/asdas"}
    $.getJSON("controllers/wms_endpoints.jag?serverId=all", function (data) {
        $.each(data, function (key, val) {

            wmsLayer = L.tileLayer.wms(val.serviceUrl, {
                layers: val.layers.split(','),
                format: val.format ? val.format : 'image/png',
                version: val.version,
                transparent: true,
                opacity: 0.4
            });
            layerControl.addOverlay(wmsLayer, val.name, "Web Map Service layers");
        });
    });
}

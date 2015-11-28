/**
 *
 * @param {DOM} alertData
 */
function showAlertInMap(alertData) {
    clearFocus();

    var id = $(alertData).attr("data-id");
    var latitude = $(alertData).attr("data-latitude");
    var longitude = $(alertData).attr("data-longitude");
    var state = $(alertData).attr("data-state");
    var information = $(alertData).attr("data-information");

    var alertLatLngPoint = L.latLng(latitude,longitude);

    var alertOccouredArea = L.circle(alertLatLngPoint, 10, {
        color: '#FF9900',
        fillColor: '#FF00FF',
        fillOpacity: 0.5
    }).addTo(map);

    alertOccouredArea.bindPopup("Id: <b>"+id+"</b><br>"+
            "State: <b>"+state+"</b><br>"+
            "Information: <b>"+information+"</b><br>"
    ).openPopup();
    $(alertOccouredArea._popup._closeButton).on("click",function(){map.removeLayer(alertOccouredArea)});
    map.setView(alertLatLngPoint,18);

    /* TODO: for reference <Update lib or remove if not in use>: This `R`(RaphaelLayer: https://github.com/dynmeth/RaphaelLayer) library is dam buggy can't use it reliably */
    /*
    var alertPulse = new R.Pulse(
     alertLatLngPoint,
     8,
     {'stroke': '#FF9E0E', 'fill': '#FF0000'},
     {'stroke': '#FF3E2F', 'stroke-width': 3});
     map.addLayer(alertPulse);
     */


}
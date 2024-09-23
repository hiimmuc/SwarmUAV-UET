// Where you want to render the map.

var map;

var markers = [];

var LeafIcon;

function initialize() {
    var element = document.getElementById('mapid');

    map = L.map(element).setView([21.064862, 105.792958], 16);

    // streets:   'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    // hybrid:    'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}'
    // Satellite: 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    // Terrain:   'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}'
    // OSM:       'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

    L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', 
        {
        maxZoom: 30,
        minZoom: 5,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: 'Google'
        }
    ).addTo(map);

    LeafIcon = L.Icon.extend({
        options: {
            shadowUrl: 'leaf-shadow.png',
            iconSize: [38, 95],
            shadowSize: [50, 64],
            iconAnchor: [22, 94],
            shadowAnchor: [4, 62],
            popupAnchor: [-3, -76]
        }
    });

        // Draw polygon and line features
    var drawnItems = new L.FeatureGroup();

    map.addLayer(drawnItems);
    var drawControl = new L.Control.Draw({
        position: 'topright',
        draw: {
            polygon: {
                shapeOptions: {
                    color: "rgb(0% 98.576% 15.974%)" //polygons being drawn will be purple color
                },
                allowIntersection: false,
                drawError: {
                    color: 'orange',
                    timeout: 1000
                },
                showArea: true, //the area of the polygon will be displayed as it is drawn.
                metric: true,
                repeatMode: true
            },
            polyline: {
                shapeOptions: {
                    color: 'red'
                },
            },
            circlemarker: false, //circlemarker type has been disabled.
            rect: {
                shapeOptions: {
                    color: 'green'
                },
            },
            circle: false,
        },
        edit: {
            featureGroup: drawnItems
        }
    });
    map.addControl(drawControl);
    map.on('draw:created', function (e) {
        var type = e.layerType,
            layer = e.layer;
        drawnItems.addLayer(layer);
        $('#polygon').val(JSON.stringify(layer.toGeoJSON()));

    });

    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.qtWidget = channel.objects.qtWidget;
        map.on('dragend', function () {
            center = map.getCenter();
            qtWidget.mapMoved(center.lat, center.lng);
        });

        map.on('click', function (ev) {
            qtWidget.mapClicked(ev.latlng.lat, ev.latlng.lng);
        });

        map.on('dblclick', function (ev) {
            qtWidget.mapDoubleClicked(ev.latlng.lat, ev.latlng.lng);
        });

        map.on('contextmenu', function (ev) {
            qtWidget.mapRightClicked(ev.latlng.lat, ev.latlng.lng);
        });

        // map.on('draw:created', function (e) {
        //     var type = e.layerType,
        //         layer = e.layer;
        //         // console.log(layer.toGeoJSON());
        //     qtWidget.polygonDrawn(JSON.stringify(layer.toGeoJSON()));
        // });
    });

}

function setCenterJs(lat, lng) {
    //console.log(lat);
    map.panTo(new L.LatLng(lat, lng));
}

function getCenterJs() {
    return map.getCenter();
}

function setZoomJs(zoom) {
    map.setZoom(zoom);
}

function addMarkerJs(key, latitude, longitude) {

    if (key in markers) {
        deleteMarker(key);
    }

    // if ("icon" in parameters) {

    //     parameters["icon"] = new L.Icon({
    //         iconUrl: parameters["icon"],
    //         iconAnchor: new L.Point(16, 16)
    //     });
    // }

    var marker = L.marker([latitude, longitude]).addTo(map);

    marker.on('dragend', function (event) {
        var marker = event.target;
        qtWidget.markerMoved(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on('click', function (event) {
        var marker = event.target;
        marker.bindPopup(parameters["title"]);
        qtWidget.markerClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on('dbclick', function (event) {
        var marker = event.target;
        qtWidget.markerDoubleClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on('contextmenu', function (event) {
        var marker = event.target;
        qtWidget.markerRightClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    markers[key] = marker;
    return key;
}

function deleteMarkerJs(key) {
    map.removeLayer(markers[key]);
    delete markers[key];
}

function moveMarkerJs(key, latitude, longitude) {
    marker = markers[key];
    var newLatLng = new L.LatLng(latitude, longitude);
    marker.setLatLng(newLatLng);
}

function posMarkerJs(key) {
    marker = markers[key];
    return [marker.getLatLng().lat, marker.getLatLng().lng];
}
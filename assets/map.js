// Where you want to render the map.

var map;

var markers = [];

var markerCounter = 0;  // Initialize a counter for markers

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
        export: true,
        position: 'topright',
        draw: {
            polygon: {
                shapeOptions: {
                    color: "rgb(0% 98.576% 15.974%)" //polygons being drawn will be purple color
                },
                drawError: {
                    color: 'orange',
                    timeout: 1000
                },
                showArea: true, //the area of the polygon will be displayed as it is drawn.
                metric: true,
                repeatMode: true,
                allowIntersection: false,
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
            featureGroup: drawnItems,
        }
    });
    
    map.addControl(drawControl);
    map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,
            layer = e.layer;
        // Add the drawn layer to the map
        drawnItems.addLayer(layer);
        // Get the GeoJSON of the layer (polygon or marker)
        var geojsonData = JSON.stringify(layer.toGeoJSON());
        // Set the GeoJSON data to the hidden input field
        $('#polygon').val(geojsonData);

    });

    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.qtWidget = channel.objects.qtWidget;
        map.on('dragend', function () {
            center = map.getCenter();
            qtWidget.mapMoved(center.lat, center.lng);
        });

        map.on('click', function (ev) {
            qtWidget.mapLeftClicked(ev.latlng.lat, ev.latlng.lng);
        });

        map.on('dblclick', function (ev) {
            qtWidget.mapDoubleClicked(ev.latlng.lat, ev.latlng.lng);
        });

        map.on('contextmenu', function (ev) {
            qtWidget.mapRightClicked(ev.latlng.lat, ev.latlng.lng);
        });
        map.on(L.Draw.Event.CREATED, function (e) {
            var type = e.layerType,
                layer = e.layer;
            var geojsonData = JSON.stringify(layer.toGeoJSON());
            qtWidget.geoJsonHandle(geojsonData);
        });
        
    });

}

function setCenterJs(lat, lng) {
    map.panTo(new L.LatLng(lat, lng));
}

function getCenterJs() {
    return map.getCenter();
}

function setZoomJs(zoom) {
    map.setZoom(zoom);
}

function drawGeoJsonJs(geoJson) {
    var geoJsonLayer = L.geoJson(JSON.parse(geoJson)).addTo(map);
    map.fitBounds(geoJsonLayer.getBounds());
}

function addMarkerJs(key, latitude, longitude) {

    if (key in markers) {
        deleteMarkerJs(key);
    }

    // Increment the marker counter
    markerCounter++;

    // Create a custom DivIcon with the marker number
    var customIcon = L.divIcon({
        className: 'custom-marker',  // Custom class for styling
        html: `<div class="marker-label">${markerCounter}</div>`,  // HTML with marker number
        iconSize: [30, 42],  // Adjust size to fit the number display
        iconAnchor: [15, 42],  // Anchor the icon to the correct position
    });

    // Create a marker using the custom DivIcon
    var marker = L.marker([latitude, longitude], { icon: customIcon, draggable: true }).addTo(map);


    // Add event listeners (drag, click, etc.) for the marker
    marker.on('dragend', function (event) {
        var marker = event.target;
        qtWidget.markerMoved(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on('click', function (event) {
        var marker = event.target;
        marker.bindPopup(parameters["title"]);
        qtWidget.markerLeftClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on('dblclick', function (event) {
        var marker = event.target;
        qtWidget.markerDoubleClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on('contextmenu', function (event) {
        var marker = event.target;
        qtWidget.markerRightClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    // Store the marker in the markers array
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
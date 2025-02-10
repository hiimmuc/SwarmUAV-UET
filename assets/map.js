// Where you want to render the map.
// cspell: ignore circlemarker latlng mapid dbclick

var map;

var markers = [];

var lines = [];

var polygons = [];

var lineCounter = 0;

var polygonCounter = 0;

var markerCounter = 0;  // Initialize a counter for markers

var LeafIcon;


function initialize() {
    var element = document.getElementById('mapid');

    map = L.map(element).setView([21.064862, 105.792958], 16);

    // Add a tile layer
    // streets:   'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    // hybrid:    'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}'
    // Satellite: 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    // Terrain:   'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}'
    // OSM:       'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', 
        {
        maxZoom: 50,
        minZoom: 5,
        subdomains:['mt0','mt1','mt2','mt3'],
        attribution: 'Google'
        }
    ).addTo(map);
    // If using OpenStreetMap
    // L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    // }).addTo(map);

    // var LeafIcon = L.Icon.extend({
    //     options: {
    //         shadowUrl: 'leaf-shadow.png',
    //         iconSize: [38, 95],
    //         shadowSize: [50, 64],
    //         iconAnchor: [22, 94],
    //         shadowAnchor: [4, 62],
    //         popupAnchor: [-3, -76]
    //     }
    // });

    var UAVIcon = L.Icon.extend({
        options: {
            iconAnchor: new L.Point(12, 12),
            iconSize: new L.Point(37, 37),
            iconUrl: './icons/drone.png',
        }
    });

    // Draw polygon and line features
    var drawnItems = new L.FeatureGroup();

    map.addLayer(drawnItems);
    var drawControl = new L.Control.Draw({
        export: false,
        position: 'topright',
        show_geometry_on_click: true,
        draw: {
            polygon: {
                shapeOptions: {
                    color: "rgb(0% 98.576% 15.974%)" //polygons being drawn will be purple color
                },
                drawError: {
                    color: 'orange',
                    message: '<strong>Oh snap!<strong> you can\'t draw that!' //error message will be displayed if the polygon is drawn incorrectly.
                },
                showArea: ['km', 'm'], //the area of the polygon will be displayed as it is drawn.
                metric: true,
                repeatMode: false,
                allowIntersection: false,            
            },

            polyline: {
                shapeOptions: {
                    color: 'red'
                },
            },
            
            rect: {
                shapeOptions: {
                    color: 'green'
                },
                showArea: true,
            },

            marker: {
                icon: new UAVIcon
            },

            circle: false,
            circlemarker: false, //  type has been disabled.
        },
        edit: {
            featureGroup: drawnItems,
            remove: false
        }
    });
    
    map.addControl(drawControl);

    map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,
            layer = e.layer;
        // Add the drawn layer to the map
        layer.on('click', function() {
            alert(coords);
            console.log(coords);
        });
        drawnItems.addLayer(layer);
        // Get the GeoJSON of the layer (polygon or marker)
        var geojsonData = JSON.stringify(layer.toGeoJSON());
        // Set the GeoJSON data to the hidden input field
        $('#polygon').val(geojsonData);

    });

    map.on('draw:edited', function (e) {
        var layers = e.layers;
        layers.eachLayer(function (layer) {
            // Get the GeoJSON of the layer (polygon or marker)
            var geojsonData = JSON.stringify(layer.toGeoJSON());
            // Set the GeoJSON data to the hidden input field
            $('#polygon').val(geojsonData);
        });
    });

    // connect to the Qt WebChannel
    new QWebChannel(qt.webChannelTransport, function (channel) {
        window.qtWidget = channel.objects.qtWidget;
        map.on('dragend', function () {
            center = map.getCenter();
            qtWidget.mapMoved(center.lat, center.lng);
            // TODO(today): zoom level
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
        
        map.on('draw:edited', function (e) {
            var layers = e.layers;
            layers.eachLayer(function (layer) {
                // Get the GeoJSON of the layer (polygon or marker)
                var geojsonData = JSON.stringify(layer.toGeoJSON());
                // Set the GeoJSON data to the hidden input field
                qtWidget.geoJsonHandle(geojsonData);
            });
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
// ================== Marker ==================
function addMarkerJs(key, latitude, longitude, parameters) {
    if (key in markers) {
        deleteMarkerJs(key);
    }

    if ("icon" in parameters) {
        parameters["icon"] = new L.Icon({
        iconUrl: parameters["icon"],
        // iconAnchor: new L.Point(parameters["iconAnchor"].x, parameters["iconAnchor"].y),
        iconSize: new L.Point(parameters["iconSize"].width, parameters["iconSize"].height),
        });
    }

    var marker = L.marker([latitude, longitude], parameters).addTo(map);
    // var popup = L.popup({autoClose: false}).setLatLng([latitude, longitude]).setContent(key).addTo(map);
    var tooltip = L.tooltip({ direction: 'top'}).setContent(key).setLatLng([latitude, longitude]).addTo(map);

    marker.on("dragend", function (event) {
        var marker = event.target;
        qtWidget.markerMoved(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on("click", function (event) {
        var marker = event.target;
        //marker.bindPopup(parameters["title"]);
        qtWidget.markerClicked(key, marker.getLatLng().lat, marker.getLatLng().lng);
    });

    marker.on("dbclick", function (event) {
        var marker = event.target;
        qtWidget.markerDoubleClicked(
        key,
        marker.getLatLng().lat,
        marker.getLatLng().lng
        );
    });

    marker.on("contextmenu", function (event) {
        var marker = event.target;
        qtWidget.markerRightClicked(
        key,
        marker.getLatLng().lat,
        marker.getLatLng().lng
        );
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

// ================== Line ==================
function drawPolyLineJs(key, coords, options) {
    var polyline = L.polyline(coords, options)
    polyline.addTo(map);
    lines[key] = polyline;
    return key;
}

function deletePolyLineJs() {
    map.removeLayer(lines[key]);
    delete lines[key];
}

// ================== Polygon ==================
function drawPolygonJs(key,coords, options) {
    var polygon = L.polygon(coords, options);
    polygon.addTo(map);
    polygons[key] = polygon;
    return key;
}

function deletePolygonJs(key) {
    map.removeLayer(polygons[key]);
    delete polygons[key];
}

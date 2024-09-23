    // streets:   'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}'
    // hybrid:    'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}'
    // Satellite: 'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    // Terrain:   'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}'
    // OSM:       'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

export const urlTemplate =  'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}';
export const wmtsUrlTemplate =
  'https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0?service=WMTS&request=GetTile&version=1.0.0&tilematrixset=EPSG:3857&layer={layer}&tilematrix={z}&tilerow={y}&tilecol={x}&format=image%2Fpng';
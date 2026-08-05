const map = L.map("map").setView([26.2, 92.9], 8);

const osm = L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }
);

osm.addTo(map);

const floodLayer = L.tileLayer.wms(
    "http://localhost:8084/geoserver/wms",
    {
        layers: "FloodMapping:FloodExtent",
        format: "image/png",
        transparent: true,
        version: "1.1.1"
    }
);

floodLayer.addTo(map);

L.control.layers(
    {
        "OpenStreetMap": osm
    },
    {
        "Flood Extent": floodLayer
    }
).addTo(map);

L.control.scale().addTo(map);
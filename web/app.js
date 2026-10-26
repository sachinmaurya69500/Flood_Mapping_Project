const INDIA_BOUNDS = [[6.5, 68.1], [35.7, 97.4]];
const map = L.map("map").setView([22.5, 79], 5);

const osm = L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }
);

const satellite = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    {maxZoom: 19, attribution: "Tiles &copy; Esri"}
);
const terrain = L.tileLayer(
    "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    {maxZoom: 17, attribution: "Map data &copy; OpenStreetMap contributors, SRTM | Map style &copy; OpenTopoMap"}
);
const dark = L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    {maxZoom: 19, attribution: "&copy; OpenStreetMap contributors &copy; CARTO"}
);

osm.addTo(map);

L.control.scale().addTo(map);

const layerControl = L.control.layers({
    "Street map": osm,
    "Satellite": satellite,
    "Terrain": terrain,
    "Dark map": dark
}).addTo(map);
const result = document.getElementById("result");
const layers = {};
const API_BASE = location.protocol === "file:" ? "http://localhost:8086" : "";
let selectedBounds = INDIA_BOUNDS;
const drawnItems = new L.FeatureGroup().addTo(map);
map.addControl(new L.Control.Draw({
    draw: {polygon: false, polyline: false, circle: false, circlemarker: false, marker: false},
    edit: {featureGroup: drawnItems}
}));

function setSelection(bounds) {
    selectedBounds = bounds;
    document.getElementById("selection").textContent =
        `Selected: ${bounds[0][1].toFixed(3)}, ${bounds[0][0].toFixed(3)} to ${bounds[1][1].toFixed(3)}, ${bounds[1][0].toFixed(3)}`;
}

map.on(L.Draw.Event.CREATED, event => {
    drawnItems.clearLayers();
    drawnItems.addLayer(event.layer);
    const b = event.layer.getBounds();
    setSelection([[b.getSouth(), b.getWest()], [b.getNorth(), b.getEast()]]);
});

map.on("click", event => {
    const lat = event.latlng.lat, lng = event.latlng.lng;
    const delta = 0.05;
    drawnItems.clearLayers();
    setSelection([[lat - delta, lng - delta], [lat + delta, lng + delta]]);
    L.rectangle([[lat - delta, lng - delta], [lat + delta, lng + delta]], {color: "#3388ff", weight: 1}).addTo(drawnItems);
});

function addEarthEngineLayer(name, layer, options) {
    if (layers[name]) map.removeLayer(layers[name]);
    layers[name] = L.tileLayer(layer.url, options).addTo(map);
    layerControl.addOverlay(layers[name], name);
}

document.getElementById("run").addEventListener("click", async () => {
    const button = document.getElementById("run");
    button.disabled = true;
    button.textContent = "Loading imagery…";
    result.className = "loading";
    result.textContent = "Connecting to Google Earth Engine…";
    const value = id => document.getElementById(id).value;
    const payload = {
        before_start: value("beforeStart"), before_end: value("beforeEnd"),
        after_start: value("afterStart"), after_end: value("afterEnd"),
        polarization: value("polarization"), threshold: Number(value("threshold")),
        bbox: [selectedBounds[0][1], selectedBounds[0][0], selectedBounds[1][1], selectedBounds[1][0]]
    };
    try {
        const response = await fetch(`${API_BASE}/api/analyze`, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(payload)});
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Analysis failed");
        addEarthEngineLayer("Before flood", data.layers.before, {opacity: 0.75});
        addEarthEngineLayer("After flood", data.layers.after, {opacity: 0.75});
        addEarthEngineLayer("Change difference", data.layers.difference, {opacity: 0.7});
        addEarthEngineLayer("Flood extent", data.layers.flood, {opacity: 0.8});
        map.fitBounds([[payload.bbox[1], payload.bbox[0]], [payload.bbox[3], payload.bbox[2]]]);
        result.className = "success";
        const exportInfo = data.download_url
            ? `<a href="${data.download_url}" target="_blank">Download GeoTIFF (${data.download_scale_m} m)</a>`
            : `${data.export_message || "GeoTIFF export started in Google Drive."}<br>Task: ${data.export_task || "submitted"}`;
        result.innerHTML = `<b>${data.flooded_area_km2.toFixed(2)} km² flooded</b><br>${data.image_count} images found · ${data.scale_m} m analysis<br>${exportInfo}`;
    } catch (error) {
        result.className = "error";
        result.textContent = `Could not load data\n\n${error.message}\n\nCheck EE_PROJECT_ID and Earth Engine authentication.`;
    } finally {
        button.disabled = false;
        button.textContent = "Load Earth Engine data";
    }
});

document.getElementById("india").addEventListener("click", () => {
    drawnItems.clearLayers();
    selectedBounds = INDIA_BOUNDS;
    L.rectangle(INDIA_BOUNDS, {color: "#147d92", weight: 2}).addTo(drawnItems);
    setSelection(INDIA_BOUNDS);
    map.fitBounds(INDIA_BOUNDS);
});

document.getElementById("india").click();


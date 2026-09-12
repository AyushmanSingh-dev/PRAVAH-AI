/**
 * PRAVAH AI - Multi-Region Himalayan Client Application Logic
 * Supports real-time disaster simulation across Uttarakhand Basins:
 * - Alaknanda / Rishi Ganga Basin (Chamoli)
 * - Mandakini River Basin (Kedarnath)
 * - Bhagirathi River Basin (Uttarkashi)
 * Includes 3-Tier Lead Time Horizons (180 min, 90 min, 30 min) and
 * Historical Disaster Benchmarks.
 */

let map = null;
let riverPolyline = null;
let settlementMarkers = {};
let hydrographChart = null;
let currentPipelineData = null;
let historicalSuiteData = null;
let regionsCatalog = null;

let currentRegionId = "alaknanda";
let currentHorizonMin = 30;

// Default Uttarakhand Basins Catalog
const REGIONS_DATA = {
  alaknanda: {
    id: "alaknanda",
    name: "Alaknanda & Rishi Ganga Basin",
    short_name: "Alaknanda (Chamoli)",
    district: "Chamoli, Uttarakhand",
    elevation_range: "1,050m - 5,200m",
    dominant_geology: "Crystalline Gneiss & Colluvial Debris Mantle",
    center_lat: 30.49,
    center_lon: 79.55,
    default_zoom: 11,
    river_path: [
      [30.4710, 79.7350], [30.4886, 79.6975], [30.5012, 79.6241],
      [30.5310, 79.5880], [30.5567, 79.5684], [30.5200, 79.5100],
      [30.4500, 79.4200], [30.4128, 79.3315]
    ],
    geotechnical: {
      rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 85.0,
      initial_soil_moisture: 0.22, k_sat_mm_hr: 14.5, psi_suction_mm: 110.0, soil_depth_z: 2.2,
      slope_beta_deg: 35.0, c_prime: 8500.0, phi_prime_deg: 32.0,
      manning_n: 0.048, bed_slope_s0: 0.024, bottom_width_b: 28.0
    }
  },
  mandakini: {
    id: "mandakini",
    name: "Mandakini River Basin (Kedarnath Corridor)",
    short_name: "Mandakini (Kedarnath)",
    district: "Rudraprayag, Uttarakhand",
    elevation_range: "610m - 4,100m",
    dominant_geology: "Glacial Moraines, Paragneiss & High-Gradient Scree",
    center_lat: 30.64,
    center_lon: 79.05,
    default_zoom: 11,
    river_path: [
      [30.7450, 79.0700], [30.7350, 79.0670], [30.6850, 79.0450],
      [30.6520, 79.0300], [30.6310, 78.9980], [30.5500, 79.0500],
      [30.4500, 79.0700], [30.2850, 78.9800]
    ],
    geotechnical: {
      rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 68.0,
      initial_soil_moisture: 0.25, k_sat_mm_hr: 16.0, psi_suction_mm: 95.0, soil_depth_z: 1.8,
      slope_beta_deg: 38.0, c_prime: 6500.0, phi_prime_deg: 30.0,
      manning_n: 0.052, bed_slope_s0: 0.029, bottom_width_b: 24.0
    }
  },
  bhagirathi: {
    id: "bhagirathi",
    name: "Bhagirathi River Basin (Uttarkashi Reach)",
    short_name: "Bhagirathi (Uttarkashi)",
    district: "Uttarkashi, Uttarakhand",
    elevation_range: "850m - 3,800m",
    dominant_geology: "Weathered Biotite Schist, Quartzite & Valley Colluvium",
    center_lat: 30.82,
    center_lon: 78.60,
    default_zoom: 10,
    river_path: [
      [30.9950, 78.9400], [31.0350, 78.7400], [30.9100, 78.6700],
      [30.8150, 78.6200], [30.7250, 78.4400], [30.6500, 78.3900],
      [30.5600, 78.3300]
    ],
    geotechnical: {
      rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 110.0,
      initial_soil_moisture: 0.22, k_sat_mm_hr: 17.5, psi_suction_mm: 100.0, soil_depth_z: 2.4,
      slope_beta_deg: 33.0, c_prime: 7800.0, phi_prime_deg: 33.0,
      manning_n: 0.046, bed_slope_s0: 0.020, bottom_width_b: 32.0
    }
  },
  beas: {
    id: "beas",
    name: "Beas River Basin (Kullu - Manali Valley)",
    short_name: "Beas (Kullu-Manali)",
    district: "Kullu, Himachal Pradesh",
    elevation_range: "1,100m - 4,200m",
    dominant_geology: "Central Crystalline Gneiss, Quartzite & River Terraces",
    center_lat: 31.95,
    center_lon: 77.15,
    default_zoom: 11,
    river_path: [
      [32.3200, 77.1800], [32.2800, 77.1650], [32.2432, 77.1892],
      [32.1800, 77.1700], [31.9600, 77.1100], [31.8600, 77.1400],
      [31.7500, 77.1200], [31.6700, 77.0600]
    ],
    geotechnical: {
      rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 95.0,
      initial_soil_moisture: 0.23, k_sat_mm_hr: 15.2, psi_suction_mm: 105.0,
      soil_depth_z: 2.0, slope_beta_deg: 34.0, c_prime: 7200.0, phi_prime_deg: 32.0,
      manning_n: 0.045, bed_slope_s0: 0.022, bottom_width_b: 30.0
    }
  },
  teesta: {
    id: "teesta",
    name: "Teesta River Basin (North Sikkim Corridor)",
    short_name: "Teesta (North Sikkim)",
    district: "Mangan, Sikkim",
    elevation_range: "650m - 5,200m",
    dominant_geology: "Lingtse Gneiss, Daling Phyllites & Moraine Scree",
    center_lat: 27.60,
    center_lon: 88.58,
    default_zoom: 10,
    river_path: [
      [27.9800, 88.6200], [27.6000, 88.6400], [27.5000, 88.5300],
      [27.4200, 88.5200], [27.2300, 88.5000], [27.0800, 88.4700]
    ],
    geotechnical: {
      rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 120.0,
      initial_soil_moisture: 0.24, k_sat_mm_hr: 16.5, psi_suction_mm: 98.0,
      soil_depth_z: 1.9, slope_beta_deg: 36.0, c_prime: 6800.0, phi_prime_deg: 31.0,
      manning_n: 0.050, bed_slope_s0: 0.027, bottom_width_b: 26.0
    }
  },
  chenab: {
    id: "chenab",
    name: "Chenab River Basin (Kishtwar & Machail Gorges)",
    short_name: "Chenab (Kishtwar)",
    district: "Kishtwar, Jammu & Kashmir",
    elevation_range: "950m - 4,600m",
    dominant_geology: "Kishtwar Quartzites, Mica-Schist & Glacio-Fluvial Scree",
    center_lat: 33.31,
    center_lon: 75.76,
    default_zoom: 10,
    river_path: [
      [33.5600, 76.1200], [33.4500, 75.9800], [33.3600, 75.8400],
      [33.3150, 75.7650], [33.2400, 75.6800], [33.1400, 75.5400]
    ],
    geotechnical: {
      rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 105.0,
      initial_soil_moisture: 0.22, k_sat_mm_hr: 14.8, psi_suction_mm: 112.0,
      soil_depth_z: 2.1, slope_beta_deg: 37.0, c_prime: 8100.0, phi_prime_deg: 33.0,
      manning_n: 0.047, bed_slope_s0: 0.025, bottom_width_b: 32.0
    }
  }
};

document.addEventListener("DOMContentLoaded", () => {
  initClock();
  initMap();
  initHydrographChart();
  // Fetch regions from server or use catalog
  fetchRegions();

  const select = document.getElementById("select-himalayan-basin");
  const initRegion = (select && select.value) ? select.value : "alaknanda";
  switchRegion(initRegion);

  // Pre-fetch historical validation benchmark data
  fetchHistoricalValidationData();
});

/* -------------------------------------------------------------------------
   1. CLOCK LOGIC
   ------------------------------------------------------------------------- */
function initClock() {
  const clockEl = document.getElementById("live-clock");
  setInterval(() => {
    const now = new Date();
    const utcStr = now.toUTCString().split(" ")[4];
    const istOptions = { timeZone: "Asia/Kolkata", hour12: false, hour: "2-digit", minute: "2-digit", second: "2-digit" };
    const istStr = now.toLocaleTimeString("en-GB", istOptions);
    clockEl.innerText = `UTC ${utcStr} | IST ${istStr}`;
  }, 1000);
}

/* -------------------------------------------------------------------------
   2. LEAFLET GEOSPATIAL MAP & REGIONAL SWITCHER
   ------------------------------------------------------------------------- */
function initMap() {
  map = L.map("catchment-map", {
    zoomControl: false,
    attributionControl: false
  }).setView([30.49, 79.55], 11);

  // Esri World Topo Map for high-resolution relief contours & mountain topography
  L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}", {
    maxZoom: 18,
    attribution: "Tiles &copy; Esri"
  }).addTo(map);

  L.control.zoom({ position: "bottomright" }).addTo(map);

  riverPolyline = L.polyline(REGIONS_DATA.alaknanda.river_path, {
    color: "#0284c7",
    weight: 5,
    opacity: 0.85,
    smoothFactor: 1
  }).addTo(map);
}

async function fetchRegions() {
  try {
    const res = await fetch("/api/regions");
    if (res.ok) {
      regionsCatalog = await res.json();
    }
  } catch (err) {
    regionsCatalog = REGIONS_DATA;
  }
}

function onRegionChange() {
  const select = document.getElementById("select-himalayan-basin");
  if (select) switchRegion(select.value);
}

function switchRegion(regionId) {
  if (!REGIONS_DATA[regionId] && (!regionsCatalog || !regionsCatalog[regionId])) {
    regionId = "alaknanda";
  }
  currentRegionId = regionId;
  const region = (regionsCatalog && regionsCatalog[regionId]) || REGIONS_DATA[regionId] || REGIONS_DATA.alaknanda;

  // 1. Sync Dropdown Select
  const select = document.getElementById("select-himalayan-basin");
  if (select && select.value !== regionId) {
    select.value = regionId;
  }

  // 4. Update Ribbon Metadata
  document.getElementById("ribbon-basin-name").innerText = region.name;
  document.getElementById("ribbon-district").innerText = region.district;
  document.getElementById("ribbon-elevation").innerText = region.elevation_range;
  document.getElementById("ribbon-geology").innerText = region.dominant_geology;

  // 5. Render Dynamic Basin Disaster Presets
  renderBasinScenarios(regionId);

  // 6. Fly map to new coordinates
  if (map) {
    map.flyTo([region.center_lat, region.center_lon], region.default_zoom, {
      duration: 1.0,
      easeLinearity: 0.25
    });
  }

  // 7. Clear old settlement markers and update polyline
  Object.values(settlementMarkers).forEach(m => map.removeLayer(m));
  settlementMarkers = {};

  if (riverPolyline && region.river_path) {
    riverPolyline.setLatLngs(region.river_path);
  }

  // 8. Load that region's calibrated geotechnical values into sliders
  const cfg = region.geotechnical || REGIONS_DATA.alaknanda.geotechnical;
  setAllSliders(cfg);

  // 9. Run simulation for the new region
  runMultiFactorSimulation(cfg);
}

function updateMapMarkers(settlements, overallHazard) {
  let riverColor = "#10b981";
  if (overallHazard === "RED") riverColor = "#ef4444";
  else if (overallHazard === "YELLOW") riverColor = "#f59e0b";

  riverPolyline.setStyle({ color: riverColor });

  settlements.forEach(s => {
    const latlng = [s.lat, s.lon];
    const markerColor = s.status_color;

    const customIcon = L.divIcon({
      className: "custom-pin",
      html: `
        <div style="
          width: 14px;
          height: 14px;
          background-color: ${markerColor};
          border: 2px solid #ffffff;
          border-radius: 50%;
          box-shadow: 0 0 10px ${markerColor};
        "></div>
      `,
      iconSize: [14, 14],
      iconAnchor: [7, 7]
    });

    if (settlementMarkers[s.id]) {
      settlementMarkers[s.id].setIcon(customIcon);
      settlementMarkers[s.id].setPopupContent(`
        <div style="color: #0f172a; font-family: sans-serif; font-size: 11px;">
          <strong>${s.name}</strong><br>
          Stage: <b>${s.predicted_stage_m}m</b> (Danger: ${s.danger_depth_m}m)<br>
          Evacuation Lead Time: <b>${s.evacuation_lead_time_min} mins</b><br>
          Status: <span style="color: ${markerColor}; font-weight: bold;">${s.status}</span>
        </div>
      `);
    } else {
      const marker = L.marker(latlng, { icon: customIcon }).addTo(map);
      marker.bindPopup(`
        <div style="color: #0f172a; font-family: sans-serif; font-size: 11px;">
          <strong>${s.name}</strong><br>
          Stage: <b>${s.predicted_stage_m}m</b> (Danger: ${s.danger_depth_m}m)<br>
          Evacuation Lead Time: <b>${s.evacuation_lead_time_min} mins</b><br>
          Status: <span style="color: ${markerColor}; font-weight: bold;">${s.status}</span>
        </div>
      `);
      settlementMarkers[s.id] = marker;
    }
  });

  const badge = document.getElementById("map-status-badge");
  if (overallHazard === "RED") {
    badge.innerHTML = `Overall Status: <strong style="color: var(--color-danger);">🔴 FLASH FLOOD EVACUATION ACTIVE</strong>`;
  } else if (overallHazard === "YELLOW") {
    badge.innerHTML = `Overall Status: <strong style="color: var(--color-warning);">🟡 CATCHMENT WATCH WARNING</strong>`;
  } else {
    badge.innerHTML = `Overall Status: <strong style="color: var(--color-safe);">🟢 NORMAL MONITORING (SAFE)</strong>`;
  }
}

/* -------------------------------------------------------------------------
   3. CHART.JS HYDROGRAPH
   ------------------------------------------------------------------------- */
function initHydrographChart() {
  const ctx = document.getElementById("hydrographChart").getContext("2d");
  
  hydrographChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00"],
      datasets: [
        {
          label: "Predicted River Discharge Q(t) [m³/s]",
          data: [35, 42, 60, 50, 40, 38, 35],
          borderColor: "#38bdf8",
          backgroundColor: "rgba(56, 189, 248, 0.12)",
          fill: true,
          tension: 0.4,
          borderWidth: 2,
          pointRadius: 3,
          pointBackgroundColor: "#38bdf8"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          labels: { color: "#94a3b8", font: { size: 10 } }
        },
        tooltip: {
          mode: "index",
          intersect: false
        }
      },
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#64748b", font: { size: 9 } }
        },
        y: {
          grid: { color: "rgba(255, 255, 255, 0.05)" },
          ticks: { color: "#64748b", font: { size: 9 } },
          suggestedMin: 0
        }
      }
    }
  });
}

function updateHydrograph(peakQ, durationHr) {
  if (!hydrographChart) return;

  const baseQ = 35.0;
  const peakTimeIdx = Math.min(Math.round(durationHr), 4);
  const hydroData = [];

  for (let i = 0; i < 7; i++) {
    if (i < peakTimeIdx) {
      const frac = i / Math.max(peakTimeIdx, 1);
      hydroData.push(Math.round(baseQ + (peakQ - baseQ) * (frac ** 1.8)));
    } else if (i === peakTimeIdx) {
      hydroData.push(Math.round(peakQ));
    } else {
      const frac = (i - peakTimeIdx) / (7 - peakTimeIdx);
      hydroData.push(Math.round(baseQ + (peakQ - baseQ) * Math.exp(-2.2 * frac)));
    }
  }

  hydrographChart.data.datasets[0].data = hydroData;
  if (peakQ >= 500) {
    hydrographChart.data.datasets[0].borderColor = "#ef4444";
    hydrographChart.data.datasets[0].backgroundColor = "rgba(239, 68, 68, 0.2)";
    hydrographChart.data.datasets[0].pointBackgroundColor = "#ef4444";
  } else if (peakQ >= 200) {
    hydrographChart.data.datasets[0].borderColor = "#f59e0b";
    hydrographChart.data.datasets[0].backgroundColor = "rgba(245, 158, 11, 0.15)";
    hydrographChart.data.datasets[0].pointBackgroundColor = "#f59e0b";
  } else {
    hydrographChart.data.datasets[0].borderColor = "#38bdf8";
    hydrographChart.data.datasets[0].backgroundColor = "rgba(56, 189, 248, 0.12)";
    hydrographChart.data.datasets[0].pointBackgroundColor = "#38bdf8";
  }

  hydrographChart.update();
  document.getElementById("peak-q-badge").innerText = `Peak Q: ${peakQ.toFixed(1)} m³/s`;
}

/* -------------------------------------------------------------------------
   4. MULTI-FACTOR TELEMETRY & SLIDER HANDLER
   ------------------------------------------------------------------------- */
let debounceTimeout = null;

function getFactorValuesFromSliders() {
  return {
    region_id: currentRegionId,
    rainfall_rate_mm_hr: parseFloat(document.getElementById("slider-rainfall").value),
    duration_hr: parseFloat(document.getElementById("slider-duration").value),
    catchment_area_km2: parseFloat(document.getElementById("slider-area").value),
    initial_soil_moisture: parseFloat(document.getElementById("slider-moisture").value),
    k_sat_mm_hr: parseFloat(document.getElementById("slider-ksat").value),
    psi_suction_mm: parseFloat(document.getElementById("slider-psi").value),
    soil_depth_z: parseFloat(document.getElementById("slider-soildepth").value),
    slope_beta_deg: parseFloat(document.getElementById("slider-slopebeta").value),
    c_prime: parseFloat(document.getElementById("slider-cprime").value) * 1000.0,
    phi_prime_deg: parseFloat(document.getElementById("slider-phiprime").value),
    manning_n: parseFloat(document.getElementById("slider-manningn").value),
    bed_slope_s0: parseFloat(document.getElementById("slider-bedslope").value),
    bottom_width_b: parseFloat(document.getElementById("slider-channelb").value)
  };
}

function updateSliderLabels(factors) {
  document.getElementById("val-rainfall").innerText = `${factors.rainfall_rate_mm_hr.toFixed(0)} mm/hr`;
  document.getElementById("val-duration").innerText = `${factors.duration_hr.toFixed(1)} hrs`;
  document.getElementById("val-area").innerText = `${factors.catchment_area_km2.toFixed(0)} km²`;

  const satPct = Math.round((factors.initial_soil_moisture / 0.44) * 100);
  document.getElementById("val-moisture").innerText = `${factors.initial_soil_moisture.toFixed(2)} (${satPct}% Sat)`;
  document.getElementById("val-ksat").innerText = `${factors.k_sat_mm_hr.toFixed(1)} mm/hr`;
  document.getElementById("val-psi").innerText = `${factors.psi_suction_mm.toFixed(0)} mm`;
  document.getElementById("val-soildepth").innerText = `${factors.soil_depth_z.toFixed(1)} m`;

  document.getElementById("val-slopebeta").innerText = `${factors.slope_beta_deg.toFixed(1)}°`;
  document.getElementById("val-cprime").innerText = `${(factors.c_prime / 1000.0).toFixed(1)} kPa`;
  document.getElementById("val-phiprime").innerText = `${factors.phi_prime_deg.toFixed(1)}°`;

  document.getElementById("val-manningn").innerText = `${factors.manning_n.toFixed(3)}`;
  document.getElementById("val-bedslope").innerText = `${factors.bed_slope_s0.toFixed(3)} (${(factors.bed_slope_s0 * 100).toFixed(1)}%)`;
  document.getElementById("val-channelb").innerText = `${factors.bottom_width_b.toFixed(1)} m`;
}

function onFactorChange() {
  const factors = getFactorValuesFromSliders();
  updateSliderLabels(factors);

  document.querySelectorAll(".scenario-btn").forEach(btn => btn.classList.remove("active"));

  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    runMultiFactorSimulation(factors);
  }, 100);
}

async function runMultiFactorSimulation(factors) {
  try {
    factors.region_id = currentRegionId;
    const res = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(factors)
    });
    const data = await res.json();
    currentPipelineData = data;
    renderPipelineData(data);
  } catch (err) {
    console.error("Multi-factor simulation failed:", err);
  }
}

/* -------------------------------------------------------------------------
   5. RENDER PIPELINE DATA & LEAD TIME HORIZONS
   ------------------------------------------------------------------------- */
function switchHorizon(horizonMin) {
  currentHorizonMin = horizonMin;
  document.querySelectorAll(".horizon-btn").forEach(b => b.classList.remove("active"));
  document.getElementById(`btn-horizon-${horizonMin}`).classList.add("active");

  if (currentPipelineData) {
    renderPipelineData(currentPipelineData);
  }
}

function renderPipelineData(data) {
  // 1. Compound Probability & Verdict Hero Bar
  const cp = data.compound_probability;
  const probVal = cp.compound_flash_flood_probability_pct;
  const probBar = document.getElementById("prob-bar-fill");
  const probText = document.getElementById("prob-percentage-text");
  const riskBadge = document.getElementById("risk-verdict-badge");

  probBar.style.width = `${Math.min(100, Math.max(5, probVal))}%`;
  probText.innerText = `${probVal.toFixed(1)}%`;

  if (probVal >= 75.0) {
    probBar.className = "prob-bar-fill danger";
    riskBadge.innerText = "🔴 EXTREME FLASH FLOOD DANGER";
    riskBadge.style.color = "#ef4444";
    riskBadge.style.borderColor = "#ef4444";
    riskBadge.style.background = "rgba(239, 68, 68, 0.2)";
  } else if (probVal >= 40.0) {
    probBar.className = "prob-bar-fill";
    probBar.style.background = "linear-gradient(90deg, #10b981, #f59e0b)";
    riskBadge.innerText = "🟡 MONSOON WATCH / ADVISORY";
    riskBadge.style.color = "#f59e0b";
    riskBadge.style.borderColor = "#f59e0b";
    riskBadge.style.background = "rgba(245, 158, 11, 0.2)";
  } else {
    probBar.className = "prob-bar-fill";
    probBar.style.background = "linear-gradient(90deg, #10b981, #0ea5e9)";
    riskBadge.innerText = "🟢 NORMAL REGIME (SAFE)";
    riskBadge.style.color = "#10b981";
    riskBadge.style.borderColor = "#10b981";
    riskBadge.style.background = "rgba(16, 185, 129, 0.2)";
  }

  // Sub-probabilities
  document.getElementById("sub-prob-runoff").innerText = `${cp.sub_probabilities.runoff_hazard_pct.toFixed(1)}%`;
  document.getElementById("sub-prob-slope").innerText = `${cp.sub_probabilities.slope_instability_pct.toFixed(1)}%`;
  document.getElementById("sub-prob-debris").innerText = `${cp.sub_probabilities.debris_hazard_pct.toFixed(1)}%`;
  document.getElementById("sub-prob-hydraulic").innerText = `${cp.sub_probabilities.inundation_hazard_pct.toFixed(1)}%`;

  // Decision Attribution
  const da = cp.decision_attribution;
  document.getElementById("attrib-primary").innerText = da.primary_driver;
  document.getElementById("attrib-secondary").innerText = da.secondary_trigger;
  document.getElementById("attrib-buffer").innerText = da.mitigating_buffer;

  // 2. Physical Engine Telemetry Pills
  const infil = data.factor_2_infiltration;
  const slope = data.factor_3_slope_stability;
  const debris = data.factor_4_debris_bulge;

  document.getElementById("val-runoff").innerText = `${infil.surface_runoff_rate_mm_hr} mm/hr`;
  document.getElementById("val-runoff").style.color = infil.surface_runoff_rate_mm_hr > 25 ? "#ef4444" : (infil.surface_runoff_rate_mm_hr > 5 ? "#f59e0b" : "#10b981");

  document.getElementById("val-fs").innerText = `${slope.factor_of_safety.toFixed(2)} (${slope.status})`;
  document.getElementById("val-fs").style.color = slope.status_color;
  document.getElementById("val-chen-young").innerText = `${slope.chen_young_threshold_mm_hr} mm/hr`;
  document.getElementById("val-bulge").innerText = `${debris.bulge_multiplier.toFixed(2)}x (${debris.debris_hazard.split(" ")[0]})`;

  // 3. Hydraulics & Dynamic Hydrograph
  const hyd = data.factor_5_hydraulics;
  updateHydrograph(hyd.peak_discharge_m3s, data.inputs.duration_hr);

  // 4. Deliverable 2: Actionable Lead Time Clock across Selected Horizon
  const leadCard = document.getElementById("lead-time-card");
  const leadClock = document.getElementById("clock-lead-time");
  const leadDesc = document.getElementById("lead-time-status-desc");
  const mtl = data.multi_tier_lead_time;

  if (currentHorizonMin === 180) {
    const t1Min = mtl ? mtl.tier1_atmospheric_nowcast.minutes : 180;
    leadClock.innerText = `${t1Min} MIN`;
    leadCard.className = "card lead-time-card";
    leadClock.className = "lead-time-clock";
    leadClock.style.color = probVal >= 75 ? "#f87171" : "#38bdf8";
    leadDesc.innerHTML = `🔭 <strong>T-180m PRE-STORM WATCH:</strong> Satellite cloud-top cooling &amp; Doppler radar advance notice dispatched to SDRF &amp; bridge guards (${t1Min} mins advance notice).`;
  } else if (currentHorizonMin === 90) {
    const t2Min = mtl ? mtl.tier2_catchment_saturation.minutes : 90;
    leadClock.innerText = `${t2Min} MIN`;
    leadCard.className = "card lead-time-card";
    leadClock.className = "lead-time-clock";
    leadClock.style.color = probVal >= 75 ? "#fbbf24" : "#38bdf8";
    leadDesc.innerHTML = `⚡ <strong>T-90m RUNOFF ONSET:</strong> Catchment soil column saturation deficit depleted (${t2Min} mins until unbuffered overland runoff peaks).`;
  } else {
    // 30 min (Wave Crest Evacuation)
    // Physically, higher rainfall = higher discharge = faster celerity = LESS time to evacuate!
    const localWaveLag = (data.deliverable_1_settlements && data.deliverable_1_settlements[0]) 
      ? data.deliverable_1_settlements[0].in_stream_travel_lag_min 
      : (data.primary_wave_travel_lag_min || 22);

    leadClock.innerText = `${localWaveLag} MIN`;

    if (data.overall_hazard_level === "RED") {
      leadCard.className = "card lead-time-card hazard-red";
      leadClock.className = "lead-time-clock hazard-red";
      leadDesc.innerHTML = `⚠️ <strong>CRITICAL FLOOD WAVE CREST</strong> travelling at high velocity, reaching primary bridge in <strong>${localWaveLag} mins</strong>. Immediate evacuation!`;
    } else if (data.overall_hazard_level === "YELLOW") {
      leadCard.className = "card lead-time-card";
      leadClock.className = "lead-time-clock";
      leadClock.style.color = "#f59e0b";
      leadDesc.innerHTML = `🟡 <strong>WATCH ADVISORY:</strong> River surge wave arrival in <strong>${localWaveLag} mins</strong>. Stage approaching warning mark.`;
    } else {
      leadCard.className = "card lead-time-card";
      leadClock.className = "lead-time-clock";
      leadClock.style.color = "#38bdf8";
      leadDesc.innerHTML = `🟢 Normal baseflow regime. In-stream kinematic wave lag: <strong>${localWaveLag} mins</strong>. Inundation buffer intact.`;
    }
  }

  // 5. Deliverable 1: Village Inundation Cards
  renderVillageCards(data.deliverable_1_settlements);

  // 6. Leaflet Map
  updateMapMarkers(data.deliverable_1_settlements, data.overall_hazard_level);

  // 7. Multi-Tiered Actionable Evacuation Lead Time (SIH26192 Core Deliverable)
  if (data.multi_tier_lead_time) {
    renderMultiTierLeadTime(data.multi_tier_lead_time, probVal);
  }

  // 8. Physics-Guided AI (PGNN) Hybrid Machine Learning Concordance
  if (data.ml_guidance) {
    renderPGNNConcordance(data.ml_guidance, probVal);
  }

  // 9. IoT In-Situ Sensor Telemetry Status
  if (data.iot_telemetry) {
    updateIoTStationsView(data.iot_telemetry);
  }
}

function renderMultiTierLeadTime(mtl, probVal) {
  const cdClock = document.getElementById("countdown-clock");
  const cdSub = document.getElementById("countdown-subtext");
  const cdPill = document.getElementById("leadtime-status-pill");

  if (cdClock) cdClock.innerText = `${mtl.composite_evacuation_countdown_min} MIN`;
  if (cdSub) {
    const hrs = Math.floor(mtl.composite_evacuation_countdown_min / 60);
    const mins = mtl.composite_evacuation_countdown_min % 60;
    cdSub.innerText = `(${hrs}h ${mins}m actionable evacuation lead time)`;
  }

  if (cdPill) {
    if (probVal >= 75.0) {
      cdPill.innerText = "🔴 IMMEDIATE EVACUATION PROTOCOL ACTIVE";
      cdPill.style.background = "rgba(239, 68, 68, 0.25)";
      cdPill.style.color = "#ef4444";
      cdPill.style.borderColor = "#ef4444";
    } else if (probVal >= 40.0) {
      cdPill.innerText = "🟡 ACTIONABLE EVACUATION WINDOW ACTIVE";
      cdPill.style.background = "rgba(245, 158, 11, 0.2)";
      cdPill.style.color = "#f59e0b";
      cdPill.style.borderColor = "#f59e0b";
    } else {
      cdPill.innerText = "🟢 MONITORING - EVACUATION HORIZON CLEAR";
      cdPill.style.background = "rgba(16, 185, 129, 0.2)";
      cdPill.style.color = "#10b981";
      cdPill.style.borderColor = "#10b981";
    }
  }

  const t1Val = document.getElementById("tier1-val");
  const t1Stat = document.getElementById("tier1-status");
  if (t1Val) t1Val.innerText = `${mtl.tier1_atmospheric_nowcast.minutes} min`;
  if (t1Stat) t1Stat.innerText = mtl.tier1_atmospheric_nowcast.status;

  const t2Val = document.getElementById("tier2-val");
  const t2Stat = document.getElementById("tier2-status");
  if (t2Val) t2Val.innerText = `${mtl.tier2_catchment_saturation.minutes} min`;
  if (t2Stat) t2Stat.innerText = mtl.tier2_catchment_saturation.status;

  const t3Val = document.getElementById("tier3-val");
  const t3Stat = document.getElementById("tier3-status");
  if (t3Val) t3Val.innerText = `${mtl.tier3_hydraulic_wave_lag.minutes} min`;
  if (t3Stat) t3Stat.innerText = mtl.tier3_hydraulic_wave_lag.status;
}

function renderPGNNConcordance(ml, probVal) {
  const physEl = document.getElementById("pgnn-physics-pct");
  const mlEl = document.getElementById("pgnn-ml-pct");
  const fusedEl = document.getElementById("pgnn-fused-pct");
  const badgeEl = document.getElementById("pgnn-concordance-badge");

  if (physEl) physEl.innerText = `${probVal.toFixed(1)}%`;
  if (mlEl) mlEl.innerText = `${ml.ml_probability_pct.toFixed(1)}%`;
  if (fusedEl) fusedEl.innerText = `${ml.hybrid_fused_risk_pct.toFixed(1)}%`;
  if (badgeEl) {
    badgeEl.innerText = ml.concordance;
    badgeEl.style.color = ml.concordance_color;
    badgeEl.style.background = `${ml.concordance_color}22`;
    badgeEl.style.borderColor = ml.concordance_color;
  }
}

function renderVillageCards(settlements) {
  const container = document.getElementById("villages-list");
  container.innerHTML = "";

  settlements.forEach(s => {
    let cardClass = "village-card";
    let pillClass = "village-status-pill pill-safe";

    if (s.status === "DANGER") {
      cardClass += " status-danger";
      pillClass = "village-status-pill pill-danger";
    } else if (s.status === "WARNING") {
      cardClass += " status-warning";
      pillClass = "village-status-pill pill-warning";
    }

    const card = document.createElement("div");
    card.className = cardClass;
    card.innerHTML = `
      <div class="village-header">
        <span class="village-name">${s.name} (${s.distance_km} km)</span>
        <span class="${pillClass}">${s.status}</span>
      </div>
      <div class="village-details">
        <span>Stage: <b>${s.predicted_stage_m}m</b> / ${s.danger_depth_m}m</span>
        <span>Peak Q: <b>${s.predicted_discharge_m3s} m³/s</b></span>
        <span>Lead Time: <b>${s.evacuation_lead_time_min}m</b></span>
      </div>
      <div class="village-action">
        &bull; Action: ${s.action_order} (Pop: ${s.population.toLocaleString()})
      </div>
    `;
    container.appendChild(card);
  });
}

/* -------------------------------------------------------------------------
   6. SCENARIOS PRESET SWITCHER & DYNAMIC BASIN PRESETS
   ------------------------------------------------------------------------- */
const BASIN_SCENARIOS = {
  alaknanda: [
    { id: "chamoli_2021", label: "Chamoli 2021 Cloudburst & Breach", desc: "105 mm/hr &bull; 2,150 m³/s Surge", icon: "🔴" },
    { id: "monsoon_saturated", label: "Active Monsoon Regolith Watch", desc: "52 mm/hr &bull; Saturated AMC III", icon: "🟡" },
    { id: "normal_baseline", label: "Clear Summer Baseline", desc: "4 mm/hr &bull; Stable Baseflow Regime", icon: "🟢", active: true }
  ],
  mandakini: [
    { id: "kedarnath_2013", label: "Kedarnath 2013 GLOF Breach", desc: "85 mm/hr &bull; Chorabari Moraine Dam Burst", icon: "🔴" },
    { id: "monsoon_mandakini", label: "Mandakini Monsoon Surcharge", desc: "48 mm/hr &bull; Gaurikund Riverbank Spill", icon: "🟡" },
    { id: "normal_baseline", label: "Clear Weather Baseflow", desc: "3.5 mm/hr &bull; Pilgrimage Route Clear", icon: "🟢", active: true }
  ],
  bhagirathi: [
    { id: "uttarkashi_2012", label: "Uttarkashi 2012 Asi Ganga Surge", desc: "95 mm/hr &bull; Cloudburst Debris Inundation", icon: "🔴" },
    { id: "monsoon_bhagirathi", label: "Bhagirathi Inflow Watch", desc: "45 mm/hr &bull; Tehri Tailwater Reservoir Buffer", icon: "🟡" },
    { id: "normal_baseline", label: "Clear Weather Baseflow", desc: "4 mm/hr &bull; Snowmelt Stream Baseflow", icon: "🟢", active: true }
  ],
  beas: [
    { id: "kullu_2023", label: "Kullu-Manali 2023 Torrential Surge", desc: "95 mm/hr &bull; 1,850 m³/s Extreme Flood", icon: "🔴" },
    { id: "monsoon_beas", label: "Beas River Spill Watch", desc: "50 mm/hr &bull; Parbati Confluence Surcharge", icon: "🟡" },
    { id: "normal_baseline", label: "Clear Alpine Baseflow", desc: "3.5 mm/hr &bull; Solang Snowmelt Regime", icon: "🟢", active: true }
  ],
  teesta: [
    { id: "teesta_2023", label: "Teesta 2023 South Lhonak GLOF", desc: "65 mm/hr &bull; 3,950 m³/s Dam Washout Wave", icon: "🔴" },
    { id: "monsoon_teesta", label: "Teesta Monsoon Fluvial Watch", desc: "55 mm/hr &bull; Mangan Gorge Surcharge", icon: "🟡" },
    { id: "normal_baseline", label: "Clear Weather Baseflow", desc: "4 mm/hr &bull; Teesta Hydro Inflow Safe", icon: "🟢", active: true }
  ],
  chenab: [
    { id: "kishtwar_2021", label: "Kishtwar 2021 Honzar Flash Surge", desc: "110 mm/hr &bull; 1,450 m³/s Torrent Surge", icon: "🔴" },
    { id: "monsoon_chenab", label: "Chenab Overflow Watch", desc: "48 mm/hr &bull; Pir Panjal Monsoon Runoff", icon: "🟡" },
    { id: "normal_baseline", label: "Clear Alpine Baseflow", desc: "3.8 mm/hr &bull; Dul Hasti Hydel Baseflow", icon: "🟢", active: true }
  ]
};

function renderBasinScenarios(regionId) {
  const container = document.getElementById("basin-scenarios-container");
  if (!container) return;
  const scenarios = BASIN_SCENARIOS[regionId] || BASIN_SCENARIOS.alaknanda;
  container.innerHTML = "";

  scenarios.forEach(sc => {
    const btn = document.createElement("button");
    btn.className = `scenario-btn ${sc.active ? "active" : ""}`;
    btn.id = `btn-scenario-${sc.id}`;
    btn.onclick = () => loadScenario(sc.id);
    btn.innerHTML = `${sc.icon} <strong>${sc.label}</strong> (${sc.desc})`;
    container.appendChild(btn);
  });
}

function toggleCrossBasinBenchmarks() {
  const container = document.getElementById("cross-basin-scenarios-container");
  const icon = document.getElementById("cross-basin-icon");
  if (!container) return;
  if (container.style.display === "none" || !container.style.display) {
    container.style.display = "flex";
    if (icon) icon.innerText = "▼";
  } else {
    container.style.display = "none";
    if (icon) icon.innerText = "▶";
  }
}

const PRESET_FACTOR_CONFIGS = {
  chamoli_2021: {
    region_id: "alaknanda",
    rainfall_rate_mm_hr: 105.0, duration_hr: 2.5, catchment_area_km2: 85.0,
    initial_soil_moisture: 0.38, k_sat_mm_hr: 14.5, psi_suction_mm: 110.0, soil_depth_z: 2.2,
    slope_beta_deg: 35.0, c_prime: 8500.0, phi_prime_deg: 32.0,
    manning_n: 0.048, bed_slope_s0: 0.024, bottom_width_b: 28.0
  },
  monsoon_saturated: {
    region_id: "alaknanda",
    rainfall_rate_mm_hr: 52.0, duration_hr: 12.0, catchment_area_km2: 85.0,
    initial_soil_moisture: 0.42, k_sat_mm_hr: 14.5, psi_suction_mm: 110.0, soil_depth_z: 2.2,
    slope_beta_deg: 35.0, c_prime: 8500.0, phi_prime_deg: 32.0,
    manning_n: 0.048, bed_slope_s0: 0.024, bottom_width_b: 28.0
  },
  kedarnath_2013: {
    region_id: "mandakini",
    rainfall_rate_mm_hr: 85.0, duration_hr: 4.0, catchment_area_km2: 68.0,
    initial_soil_moisture: 0.42, k_sat_mm_hr: 16.0, psi_suction_mm: 95.0, soil_depth_z: 1.8,
    slope_beta_deg: 38.0, c_prime: 6500.0, phi_prime_deg: 30.0,
    manning_n: 0.052, bed_slope_s0: 0.029, bottom_width_b: 24.0, breach_surge_m3s: 850.0
  },
  monsoon_mandakini: {
    region_id: "mandakini",
    rainfall_rate_mm_hr: 48.0, duration_hr: 8.0, catchment_area_km2: 68.0,
    initial_soil_moisture: 0.38, k_sat_mm_hr: 16.0, psi_suction_mm: 95.0, soil_depth_z: 1.8,
    slope_beta_deg: 38.0, c_prime: 6500.0, phi_prime_deg: 30.0,
    manning_n: 0.052, bed_slope_s0: 0.029, bottom_width_b: 24.0
  },
  uttarkashi_2012: {
    region_id: "bhagirathi",
    rainfall_rate_mm_hr: 95.0, duration_hr: 3.0, catchment_area_km2: 110.0,
    initial_soil_moisture: 0.40, k_sat_mm_hr: 17.5, psi_suction_mm: 100.0, soil_depth_z: 2.4,
    slope_beta_deg: 33.0, c_prime: 7800.0, phi_prime_deg: 33.0,
    manning_n: 0.046, bed_slope_s0: 0.020, bottom_width_b: 32.0
  },
  monsoon_bhagirathi: {
    region_id: "bhagirathi",
    rainfall_rate_mm_hr: 45.0, duration_hr: 10.0, catchment_area_km2: 110.0,
    initial_soil_moisture: 0.38, k_sat_mm_hr: 17.5, psi_suction_mm: 100.0, soil_depth_z: 2.4,
    slope_beta_deg: 33.0, c_prime: 7800.0, phi_prime_deg: 33.0,
    manning_n: 0.046, bed_slope_s0: 0.020, bottom_width_b: 32.0
  },
  kullu_2023: {
    region_id: "beas",
    rainfall_rate_mm_hr: 95.0, duration_hr: 3.5, catchment_area_km2: 95.0,
    initial_soil_moisture: 0.42, k_sat_mm_hr: 15.2, psi_suction_mm: 105.0, soil_depth_z: 2.0,
    slope_beta_deg: 34.0, c_prime: 7200.0, phi_prime_deg: 32.0,
    manning_n: 0.045, bed_slope_s0: 0.022, bottom_width_b: 30.0
  },
  monsoon_beas: {
    region_id: "beas",
    rainfall_rate_mm_hr: 50.0, duration_hr: 10.0, catchment_area_km2: 95.0,
    initial_soil_moisture: 0.38, k_sat_mm_hr: 15.2, psi_suction_mm: 105.0, soil_depth_z: 2.0,
    slope_beta_deg: 34.0, c_prime: 7200.0, phi_prime_deg: 32.0,
    manning_n: 0.045, bed_slope_s0: 0.022, bottom_width_b: 30.0
  },
  teesta_2023: {
    region_id: "teesta",
    rainfall_rate_mm_hr: 65.0, duration_hr: 4.0, catchment_area_km2: 120.0,
    initial_soil_moisture: 0.40, k_sat_mm_hr: 16.5, psi_suction_mm: 98.0, soil_depth_z: 1.9,
    slope_beta_deg: 36.0, c_prime: 6800.0, phi_prime_deg: 31.0,
    manning_n: 0.050, bed_slope_s0: 0.027, bottom_width_b: 26.0, breach_surge_m3s: 1350.0
  },
  monsoon_teesta: {
    region_id: "teesta",
    rainfall_rate_mm_hr: 55.0, duration_hr: 8.0, catchment_area_km2: 120.0,
    initial_soil_moisture: 0.38, k_sat_mm_hr: 16.5, psi_suction_mm: 98.0, soil_depth_z: 1.9,
    slope_beta_deg: 36.0, c_prime: 6800.0, phi_prime_deg: 31.0,
    manning_n: 0.050, bed_slope_s0: 0.027, bottom_width_b: 26.0
  },
  kishtwar_2021: {
    region_id: "chenab",
    rainfall_rate_mm_hr: 110.0, duration_hr: 2.5, catchment_area_km2: 105.0,
    initial_soil_moisture: 0.39, k_sat_mm_hr: 14.8, psi_suction_mm: 112.0, soil_depth_z: 2.1,
    slope_beta_deg: 37.0, c_prime: 8100.0, phi_prime_deg: 33.0,
    manning_n: 0.047, bed_slope_s0: 0.025, bottom_width_b: 32.0
  },
  monsoon_chenab: {
    region_id: "chenab",
    rainfall_rate_mm_hr: 48.0, duration_hr: 8.0, catchment_area_km2: 105.0,
    initial_soil_moisture: 0.36, k_sat_mm_hr: 14.8, psi_suction_mm: 112.0, soil_depth_z: 2.1,
    slope_beta_deg: 37.0, c_prime: 8100.0, phi_prime_deg: 33.0,
    manning_n: 0.047, bed_slope_s0: 0.025, bottom_width_b: 32.0
  },
  wayanad_2024: {
    region_id: "alaknanda",
    rainfall_rate_mm_hr: 90.0, duration_hr: 3.5, catchment_area_km2: 42.0,
    initial_soil_moisture: 0.41, k_sat_mm_hr: 25.0, psi_suction_mm: 130.0, soil_depth_z: 3.0,
    slope_beta_deg: 34.0, c_prime: 9200.0, phi_prime_deg: 28.0,
    manning_n: 0.044, bed_slope_s0: 0.021, bottom_width_b: 22.0, breach_surge_m3s: 280.0
  },
  amarnath_2022: {
    region_id: "chenab",
    rainfall_rate_mm_hr: 120.0, duration_hr: 0.6, catchment_area_km2: 18.0,
    initial_soil_moisture: 0.22, k_sat_mm_hr: 18.0, psi_suction_mm: 80.0, soil_depth_z: 1.1,
    slope_beta_deg: 42.0, c_prime: 1800.0, phi_prime_deg: 35.0,
    manning_n: 0.055, bed_slope_s0: 0.038, bottom_width_b: 12.0
  },
  normal_baseline: {
    rainfall_rate_mm_hr: 4.0, duration_hr: 1.0, catchment_area_km2: 85.0,
    initial_soil_moisture: 0.20, k_sat_mm_hr: 14.5, psi_suction_mm: 110.0, soil_depth_z: 2.2,
    slope_beta_deg: 35.0, c_prime: 8500.0, phi_prime_deg: 32.0,
    manning_n: 0.048, bed_slope_s0: 0.024, bottom_width_b: 28.0
  }
};

function loadScenario(presetId) {
  document.querySelectorAll(".scenario-btn").forEach(btn => btn.classList.remove("active"));
  const btn = document.getElementById(`btn-scenario-${presetId}`) || document.getElementById(`btn-${presetId.replace("_", "-")}`);
  if (btn) btn.classList.add("active");

  const cfg = PRESET_FACTOR_CONFIGS[presetId] || PRESET_FACTOR_CONFIGS.normal_baseline;
  
  // If the scenario belongs to a specific region, switch basin
  if (cfg.region_id && cfg.region_id !== currentRegionId) {
    switchRegion(cfg.region_id, true);
  }

  setAllSliders(cfg);
  runMultiFactorSimulation(cfg);
}

function setAllSliders(cfg) {
  document.getElementById("slider-rainfall").value = cfg.rainfall_rate_mm_hr;
  document.getElementById("slider-duration").value = cfg.duration_hr;
  document.getElementById("slider-area").value = cfg.catchment_area_km2;
  document.getElementById("slider-moisture").value = cfg.initial_soil_moisture;
  document.getElementById("slider-ksat").value = cfg.k_sat_mm_hr;
  document.getElementById("slider-psi").value = cfg.psi_suction_mm;
  document.getElementById("slider-soildepth").value = cfg.soil_depth_z;
  document.getElementById("slider-slopebeta").value = cfg.slope_beta_deg;
  document.getElementById("slider-cprime").value = cfg.c_prime / 1000.0;
  document.getElementById("slider-phiprime").value = cfg.phi_prime_deg;
  document.getElementById("slider-manningn").value = cfg.manning_n;
  document.getElementById("slider-bedslope").value = cfg.bed_slope_s0;
  document.getElementById("slider-channelb").value = cfg.bottom_width_b;

  updateSliderLabels(cfg);
}

/* -------------------------------------------------------------------------
   7. HISTORICAL DISASTER HINDCASTING VALIDATION MODAL
   ------------------------------------------------------------------------- */
async function fetchHistoricalValidationData() {
  try {
    const res = await fetch("/api/historical-validation");
    historicalSuiteData = await res.json();
    renderHistoricalTable(historicalSuiteData);
  } catch (err) {
    console.error("Failed to load historical validation data:", err);
  }
}

function openHistoricalModal() {
  document.getElementById("historicalModal").classList.add("open");
  if (historicalSuiteData) {
    renderHistoricalTable(historicalSuiteData);
  } else {
    fetchHistoricalValidationData();
  }
}

function closeHistoricalModal() {
  document.getElementById("historicalModal").classList.remove("open");
}

function renderHistoricalTable(data) {
  if (!data) return;

  document.getElementById("hist-mape").innerText = `${data.mean_absolute_percentage_error_q}%`;
  document.getElementById("hist-nse").innerText = `${data.nash_sutcliffe_efficiency_nse}`;
  document.getElementById("hist-slope-acc").innerText = `${data.slope_failure_detection_accuracy_pct}%`;
  document.getElementById("hist-lead-err").innerText = `±${data.mean_lead_time_error_min} min`;

  const tbody = document.getElementById("historical-tbody");
  tbody.innerHTML = "";

  data.events.forEach(ev => {
    const errQ = ev.metrics.relative_discharge_error_pct;
    const badgeClass = errQ < 10 ? "good" : "warning";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${ev.name}</strong><br><span style="font-size: 10px; color: var(--text-muted);">${ev.date}</span></td>
      <td>${ev.terrain_type.split("(")[0]}</td>
      <td><b style="color: #38bdf8;">${ev.observed.peak_discharge_m3s.toLocaleString()} m³/s</b></td>
      <td><b style="color: #f8fafc;">${ev.predicted.peak_discharge_m3s.toLocaleString()} m³/s</b></td>
      <td>${ev.observed.stage_depth_m}m</td>
      <td>${ev.predicted.stage_depth_m}m</td>
      <td>
        <span style="color: ${ev.predicted.factor_of_safety < 1.0 ? '#ef4444' : '#10b981'}; font-weight: bold;">
          FS ${ev.predicted.factor_of_safety.toFixed(2)} (${ev.predicted.slope_failure ? 'FAILURE' : 'STABLE'})
        </span>
      </td>
      <td><span class="badge-hist-error ${badgeClass}">${errQ}%</span></td>
      <td>
        <button class="btn-load-event" onclick="loadHistoricalEventIntoDashboard('${ev.id}')">
          Load Event
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function loadHistoricalEventIntoDashboard(eventId) {
  closeHistoricalModal();
  loadScenario(eventId);
}

/* -------------------------------------------------------------------------
   8. CAP v1.2 EMERGENCY BROADCAST MODAL
   ------------------------------------------------------------------------- */
async function openBroadcastModal() {
  const modal = document.getElementById("broadcastModal");
  modal.classList.add("open");

  if (!currentPipelineData) return;

  const primarySettlement = currentPipelineData.deliverable_1_settlements[0];

  try {
    const res = await fetch("/api/export-cap", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        settlement_id: primarySettlement.id,
        lead_time_min: primarySettlement.evacuation_lead_time_min,
        stage_depth_m: primarySettlement.predicted_stage_m,
        hazard_level: currentPipelineData.overall_hazard_level
      })
    });
    const capData = await res.json();
    document.getElementById("modal-hindi-text").innerText = capData.audio_script_hindi;
    document.getElementById("modal-english-text").innerText = capData.audio_script_english;
    document.getElementById("modal-xml-text").innerText = capData.cap_xml;
  } catch (err) {
    console.error("CAP Export failed:", err);
  }
}

function closeBroadcastModal() {
  document.getElementById("broadcastModal").classList.remove("open");
}

/* -------------------------------------------------------------------------
   9. ALL-BASIN HIMALAYAN SURVEILLANCE MATRIX MODAL
   ------------------------------------------------------------------------- */
async function openAllRegionsModal() {
  const modal = document.getElementById("allRegionsModal");
  if (!modal) return;
  modal.classList.add("open");

  const tbody = document.getElementById("all-regions-tbody");
  if (tbody) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 24px; color: var(--text-muted);">Fetching live multi-basin geotechnical and flood risk telemetries across Himalaya...</td></tr>';
  }

  try {
    const res = await fetch("/api/regions-overview");
    const overview = await res.json();
    renderAllRegionsTable(overview);
  } catch (err) {
    console.error("Failed to load regional overview matrix:", err);
  }
}

function closeAllRegionsModal() {
  const modal = document.getElementById("allRegionsModal");
  if (modal) modal.classList.remove("open");
}

function renderAllRegionsTable(overview) {
  const tbody = document.getElementById("all-regions-tbody");
  if (!tbody) return;
  tbody.innerHTML = "";

  overview.forEach(r => {
    const tr = document.createElement("tr");
    tr.className = "region-matrix-row";
    let badgeStyle = "background: rgba(16,185,129,0.2); color: #34d399; border: 1px solid rgba(16,185,129,0.4);";
    if (r.hazard_level === "RED") badgeStyle = "background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.4);";
    else if (r.hazard_level === "YELLOW") badgeStyle = "background: rgba(245,158,11,0.2); color: #fbbf24; border: 1px solid rgba(245,158,11,0.4);";

    tr.innerHTML = `
      <td>
        <strong style="color: #ffffff; font-size: 13px;">${r.short_name}</strong><br>
        <span style="font-size: 10px; color: var(--text-muted);">${r.name}</span>
      </td>
      <td>
        <strong>${r.state}</strong><br>
        <span style="font-size: 10.5px; color: var(--text-secondary);">${r.district}</span>
      </td>
      <td><span style="font-family: var(--font-mono); font-size: 11px;">${r.elevation_range}</span></td>
      <td><span style="font-size: 11px; color: var(--text-secondary);">${r.dominant_geology.split('&')[0]}</span></td>
      <td><b style="color: #e2e8f0;">${r.critical_settlement}</b></td>
      <td><b style="color: #38bdf8; font-size: 13px;">${r.compound_risk_pct}%</b></td>
      <td>
        <span style="display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; ${badgeStyle}">
          ${r.hazard_level}
        </span>
      </td>
      <td>
        <button class="btn-switch-basin-action" onclick="closeAllRegionsModal(); switchRegion('${r.id}');">
          Open Basin Page &rarr;
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

/* -------------------------------------------------------------------------
   10. LIVE IOT TELEMETRY STREAMING & SENSOR MODAL (SIH26192)
   ------------------------------------------------------------------------- */
let isIoTStreaming = false;
let iotStreamInterval = null;

async function toggleIoTStream() {
  const btn = document.getElementById("btn-toggle-iot-stream");
  const txt = document.getElementById("iot-btn-text");

  isIoTStreaming = !isIoTStreaming;

  if (isIoTStreaming) {
    if (btn) btn.classList.add("active-stream");
    if (txt) txt.innerText = "⏹️ Stop Live Feed";
    
    // Immediate first tick
    await stepIoTStreamTick();

    // Loop every 3 seconds for continuous realistic sensor stream
    iotStreamInterval = setInterval(stepIoTStreamTick, 3000);
  } else {
    if (btn) btn.classList.remove("active-stream");
    if (txt) txt.innerText = "📡 Live IoT Stream";
    if (iotStreamInterval) {
      clearInterval(iotStreamInterval);
      iotStreamInterval = null;
    }
  }
}

async function stepIoTStreamTick() {
  try {
    const res = await fetch(`/api/iot/stream/step?region=${currentRegionId}`);
    if (res.ok) {
      const data = await res.json();
      currentPipelineData = data;
      renderPipelineData(data);
      // Sync input sliders with live incoming telemetry
      if (data.inputs) {
        syncSlidersWithLiveInputs(data.inputs);
      }
    }
  } catch (err) {
    console.error("IoT stream step error:", err);
  }
}

function syncSlidersWithLiveInputs(inputs) {
  const rainSlider = document.getElementById("slider-rainfall");
  const moistSlider = document.getElementById("slider-moisture");
  if (rainSlider) rainSlider.value = Math.round(inputs.rainfall_rate_mm_hr);
  if (moistSlider) moistSlider.value = inputs.initial_soil_moisture.toFixed(2);
  const factors = getFactorValuesFromSliders();
  updateSliderLabels(factors);
}

function openIoTSensorsModal() {
  const modal = document.getElementById("iotSensorsModal");
  if (modal) {
    modal.classList.add("active");
    fetchAndRenderIoTModal();
  }
}

function closeIoTSensorsModal() {
  const modal = document.getElementById("iotSensorsModal");
  if (modal) modal.classList.remove("active");
}

async function fetchAndRenderIoTModal() {
  try {
    const res = await fetch(`/api/iot/status?region=${currentRegionId}`);
    if (res.ok) {
      const t = await res.json();
      updateIoTStationsView(t);
    }
  } catch (err) {
    console.error("Failed to fetch IoT status:", err);
  }
}

function updateIoTStationsView(telemetry) {
  const badge = document.getElementById("station-count-badge");
  if (badge) badge.innerText = `${telemetry.online_stations || 3} Active`;

  const nodeCnt = document.getElementById("iot-modal-nodes-count");
  if (nodeCnt) nodeCnt.innerText = `${telemetry.online_stations || 3} / ${telemetry.station_count || 3} Online`;

  const agg = telemetry.aggregated_telemetry || {};
  const peakRain = document.getElementById("iot-modal-peak-rain");
  if (peakRain) peakRain.innerText = `${agg.peak_station_rainfall_mm_hr || 0} mm/hr`;

  const meanMoist = document.getElementById("iot-modal-mean-moist");
  if (meanMoist) meanMoist.innerText = `${agg.mean_soil_moisture_pct || 22}%`;

  const stage = document.getElementById("iot-modal-river-stage");
  if (stage) stage.innerText = `${agg.max_river_stage_m || 1.2} m`;

  const grid = document.getElementById("iot-stations-grid");
  if (!grid || !telemetry.stations) return;

  grid.innerHTML = telemetry.stations.map(s => {
    const qaColor = s.qa_color || "#10b981";
    const battColor = (s.battery_v && s.battery_v < 3.6) ? "#f59e0b" : "#10b981";
    const m10 = s.soil_moisture_10cm_pct || 24.0;
    const m30 = s.soil_moisture_30cm_pct || 22.0;
    const m60 = s.soil_moisture_60cm_pct || 19.5;

    return `
      <div class="iot-station-card">
        <div class="iot-station-header">
          <div>
            <div class="iot-st-name">${s.station_name || s.name || s.id}</div>
            <div class="iot-st-id">${s.station_id || s.id} &bull; ${s.elevation_m || s.elev_m}m ASL</div>
          </div>
          <span class="iot-st-qa-badge" style="background: ${qaColor}25; color: ${qaColor}; border: 1px solid ${qaColor};">
            ${s.qa_status || "ONLINE_NORMAL"}
          </span>
        </div>

        <div class="iot-metrics-grid">
          <div class="iot-metric-box">
            <span class="iot-metric-lbl">🌧️ Precipitation Influx</span>
            <span class="iot-metric-val">${s.rainfall_rate_mm_hr || 0} mm/hr</span>
          </div>
          <div class="iot-metric-box">
            <span class="iot-metric-lbl">🌊 River Stage Radar</span>
            <span class="iot-metric-val">${s.river_stage_m || 1.2} m</span>
          </div>
          <div class="iot-metric-box">
            <span class="iot-metric-lbl">🔋 Solar Lithium Cell</span>
            <span class="iot-metric-val" style="color: ${battColor};">${s.battery_v || 4.1} V</span>
          </div>
          <div class="iot-metric-box">
            <span class="iot-metric-lbl">📶 LoRa Link (865 MHz)</span>
            <span class="iot-metric-val">${s.lora_rssi_dbm || -78} dBm (${s.lora_snr_db || 9.5} dB)</span>
          </div>
        </div>

        <div class="fdr-moisture-stack">
          <div class="fdr-moisture-title">💧 In-Situ FDR Soil Moisture Profile:</div>
          <div class="fdr-depth-row">
            <span style="width: 45px; color: #94a3b8;">10cm:</span>
            <div class="fdr-depth-bar"><div class="fdr-depth-fill" style="width: ${(m10 / 45) * 100}%;"></div></div>
            <strong style="width: 40px; text-align: right;">${m10}%</strong>
          </div>
          <div class="fdr-depth-row">
            <span style="width: 45px; color: #94a3b8;">30cm:</span>
            <div class="fdr-depth-bar"><div class="fdr-depth-fill" style="width: ${(m30 / 45) * 100}%; background: #0284c7;"></div></div>
            <strong style="width: 40px; text-align: right;">${m30}%</strong>
          </div>
          <div class="fdr-depth-row">
            <span style="width: 45px; color: #94a3b8;">60cm:</span>
            <div class="fdr-depth-bar"><div class="fdr-depth-fill" style="width: ${(m60 / 45) * 100}%; background: #0369a1;"></div></div>
            <strong style="width: 40px; text-align: right;">${m60}%</strong>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

async function injectTestLoRaPacket() {
  const testPacket = {
    station_id: `ST-TEST-${Math.floor(100 + Math.random() * 900)}`,
    basin_id: currentRegionId,
    timestamp: new Date().toISOString(),
    elevation_m: 3100,
    rainfall_5min_mm: 6.5,
    rainfall_rate_mm_hr: 78.0,
    soil_moisture_10cm_pct: 42.5,
    soil_moisture_30cm_pct: 39.8,
    soil_moisture_60cm_pct: 36.1,
    pore_pressure_kpa: 11.4,
    river_stage_m: 3.85,
    battery_v: 4.12,
    lora_rssi_dbm: -79,
    lora_snr_db: 9.8
  };

  try {
    const res = await fetch("/api/iot/telemetry", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(testPacket)
    });
    if (res.ok) {
      alert(`✅ LoRaWAN Packet Ingested Successfully!\nStation: ${testPacket.station_id}\nRainfall: 78.0 mm/hr\nStage: 3.85m`);
      fetchAndRenderIoTModal();
    }
  } catch (err) {
    alert("Packet injection failed: " + err);
  }
}

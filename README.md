# PRAVAH AI (प्रवाह-AI)
### Flash Flood Prediction System for Hilly Regions using Multi-Source Data
**Smart India Hackathon (SIH26192) &bull; Ministry of Home Affairs (MHA) &bull; National Disaster Response Force (NDRF)**

---

## 🌊 Overview

**PRAVAH AI** is a real-time, physics-guided early warning platform engineered for mountainous Himalayan river corridors. It integrates **5 multi-source data streams** to solve the flash flood and compound landslide challenge:

1. **Precipitation & Storm Influx:** Sub-hourly rainfall nowcasting and Doppler Weather Radar (DWR QPE) tracking.
2. **Soil Moisture Saturation:** In-situ 3-depth FDR probes (10cm, 30cm, 60cm) + Green-Ampt infiltration absorption dynamics.
3. **Slope Stability Equilibrium:** Infinite slope geotechnical Factor of Safety ($FS$) under dynamic pore-water pressure buildup.
4. **Historical Disaster Data & Colluvial Damming:** GSI Bhukosh landslide susceptibility integration + dynamic dam impoundment & Froehlich catastrophic breach hydraulics when $FS < 1.0$.
5. **Real-Time IoT Telemetry:** Upstream solar LoRaWAN (865 MHz) / 4G sensor network with Edge QA anomaly filtering.

---

## ⚡ The 2 Core Deliverables

### 1. Multi-Tiered Actionable Evacuation Lead Time (90 to 180 Minutes)
Resolves the physical lead-time paradox in steep mountain gorges:
* **Tier 1 (Atmospheric Doppler Radar Nowcast):** $120\text{ to }180\text{ minutes}$ advance tracking of convective cloudburst cores aloft before ground impact.
* **Tier 2 (Catchment Soil Saturation Deficit Lag):** $60\text{ to }90\text{ minutes}$ soil infiltration absorption time before unbuffered overland Hortonian sheetwash peaks.
* **Tier 3 (In-Stream Hydraulic Wave Routing):** $15\text{ to }45\text{ minutes}$ kinematic wave celerity travel lag down the river reach.

### 2. Hyper-Local Village & Ward Level Forecasts
Inverts 1D Manning's hydraulics at settlement cross-sections to predict exact river stage $h(t)$ in meters, water velocity, and automated Common Alerting Protocol (**CAP v1.2 XML**) warnings for local Panchayats and SDRF VHF radios.

---

## 🧠 Physics-Guided Machine Learning (PGNN) Hybrid Pipeline

* Combines deterministic **physics mass-conservation** (Green-Ampt + Manning + Infinite Slope) with a **Random Forest & Gradient Boosted Regression ensemble** trained on 650 Himalayan disaster events (Kedarnath 2013, Chamoli 2021, Kullu 2023, Teesta 2023, Wayanad 2024, Kishtwar 2021).
* **Bayesian Fusion:** 60% physics ground truth + 40% data-driven pattern matching with a real-time AI Concordance Indicator guarding against hallucinations.

---

## 🏔️ Monitored Himalayan Basins

* **Alaknanda & Rishi Ganga Corridor** (Chamoli, Uttarakhand)
* **Mandakini River Corridor** (Kedarnath & Rudraprayag, Uttarakhand)
* **Bhagirathi River Basin** (Uttarkashi & Tehri, Uttarakhand)
* **Beas River Valley** (Kullu & Manali, Himachal Pradesh)
* **Teesta River Corridor** (South Lhonak & Mangan, North Sikkim)
* **Chenab River Gorges** (Machail & Kishtwar, Jammu & Kashmir)

---

## 🚀 Quick Start & Installation

### Prerequisites
* Python 3.10+
* Git

### Installation
```bash
# 1. Clone repository
git clone https://github.com/AyushmanSingh-dev/PRAVAH-AI.git
cd PRAVAH-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
python app.py
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📁 Repository Structure

```
PRAVAH-AI/
├── app.py                     # Flask web server & REST API endpoints
├── engine/
│   ├── physics.py             # 5-factor physical simulation engine & dam breach
│   ├── catchment_data.py      # Multi-basin geotechnical & GIS river coordinates
│   ├── historical_validation.py # National disaster benchmark suite
│   ├── iot_manager.py         # LoRaWAN / MQTT telemetry parser & Edge QA filter
│   ├── ml_model.py            # Physics-Guided Neural Network (PGNN) pipeline
│   └── models/
│       └── pravah_ml_model.joblib # Serialized trained ML model artifact
├── templates/
│   └── index.html             # Interactive command dashboard UI
├── static/
│   ├── css/style.css          # Glassmorphic UI styles & component tokens
│   └── js/app.js              # Leaflet GIS, Chart.js hydrograph & IoT streamer
├── data/
│   └── iot_telemetry_stream.jsonl # Realistic multi-station time-series telemetry
├── tests/
│   ├── test_physics.py        # Core physics unit tests
│   └── test_historical_hindcast.py # Disaster hindcast validation tests
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

---

## 📄 License & Attribution
Developed for Smart India Hackathon — Problem Statement **SIH26192** under the Ministry of Home Affairs / National Disaster Response Force (NDRF).

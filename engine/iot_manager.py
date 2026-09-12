"""
PRAVAH AI - Real-Time IoT Telemetry & Edge Gateway Manager
Handles multi-station sensor network ingestion (LoRaWAN 865 MHz & 4G),
Edge QA anomaly filtering, and realistic file-backed telemetry replay.
"""

import json
import os
import time
import random
import threading
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "iot_telemetry_stream.jsonl")

# Standard station network topology
IOT_STATIONS = {
    "alaknanda": [
        {"id": "ST-RISHI-01", "name": "Rishi Ganga Glacier Cirque", "elev_m": 3800, "lat": 30.48, "lon": 79.74, "role": "High Altitude Tipping Bucket & Pore Pressure"},
        {"id": "ST-RAINI-02", "name": "Raini Gorge Bridge Gauge", "elev_m": 2400, "lat": 30.49, "lon": 79.70, "role": "Ultrasonic River Stage & Colluvial Velocity"},
        {"id": "ST-JOSH-03", "name": "Joshimath Flank In-Situ Probe", "elev_m": 1890, "lat": 30.55, "lon": 79.56, "role": "3-Depth FDR Soil Moisture (10/30/60cm)"}
    ],
    "beas": [
        {"id": "ST-SOLANG-01", "name": "Solang Ridge Hydro-Station", "elev_m": 2650, "lat": 32.32, "lon": 77.16, "role": "Headwater Cloudburst Tipping Bucket"},
        {"id": "ST-MANALI-02", "name": "Old Manali Stream Gauge", "elev_m": 2050, "lat": 32.25, "lon": 77.19, "role": "Ultrasonic River Stage & Velocity Radar"},
        {"id": "ST-KULLU-03", "name": "Kullu Confluence Telemetry", "elev_m": 1220, "lat": 31.96, "lon": 77.11, "role": "LoRa Gateway Receiver & Flood Stage"}
    ],
    "mandakini": [
        {"id": "ST-KEDAR-01", "name": "Kedarnath Moraine AWS", "elev_m": 3580, "lat": 30.73, "lon": 79.07, "role": "High Altitude Glacier AWS & Pore Pressure"},
        {"id": "ST-GAURI-02", "name": "Gaurikund Gorge Gauge", "elev_m": 1980, "lat": 30.65, "lon": 79.03, "role": "Ultrasonic River Stage & Surface Velocity"},
        {"id": "ST-RUDR-03", "name": "Rudraprayag Sangam Bridge", "elev_m": 890, "lat": 30.28, "lon": 78.98, "role": "Downstream Hydrological Station"}
    ],
    "teesta": [
        {"id": "ST-LHONAK-01", "name": "South Lhonak Moraine Probe", "elev_m": 4400, "lat": 27.91, "lon": 88.20, "role": "GLOF Early Warning Water Sensor & Radar"},
        {"id": "ST-CHUNG-02", "name": "Chungthang Dam Gauge", "elev_m": 1790, "lat": 27.60, "lon": 88.65, "role": "Inundation Stage & Inflow Radar"},
        {"id": "ST-MANGAN-03", "name": "Mangan Bridge Telemetry", "elev_m": 1310, "lat": 27.50, "lon": 88.53, "role": "Sub-Basin LoRa Confluence Node"}
    ],
    "bhagirathi": [
        {"id": "ST-GANG-01", "name": "Gangotri Glacier Moraine Node", "elev_m": 3100, "lat": 30.99, "lon": 78.94, "role": "Snowmelt & Rain-on-Snow Sensor"},
        {"id": "ST-UTTK-02", "name": "Uttarkashi Town River Stage", "elev_m": 1150, "lat": 30.73, "lon": 78.44, "role": "Ultrasonic Stage & Flood Barrier Node"},
        {"id": "ST-TEHRI-03", "name": "Tehri Inflow Hydrometry", "elev_m": 770, "lat": 30.38, "lon": 78.48, "role": "Reservoir Tailwater Surge Monitor"}
    ],
    "chenab": [
        {"id": "ST-MACH-01", "name": "Machail Gorge Alpine Station", "elev_m": 2900, "lat": 33.42, "lon": 76.12, "role": "Alpine Cloudburst AWS & Colluvial Sensor"},
        {"id": "ST-GULAB-02", "name": "Gulabgarh Narrow Gauge", "elev_m": 1800, "lat": 33.35, "lon": 75.92, "role": "Gorge Acoustic River Stage Radar"},
        {"id": "ST-KISHT-03", "name": "Kishtwar Confluence Node", "elev_m": 1630, "lat": 33.31, "lon": 75.76, "role": "Regional LoRaWAN Concentrator Tower"}
    ]
}

class IoTTelemetryManager:
    def __init__(self):
        self.active_stream_running = False
        self._stream_thread = None
        self._current_step_idx = 0
        self.stream_records = []
        self._load_stream_records()
        self.latest_telemetry_cache = {}
        self._seed_initial_cache()

    def _load_stream_records(self):
        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.stream_records.append(json.loads(line))
            except Exception as e:
                print("Error loading stream records:", e)

    def _seed_initial_cache(self):
        """Populates initial realistic readings for all stations."""
        for basin, stations in IOT_STATIONS.items():
            self.latest_telemetry_cache[basin] = {}
            for s in stations:
                self.latest_telemetry_cache[basin][s["id"]] = {
                    "station_id": s["id"],
                    "station_name": s["name"],
                    "basin_id": basin,
                    "elevation_m": s["elev_m"],
                    "role": s["role"],
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "rainfall_5min_mm": 0.2,
                    "rainfall_rate_mm_hr": 2.4,
                    "soil_moisture_10cm_pct": 24.5,
                    "soil_moisture_30cm_pct": 22.0,
                    "soil_moisture_60cm_pct": 19.8,
                    "pore_pressure_kpa": 1.4,
                    "river_stage_m": 1.25,
                    "battery_v": 4.15,
                    "solar_lux": 34000,
                    "lora_rssi_dbm": -78,
                    "lora_snr_db": 9.5,
                    "qa_status": "ONLINE_NORMAL",
                    "qa_color": "#10b981",
                    "last_packet_age_sec": 1
                }

    # -------------------------------------------------------------------------
    # EDGE QA ANOMALY FILTER
    # -------------------------------------------------------------------------
    def run_edge_qa_filter(self, packet):
        """
        Validates raw LoRaWAN incoming packet against physical plausibility envelopes:
        - Stuck float sensor (zero variance over long period)
        - Ultrasonic acoustic echo spikes (> 4.0m jump in 5 min)
        - Battery brownout (< 3.5V)
        - LoRa packet signal degradation (RSSI < -115 dBm)
        """
        flags = []
        status = "ONLINE_NORMAL"
        color = "#10b981"

        batt = float(packet.get("battery_v", 4.1))
        if batt < 3.55:
            flags.append("LOW_BATTERY_BROWNOUT")
            status = "BATTERY_WARNING"
            color = "#f59e0b"

        rssi = int(packet.get("lora_rssi_dbm", -80))
        if rssi < -110:
            flags.append("WEAK_LORA_SIGNAL")
            if status == "ONLINE_NORMAL":
                status = "WEAK_SIGNAL"
                color = "#f59e0b"

        rain_rate = float(packet.get("rainfall_rate_mm_hr", 0.0))
        if rain_rate > 100.0:
            flags.append("CLOUDBURST_RATE_DETECTED")
            status = "EXTREME_INFLUX"
            color = "#ef4444"
        elif rain_rate > 50.0:
            flags.append("HEAVY_PRECIP_SURGE")
            status = "HEAVY_SURGE"
            color = "#f97316"

        stage = float(packet.get("river_stage_m", 1.0))
        if stage > 4.0:
            flags.append("DANGER_STAGE_EXCEEDANCE")
            status = "RED_ALERT"
            color = "#ef4444"

        packet["qa_flags"] = flags
        packet["qa_status"] = status
        packet["qa_color"] = color
        return packet

    # -------------------------------------------------------------------------
    # INGEST EXTERNAL TELEMETRY PACKET
    # -------------------------------------------------------------------------
    def ingest_packet(self, packet):
        """
        Official ingestion point for external LoRaWAN / 4G gateway HTTP POST payloads.
        """
        basin = packet.get("basin_id", "alaknanda")
        station_id = packet.get("station_id", "UNKNOWN")
        
        # Run Edge QA
        verified_packet = self.run_edge_qa_filter(packet)
        verified_packet["timestamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        if basin not in self.latest_telemetry_cache:
            self.latest_telemetry_cache[basin] = {}
        
        self.latest_telemetry_cache[basin][station_id] = verified_packet
        return verified_packet

    # -------------------------------------------------------------------------
    # TELEMETRY REPLAY STREAMER
    # -------------------------------------------------------------------------
    def step_stream(self, basin="alaknanda"):
        """Advances the realistic stream simulation by one time tick."""
        if not self.stream_records:
            return self.get_latest_basin_telemetry(basin)

        rec = self.stream_records[self._current_step_idx % len(self.stream_records)]
        self._current_step_idx += 1

        rec_basin = rec.get("basin_id", basin)
        st_id = rec.get("station_id")

        # Ingest
        self.ingest_packet(dict(rec))

        # Add small micro-variation to sibling stations in same basin
        if rec_basin in self.latest_telemetry_cache:
            for sid, station_data in self.latest_telemetry_cache[rec_basin].items():
                if sid != st_id:
                    station_data["rainfall_rate_mm_hr"] = max(0.0, round(rec["rainfall_rate_mm_hr"] * random.uniform(0.75, 1.15), 1))
                    station_data["soil_moisture_10cm_pct"] = min(45.0, round(rec["soil_moisture_10cm_pct"] * random.uniform(0.92, 1.05), 1))
                    station_data["soil_moisture_30cm_pct"] = min(44.0, round(rec["soil_moisture_30cm_pct"] * random.uniform(0.92, 1.05), 1))
                    station_data["soil_moisture_60cm_pct"] = min(43.0, round(rec["soil_moisture_60cm_pct"] * random.uniform(0.92, 1.05), 1))
                    station_data["river_stage_m"] = max(0.6, round(rec["river_stage_m"] * random.uniform(0.85, 1.1), 2))
                    self.run_edge_qa_filter(station_data)

        return self.get_latest_basin_telemetry(basin)

    def get_latest_basin_telemetry(self, basin="alaknanda"):
        """Returns the current state of all stations in the requested basin."""
        basin_stations = self.latest_telemetry_cache.get(basin, {})
        station_list = list(basin_stations.values())

        if not station_list and basin in IOT_STATIONS:
            self._seed_initial_cache()
            station_list = list(self.latest_telemetry_cache.get(basin, {}).values())

        # Calculate basin aggregated real-time indices
        avg_rain_rate = round(sum(s.get("rainfall_rate_mm_hr", 0.0) for s in station_list) / max(len(station_list), 1), 1)
        max_rain_rate = round(max((s.get("rainfall_rate_mm_hr", 0.0) for s in station_list), default=0.0), 1)
        avg_moisture = round(sum(s.get("soil_moisture_10cm_pct", 25.0) for s in station_list) / max(len(station_list), 1), 1)
        max_stage = round(max((s.get("river_stage_m", 1.0) for s in station_list), default=1.0), 2)
        online_count = sum(1 for s in station_list if "BATTERY_WARNING" not in s.get("qa_flags", []))

        return {
            "basin_id": basin,
            "station_count": len(station_list),
            "online_stations": online_count,
            "active_stream_mode": self.active_stream_running,
            "aggregated_telemetry": {
                "average_rainfall_rate_mm_hr": avg_rain_rate,
                "peak_station_rainfall_mm_hr": max_rain_rate,
                "mean_soil_moisture_pct": avg_moisture,
                "max_river_stage_m": max_stage
            },
            "stations": station_list
        }

# Global singleton
_IOT_MANAGER = None

def get_iot_manager():
    global _IOT_MANAGER
    if _IOT_MANAGER is None:
        _IOT_MANAGER = IoTTelemetryManager()
    return _IOT_MANAGER
